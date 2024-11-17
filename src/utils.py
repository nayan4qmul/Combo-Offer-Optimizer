import pandas as pd

def load_product_hierarchy(file_path):
    return pd.read_csv(file_path)

def load_transactions(file_path):
    return pd.read_csv(file_path).values.tolist()

def map_to_hierarchy(product_id, hierarchy_df):
    row = hierarchy_df[hierarchy_df['ProductID'] == product_id]
    if not row.empty:
        return row.iloc[0]['Category'], row.iloc[0]['Subcategory']
    return None, None