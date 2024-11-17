import pandas as pd
import random

# Define products, categories, and subcategories
products = ["Laptop", "Mouse", "Keyboard", "Smartphone", "Earphones", "Tablet", "Camera", "Speaker", "Charger", "Smartwatch"]
categories = ["Electronics", "Accessories", "Furniture", "Clothing"]
subcategories = {
    "Electronics": ["Computers", "Mobile", "Audio", "Tablets", "Cameras"],
    "Accessories": ["Input Devices", "Chargers", "Wearables"],
    "Furniture": ["Living Room", "Bedroom", "Office"],
    "Clothing": ["Men", "Women", "Kids"]
}

# Generate synthetic product hierarchy
product_hierarchy_data = []
for product in products:
    category = random.choice(categories)
    subcategory = random.choice(subcategories[category])
    product_hierarchy_data.append({"ProductID": product, "Category": category, "Subcategory": subcategory})

product_hierarchy_df = pd.DataFrame(product_hierarchy_data)

# Save product hierarchy to CSV
product_hierarchy_df.to_csv("synthetic_product_hierarchy.csv", index=False)

# Generate synthetic transactions
transactions = []
for _ in range(1000):  # Generating 1000 transactions
    num_items = random.randint(1, 5)
    transaction = random.sample(products, num_items)
    transactions.append(transaction)

# Save transactions to CSV
transactions_df = pd.DataFrame({"TransactionID": range(1, len(transactions) + 1), "Products": transactions})
transactions_df.to_csv("synthetic_transactions.csv", index=False)

print("Synthetic data generated successfully.")