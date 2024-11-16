# tests/test_time_management.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from modules.time_management import advance_time, get_current_date
from datetime import datetime, timedelta

class TestTimeManagement(unittest.TestCase):

    def test_advance_time(self):
        test_file_path = 'test_current_date.txt'  # Specify a test file path

        # Setup - write a known date to the test file
        with open(test_file_path, 'w') as file:
            file.write('2023-03-15')  # Write a specific date for testing

        # Setup - get current date from the test file
        current_date = get_current_date(test_file_path)

        # Call the function to advance time by 1 day
        advance_time(1, test_file_path)

        # Assert expected outcomes
        new_date = get_current_date(test_file_path)
        expected_date = current_date + timedelta(days=1)
        self.assertEqual(new_date, expected_date)

if __name__ == '__main__':
    unittest.main()

