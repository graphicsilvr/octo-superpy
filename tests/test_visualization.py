import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.inventory import buy_product, sell_product

import unittest
from modules.visualization import plot_sales_over_time
import os


class TestVisualization(unittest.TestCase):
    def setUp(self):
        # Setup by buying and selling some products to generate data
        buy_product("Apple", 1.00, "2023-01-01")
        sell_product("Apple", 1.50)

    def test_plot_sales_over_time(self):
        # Assuming plot_sales_over_time takes a list of tuples (date, amount)
        # We need to prepare this data from the CSV files
        # This is a placeholder for the actual data preparation
        sales_data = [("2023-01-01", 1.00), ("2023-01-02", 1.50)]
        try:
            plot_sales_over_time(sales_data)
            print("Visualization test passed: Plot displayed successfully")
        except Exception as e:
            self.fail(f"Visualization test failed: {e}")

    def tearDown(self):
        # Clean up: Delete the test CSV files or reset them to their original state
        os.remove("data/bought.csv")
        os.remove("data/sold.csv")


if __name__ == "__main__":
    unittest.main()
