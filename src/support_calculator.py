from collections import defaultdict
from itertools import combinations

def calculate_support(transactions, hierarchy):
    total_transactions = len(transactions)
    product_counts = defaultdict(int)
    subcategory_counts = defaultdict(int)
    category_counts = defaultdict(int)

    item_pairs = {
        "Product": defaultdict(lambda: {"count": 0, "support": 0.0}),
        "Subcategory": defaultdict(lambda: {"count": 0, "support": 0.0}),
        "Category": defaultdict(lambda: {"count": 0, "support": 0.0}),
    }

    for transaction in transactions:
        subcategories_in_transaction = set()
        categories_in_transaction = set()

        for product in transaction:
            product_counts[product] += 1
            category, subcategory = hierarchy.get(product, (None, None))
            if category:
                subcategories_in_transaction.add(subcategory)
                categories_in_transaction.add(category)

        for subcategory in subcategories_in_transaction:
            subcategory_counts[subcategory] += 1
        for category in categories_in_transaction:
            category_counts[category] += 1

        for level, items in [("Product", transaction), 
                             ("Subcategory", subcategories_in_transaction), 
                             ("Category", categories_in_transaction)]:
            for pair in combinations(items, 2):
                pair = tuple(sorted(pair))
                item_pairs[level][pair]["count"] += 1

    support = {
        "Product": {product: count / total_transactions for product, count in product_counts.items()},
        "Subcategory": {subcategory: count / total_transactions for subcategory, count in subcategory_counts.items()},
        "Category": {category: count / total_transactions for category, count in category_counts.items()},
    }

    for level in ["Product", "Subcategory", "Category"]:
        for pair, data in item_pairs[level].items():
            data["support"] = data["count"] / total_transactions

    return support, item_pairs