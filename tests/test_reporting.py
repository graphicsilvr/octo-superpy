# tests/test_reporting.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest

from modules.reporting import report_inventory, report_revenue
from datetime import datetime

class TestReporting(unittest.TestCase):

    def test_report_inventory(self):
        # Test inventory report functionality
        inventory_report = report_inventory()
        # Assert expected outcomes, such as the report being a dictionary, having certain keys, etc.
        self.assertIsInstance(inventory_report, dict)

    def report_revenue(start_date, end_date):
        sold_data = read_csv('data/sold.csv')
        revenue = 0

        for row in sold_data:
            if len(row) >= 3:  # Ensure row has at least 3 elements
                try:
                    sale_date = datetime.strptime(row[2], '%Y-%m-%d')
                    if start_date <= sale_date <= end_date:
                        revenue += float(row[3])
                except (ValueError, IndexError):
                    continue  # Skip rows with invalid data or missing fields

        return revenue

if __name__ == '__main__':
    unittest.main()
