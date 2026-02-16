# tests/test_generate_data.py

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from datetime import datetime, timedelta
import pandas as pd

# Import the script or the specific functions you're testing, adjusting the import path as necessary

from modules.utils import random_dates


class TestDataGeneration(unittest.TestCase):
    def test_random_dates(self):
        start = pd.to_datetime("2020-01-01")
        end = pd.to_datetime("2020-01-10")
        dates = random_dates(start, end, n=5)
        self.assertEqual(len(dates), 5, "Should generate 5 dates")
        for date in dates:
            self.assertTrue(
                start <= date <= end, "Date should be within the specified range"
            )


if __name__ == "__main__":
    unittest.main()
