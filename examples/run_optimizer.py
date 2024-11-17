import sys
sys.path.append('/workspaces/Combo-Offer-Optimizer/')

from src.optimizer import ComboOfferOptimizer
import pandas as pd

# Sample Data
transactions = [
    ["Laptop", "Mouse", "Keyboard"],
    ["Smartphone", "Earphones"],
    ["Tablet", "Keyboard"],
]

product_hierarchy = pd.DataFrame({
    "ProductID": ["Laptop", "Mouse", "Keyboard", "Smartphone", "Earphones", "Tablet"],
    "Category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories", "Electronics"],
    "Subcategory": ["Computers", "Input Devices", "Input Devices", "Mobile", "Audio", "Tablets"]
})

product_prices = {"Laptop": 1000, "Mouse": 20, "Keyboard": 50, "Smartphone": 800, "Earphones": 150, "Tablet": 600}
inventory_levels = {"Laptop": 10, "Mouse": 200, "Keyboard": 150, "Smartphone": 50, "Earphones": 100, "Tablet": 60}
objectives = {"revenue_growth": 1, "inventory_clearance": 1, "category_growth": 0.5, "customer_retention": 0.5}

# Run Optimizer
optimizer = ComboOfferOptimizer(transactions, product_hierarchy, product_prices, inventory_levels, objectives)
optimized_combos = optimizer.optimize_all_levels()

# Print Results
print(optimized_combos)