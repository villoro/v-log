"""
    Tests for v_log.py
"""

import unittest


from v_log.v_log import VLogger


class TestVlog(unittest.TestCase):
    """Test v_log"""

    log = VLogger(__file__)

    def test_basic_usage(self):
        """
            Test all levels of log
        """

        # Test all logging levels
        self.log.critical("Test critical")
        self.log.error("Test error")
        self.log.warning("Test warning")
        self.log.info("Test info")
        self.log.debug("Test debug")

    def test_args(self):
        """
            Test that you can pass arguments
        """
        # Test args
        self.log.info("Test logging %s", "parsing")

    def test_kwargs(self):
        """
            Test that you can pass kwargs
        """

        # Test time
        self.log.info("Test time", time=10)

        # Test error and time+error
        try:
            1 / 0
        except Exception as e:
            self.log.error("Try errors", error=e)
            self.log.error("Try errors %s", "full", time=10, error=e)

        # Test invalid num
        self.log.info("Test time", time="a")
