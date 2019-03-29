"""
    Utilities to handle time and input/output operations
"""

import os
import constants as c


def fancy_string_time_from_seconds(input_seconds):
    """
        It converts a time in seconds into a string that is beautiful to read

        Args:
            input_seconds:  time in seconds

        Returns:
            a fancy string like 1h 21m 42s
    """

    # Parse if needed
    try:
        input_seconds = float(input_seconds)

    except ValueError:
        return input_seconds

    # extract hours and minutes
    minutes, seconds = divmod(input_seconds, 60)
    hours, minutes = divmod(minutes, 60)

    # only print what it is not 0
    if hours > 0:
        return "%dh %dm %02ds" % (hours, minutes, seconds)

    if minutes > 0:
        return "%dm %02ds" % (minutes, seconds)

    return "%.2fs" % seconds


def to_one_line(msg, separator=c.DEFAULT_CSV_DELIMITER):
    """
        Replaces new line char for another in order to make csv log readable
    """

    return str(msg).replace("\n", " | ").replace(separator, ":")


def create_file_headers(uri_log, separator=c.DEFAULT_CSV_DELIMITER):
    """
        Creates a csv file for log with the headers
    """

    # To get path exclude file name
    if "/" in uri_log:
        path = "/".join(uri_log.split("/")[:-1])
        if not os.path.isdir(path):
            os.makedirs(path, exist_ok=True)

    # If log don't exist create headers
    if not os.path.isfile(uri_log):
        with open(uri_log, mode="w") as file:
            file.write(separator.join(c.COLS_ALL))
            file.write("\n")


def fix_module_name(name, base_path=c.DEFAULT_BASE_PATH):
    """
        Fixes module name in order to make it as shorter and generic as possible.
        It will keep everything after 'base_path'.

        Args:
            name:       module name
            base_path:  name of the root folder
    """

    # Clean endings
    for x in [".py"]:
        if name.endswith(x):
            name = name[: -len(x)]

    # Use slash as separations
    name = name.replace("\\", "/")

    # Clean beginnigs
    if base_path in name:
        uri_list = name.split("/")
        name = "/".join(uri_list[uri_list.index(base_path) + 1 :])

    return name
