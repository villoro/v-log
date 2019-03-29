"""
    Tests for utilities.py
"""

import os
import shutil
import unittest


from v_log import utilities as u


class TestVlog(unittest.TestCase):
    """Test utilities"""

    def test_fancy_string_time(self):
        """
            Test fancy_string_time_form_seconds
        """

        data = [(10, "10.00s"), (70, "1m 10s"), (3670, "1h 1m 10s")]

        for num, result in data:
            self.assertEqual(u.fancy_string_time_from_seconds(num), result)

    def test_filename(self):
        """
            Test that splits the name correctly
        """

        data = [
            ("PYTHON/src/utilities/uio.py", "utilities/uio"),
            ("PYTHON/src/utilities/uio", "utilities/uio"),
            ("PYTHON\\src\\utilities\\uio", "utilities/uio"),
            ("main.py", "main"),
        ]

        for inp, out in data:
            self.assertEqual(u.fix_module_name(inp), out)

    @staticmethod
    def clean_path(path):
        """ Delete folder if it exists from previous runs """

        if os.path.isdir(path):
            try:
                shutil.rmtree(path)

            except IOError:
                pass

    def test_file_headers(self):
        """
            Test writes a file with headers
        """

        filename = "temp/log.csv"
        path = filename.split("/")[0]

        # Clean the path so that it get's created when testing
        self.clean_path(path)

        u.create_file_headers(filename)

        self.assertTrue(os.path.isdir(path))

        # Clean it to avoid unuseful data
        self.clean_path(path)
