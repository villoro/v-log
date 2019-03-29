"""
    Custom log that will print info and save it in a csv file.
    It extends the default python log
"""

import logging
import sys
from termcolor import colored
import constants as c
import utilities as u


class _LoggerConsole(logging.Logger):
    """
        Custom log that extends default python log.
        The purpose is to add colors for the terminal:
            critical:   red
            error:      red
            warning:    yellow
            info:       default (usually white)
            debug:      green
    """

    def __init__(self, module_name):
        super().__init__(module_name)

        from colorama import init

        init()

    def critical(self, msg, *args, **kwargs):
        super().critical(colored(msg, "red"), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        super().error(colored(msg, "red"), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        super().warning(colored(msg, "yellow"), *args, **kwargs)

    # No need to extend info since it has no color

    def debug(self, msg, *args, **kwargs):
        super().debug(colored(msg, "green"), *args, **kwargs)


def get_csv_file_handler(uri_log, file_log_level):
    """
        Creates a file handler.

        Args:
            uri_log:        uri of the log to be saved
            file_log_level: minimum level for file log

        Returns:
            the handler
    """

    handler = logging.FileHandler(uri_log)
    handler.setLevel(file_log_level)
    mformat = "%(name)s;%(levelname)s;%(asctime)s;%(message)s"
    handler.setFormatter(logging.Formatter(mformat, datefmt="%Y-%m-%d %H:%M:%S"))

    return handler


def get_console_handler(console_log_level):
    """
        Creates a file handler.

        Args:
            console_log_level:  minimum level for file terminal

        Returns:
            the handler
    """

    handler = logging.StreamHandler()
    handler.setLevel(console_log_level)
    mformat = "%(levelname)-8s [%(asctime)s] %(name)-20s %(message)s"
    handler.setFormatter(logging.Formatter(mformat, datefmt="%Y-%m-%d %H:%M:%S"))

    return handler


class _CustomLogger:
    """
        Log class that saves prints messages with colors in the console.
        It also stores everything in a csv file.

        Avaiable levels:
            Critical:   50
            Error:      40
            Warning:    30
            Info:       20
            Debug:      10

        Args:
            module_name:        name of the module
            uri_log:            uri of the file where log will be stored
            file_log_level:     minimum level of log events in order to be writed
            console_log_level:  minimum level of log events in order to be printed
    """

    @staticmethod
    def split_kwargs(**kwa_in):
        """
            This catches error and time from kwa_in

            Args:
                kwa_in:     kwargs to read

            Returns:
                kwa_out:    kwargs with time and error
                kwa_in:     kwargs without time and error
        """
        kwa_out = {}
        for x in ["time", "error_name", "error", "error_line"]:
            kwa_out[x] = ""

        if "time" in kwa_in:
            kwa_out["time"] = kwa_in["time"]

            # Drop time from kwa_in
            kwa_in.pop("time", None)

        if "error" in kwa_in:
            kwa_out["error_name"] = kwa_in["error"].__class__.__name__
            kwa_out["error"] = u.to_one_line(kwa_in["error"])
            kwa_out["error_line"] = sys.exc_info()[-1].tb_lineno

            # Drop error from kwa_in
            kwa_in.pop("error", None)

        return kwa_out, kwa_in

    @staticmethod
    def concat_info_console(msg, **kwargs):
        """ This will append time and error for terminal """

        # This ensures that | is painted
        msg = "| " + msg

        # Check if there is something in kwargs
        mbool = False
        for _, value in kwargs.items():
            mbool += bool(value)

        # If there is info about time or error, show it!
        if mbool:
            msg += "\n{:52}".format("")

            if kwargs["time"]:
                mtime = u.fancy_string_time_from_seconds(kwargs["time"])
                msg += "| [Time]: {time:10} ".format(time=mtime)

            if kwargs["error"]:
                msg += "| [Error] [L: {error_line}]: ({error_name}) {error}".format(**kwargs)

        return msg

    @staticmethod
    def concat_info_file(msg, **kwargs):
        """ This will concat time and error info for file """

        kwargs["time"] = str(kwargs["time"]).replace(".", ",")

        msg = "{};{time};{error_name};{error};{error_line}".format(msg, **kwargs)

        # Crop last ; it will be used when time or error is missing
        while msg[-1] == ";":
            msg = msg[:-1]

        return msg

    def __init__(
        self,
        module_name="base",
        uri_log=c.DEFAULT_URI_LOG,
        file_log_level=logging.INFO,
        console_log_level=logging.INFO,
    ):

        # Fix module name
        module_name = u.fix_module_name(module_name)

        # Add headers if needed
        u.create_file_headers(uri_log)

        self.log_c = _LoggerConsole(module_name)
        self.log_f = logging.Logger(module_name)

        # Default levels
        self.log_c.setLevel(logging.DEBUG)
        self.log_f.setLevel(logging.DEBUG)

        # Add handlers
        self.log_c.addHandler(get_console_handler(console_log_level))
        self.log_f.addHandler(get_csv_file_handler(uri_log, file_log_level))

    def call_super(self, func_c, func_f, msg, *args, **kwargs):
        """
            Auxiliar function to call both logs and apply extra things to the message
        """

        kwa_extra, kwa_super = self.split_kwargs(**kwargs)
        msg = u.to_one_line(msg)

        func_c(self.concat_info_console(msg, **kwa_extra), *args, **kwa_super)
        func_f(self.concat_info_file(msg, **kwa_extra), *args, **kwa_super)

    def critical(self, msg, *args, **kwargs):
        """ Log critical problem """
        self.call_super(self.log_c.critical, self.log_f.critical, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """ Log an error """
        self.call_super(self.log_c.error, self.log_f.error, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """ Log a warning """
        self.call_super(self.log_c.warning, self.log_f.warning, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """ Log some info """
        self.call_super(self.log_c.info, self.log_f.info, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """ Log a message for debugging """
        self.call_super(self.log_c.debug, self.log_f.debug, msg, *args, **kwargs)
