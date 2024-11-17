# Combo Offer Optimizer

This project contains an optimization model for generating combo offers based on customer transactions, product inventory, and retailer objectives (e.g., revenue growth, inventory clearance, category growth, and customer retention).

## Features
- Generate combo offers based on product pairings, category, and subcategory associations.
- Optimize combos using retailer objectives such as maximizing revenue, inventory clearance, and promoting underrepresented categories.
- Custom scoring function for prioritizing combos.

## Setup Instructions

### Prerequisites
- Python 3.7+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Usage
Run the example script to see the optimization in action:
```bash
python examples/run_optimizer.py
```

### Running the Optimizer
You can also create your own dataset and use the ComboOfferOptimizer class as follows:
```python
from src.optimizer import ComboOfferOptimizer

# Load your data
transactions = [...]
product_hierarchy = pd.DataFrame([...])
product_prices = {...}
inventory_levels = {...}

# Instantiate and run the optimizer
optimizer = ComboOfferOptimizer(transactions, product_hierarchy, product_prices, inventory_levels, retailer_objectives)
optimized_combos = optimizer.optimize_all_levels()

print(optimized_combos['Product'])
```

### License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/nayan4qmul/Combo-Offer-Optimizer/blob/main/LICENSE) file for details.
