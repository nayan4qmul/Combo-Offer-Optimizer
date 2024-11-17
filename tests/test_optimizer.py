import unittest
from src.optimizer import ComboOfferOptimizer

class TestComboOfferOptimizer(unittest.TestCase):
    def setUp(self):
        # Initialize with test data
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
        self.product_prices = {"Laptop": 1000, "Mouse": 20, "Keyboard": 50, "Smartphone": 800, "Earphones": 150, "Tablet": 600}
        self.inventory_levels = {"Laptop": 10, "Mouse": 200, "Keyboard": 150, "Smartphone": 50, "Earphones": 100, "Tablet": 60}
        self.objectives = {"revenue_growth": 1, "inventory_clearance": 1, "category_growth": 0.5, "customer_retention": 0.5}
        self.optimizer = ComboOfferOptimizer(self.transactions, self.product_hierarchy, self.product_prices, self.inventory_levels, self.objectives)

    def test_optimizer(self):
        optimized_combos = self.optimizer.optimize_all_levels()
        self.assertIsNotNone(optimized_combos)
        self.assertIn("Product", optimized_combos)
        self.assertIn("Subcategory", optimized_combos)
        self.assertIn("Category", optimized_combos)

if __name__ == "__main__":
    unittest.main()