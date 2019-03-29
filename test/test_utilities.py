"""
    Tests for utilities.py
"""

import unittest


from v_log import utilities as u


class TestVlog(unittest.TestCase):
    """Test utilities"""

    def test_log_aux(self):
        """
            Test fancy_string_time_form_seconds
        """

        data = [(10, "10.00s"), (70, "1m 10s"), (3670, "1h 1m 10s")]

        for num, result in data:
            self.assertEqual(u.fancy_string_time_from_seconds(num), result)
