import unittest
import pandas as pd
from src.support_calculator import calculate_support

class TestSupportCalculator(unittest.TestCase):
    
    def setUp(self):
        self.transactions = [
            ["Laptop", "Mouse", "Keyboard"],
            ["Smartphone", "Earphones"],
            ["Tablet", "Keyboard"],
        ]
        self.product_hierarchy = pd.DataFrame({
            "ProductID": ["Laptop", "Mouse", "Keyboard", "Smartphone", "Earphones", "Tablet"],
            "Category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories", "Electronics"],
            "Subcategory": ["Computers", "Input Devices", "Input Devices", "Mobile", "Audio", "Tablets"]
        })

    def test_calculate_support(self):
        support, item_pairs = calculate_support(self.transactions, self.product_hierarchy)
        
        # Check if support for products matches expectations
        self.assertAlmostEqual(support["Product"]["Laptop"], 1/3)
        self.assertAlmostEqual(support["Product"]["Mouse"], 1/3)
        self.assertAlmostEqual(support["Product"]["Keyboard"], 2/3)
        
        # Check if lift for product pair Laptop & Mouse is calculated correctly
        pair_data = item_pairs["Product"][("Laptop", "Mouse")]
        self.assertGreater(pair_data["support"], 0)
        self.assertGreater(pair_data["lift"], 0)

if __name__ == "__main__":
    unittest.main()