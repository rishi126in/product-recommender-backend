import pandas as pd

# Load CSV once
df = pd.read_csv("products.csv")  # Make sure file is in project root

def get_products():
    return df.to_dict(orient="records")
