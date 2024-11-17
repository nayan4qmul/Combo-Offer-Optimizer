from itertools import combinations
from collections import defaultdict
import numpy as np
import pandas as pd

class ComboOfferOptimizer:
    def __init__(self, transactions, product_hierarchy, product_prices, inventory_levels, retailer_objectives):
        """
        Initialize the optimizer with required data.

        :param transactions: List of transactions, where each transaction is a list of product IDs.
        :param product_hierarchy: DataFrame with columns ['ProductID', 'Category', 'Subcategory'].
        :param product_prices: Dictionary with product prices {ProductID: Price}.
        :param inventory_levels: Dictionary with product inventory {ProductID: StockLevel}.
        :param retailer_objectives: Dictionary with objectives and weights.
        """
        self.transactions = transactions
        self.product_hierarchy = product_hierarchy.set_index('ProductID')
        self.product_prices = product_prices
        self.inventory_levels = inventory_levels
        self.objectives = retailer_objectives
        self.support = {"Product": defaultdict(float), "Subcategory": defaultdict(float), "Category": defaultdict(float)}
        self.item_pairs = {
            "Product": defaultdict(lambda: {"count": 0, "support": 0.0}),
            "Subcategory": defaultdict(lambda: {"count": 0, "support": 0.0}),
            "Category": defaultdict(lambda: {"count": 0, "support": 0.0}),
        }
        self.total_transactions = len(transactions)

    def _map_hierarchy(self, product_id):
        """
        Map a product to its category and subcategory using the hierarchy.
        """
        if product_id in self.product_hierarchy.index:
            row = self.product_hierarchy.loc[product_id]
            return row['Category'], row['Subcategory']
        else:
            return None, None

    def calculate_support(self):
        """Calculate the support for individual products, subcategories, and categories."""
        product_counts = defaultdict(int)
        subcategory_counts = defaultdict(int)
        category_counts = defaultdict(int)

        for transaction in self.transactions:
            # Track which categories and subcategories are in this transaction
            subcategories_in_transaction = set()
            categories_in_transaction = set()

            for product in transaction:
                product_counts[product] += 1
                category, subcategory = self._map_hierarchy(product)
                if category:
                    subcategories_in_transaction.add(subcategory)
                    categories_in_transaction.add(category)

            # Increment counts for subcategories and categories
            for subcategory in subcategories_in_transaction:
                subcategory_counts[subcategory] += 1
            for category in categories_in_transaction:
                category_counts[category] += 1

            # Count pairs of items, subcategories, and categories
            for level, items in [("Product", transaction),
                                 ("Subcategory", subcategories_in_transaction),
                                 ("Category", categories_in_transaction)]:
                for pair in combinations(items, 2):
                    pair = tuple(sorted(pair))
                    self.item_pairs[level][pair]["count"] += 1

        # Calculate support
        for product, count in product_counts.items():
            self.support["Product"][product] = count / self.total_transactions

        for subcategory, count in subcategory_counts.items():
            self.support["Subcategory"][subcategory] = count / self.total_transactions

        for category, count in category_counts.items():
            self.support["Category"][category] = count / self.total_transactions

        for level in ["Product", "Subcategory", "Category"]:
            for pair, data in self.item_pairs[level].items():
                data["support"] = data["count"] / self.total_transactions

    def calculate_lift(self, level):
        """Calculate lift for each pair of items in the specified level."""
        for pair, data in self.item_pairs[level].items():
            item_x, item_y = pair
            if self.support[level][item_x] > 0 and self.support[level][item_y] > 0:
                data["lift"] = data["support"] / (
                    self.support[level][item_x] * self.support[level][item_y]
                )
            else:
                data["lift"] = 0.0

    def generate_combo_candidates(self, level):
        """Generate a DataFrame of combo candidates for a specific level (Product, Subcategory, or Category)."""
        combo_data = []
        for pair, data in self.item_pairs[level].items():
            combo_data.append({
                f"{level}_X": pair[0],
                f"{level}_Y": pair[1],
                "Support_X": self.support[level][pair[0]],
                "Support_Y": self.support[level][pair[1]],
                "Support_XY": data["support"],
                "Lift": data["lift"]
            })

        return pd.DataFrame(combo_data)

    def score_combos(self, combo_df, level):
        """
        Score combos based on retailer objectives.

        :param combo_df: DataFrame with combo candidate metrics.
        :param level: Product, Subcategory, or Category.
        :return: Scored DataFrame sorted by score.
        """
        # Add pricing and inventory details
        if level == "Product":
            combo_df["Price_X"] = combo_df[f"{level}_X"].map(self.product_prices)
            combo_df["Price_Y"] = combo_df[f"{level}_Y"].map(self.product_prices)
            combo_df["Inventory_X"] = combo_df[f"{level}_X"].map(self.inventory_levels)
            combo_df["Inventory_Y"] = combo_df[f"{level}_Y"].map(self.inventory_levels)

        # Revenue growth: prioritize high-value combos
        combo_df["Basket_Value"] = combo_df.get("Price_X", 0) + combo_df.get("Price_Y", 0)
        revenue_score = self.objectives.get("revenue_growth", 0) * combo_df["Basket_Value"]

        # Inventory clearance: prioritize overstocked products
        combo_df["Overstock_Factor"] = combo_df.get("Inventory_Y", 0) / (combo_df.get("Inventory_X", 1) + 1)
        inventory_score = self.objectives.get("inventory_clearance", 0) * combo_df["Overstock_Factor"]

        # Category growth: boost scores for less-purchased categories
        if level in ["Category", "Subcategory"]:
            combo_df["Category_Boost"] = combo_df[f"{level}_X"].map(self.support[level]) + \
                                          combo_df[f"{level}_Y"].map(self.support[level])
            category_score = self.objectives.get("category_growth", 0) / (1 + combo_df["Category_Boost"])
        else:
            category_score = 0

        # Customer retention: boost combos aligned with preferences (mocked for simplicity)
        combo_df["Customer_Preference_Score"] = np.random.rand(len(combo_df))  # Replace with actual preference data
        retention_score = self.objectives.get("customer_retention", 0) * combo_df["Customer_Preference_Score"]

        # Total Score
        combo_df["Score"] = (
            revenue_score +
            inventory_score +
            category_score +
            retention_score +
            self.objectives.get("lift", 0) * combo_df["Lift"]
        )

        return combo_df.sort_values(by="Score", ascending=False)

    def optimize_combos(self, level="Product"):
        """
        End-to-end method to optimize combo offers for a specific level.

        :param level: Specify 'Product', 'Subcategory', or 'Category'.
        :return: DataFrame of ranked combo offers for the chosen level.
        """
        self.calculate_support()
        self.calculate_lift(level)
        combo_candidates = self.generate_combo_candidates(level)
        return self.score_combos(combo_candidates, level)

    def optimize_all_levels(self):
        """
        Optimize combos at all levels (Product, Subcategory, Category).

        :return: Dictionary of DataFrames for each level.
        """
        results = {}
        for level in ["Product", "Subcategory", "Category"]:
            results[level] = self.optimize_combos(level)
        return results