import sys
sys.path.append('/workspaces/Combo-Offer-Optimizer/')

import unittest
import pandas as pd
from src.utils import load_product_hierarchy, load_transactions, map_to_hierarchy

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.product_hierarchy = pd.DataFrame({
            "ProductID": ["Laptop", "Mouse", "Keyboard", "Smartphone", "Earphones", "Tablet"],
            "Category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories", "Electronics"],
            "Subcategory": ["Computers", "Input Devices", "Input Devices", "Mobile", "Audio", "Tablets"]
        })
    
    def test_map_to_hierarchy(self):
        category, subcategory = map_to_hierarchy("Laptop", self.product_hierarchy)
        self.assertEqual(category, "Electronics")
        self.assertEqual(subcategory, "Computers")

    def test_load_product_hierarchy(self):
        # Simulating loading CSV
        mock_hierarchy = pd.DataFrame({
            "ProductID": ["Laptop", "Mouse"],
            "Category": ["Electronics", "Accessories"],
            "Subcategory": ["Computers", "Input Devices"]
        })
        mock_hierarchy.to_csv("mock_product_hierarchy.csv", index=False)
        loaded_hierarchy = load_product_hierarchy("mock_product_hierarchy.csv")
        self.assertTrue("ProductID" in loaded_hierarchy.columns)
    
    def test_load_transactions(self):
        # Simulating loading transaction data
        mock_transactions = pd.DataFrame({
            "TransactionID": [1, 2, 3],
            "Products": [["Laptop", "Mouse"], ["Smartphone", "Earphones"], ["Tablet", "Keyboard"]]
        })
        mock_transactions.to_csv("mock_transactions.csv", index=False)
        loaded_transactions = load_transactions("mock_transactions.csv")
        self.assertEqual(len(loaded_transactions), 3)

if __name__ == "__main__":
    unittest.main()