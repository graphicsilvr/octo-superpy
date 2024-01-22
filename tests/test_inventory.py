# tests/test_inventory.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from modules.inventory import buy_product

class TestInventory(unittest.TestCase):

    def test_buy_product(self):
        # Setup test data
        product_name = "Test Product"
        price = 10.00
        expiration_date = "2024-01-01"
        
        # Call the function
        buy_product(product_name, price, expiration_date)

        # Assert expected outcomes (this is just an example, adjust as needed)
        # For example, check if 'bought.csv' has the new product entry

if __name__ == '__main__':
    unittest.main()
