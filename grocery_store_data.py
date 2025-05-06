from google.cloud import bigquery
import os
import random
from datetime import datetime, timedelta
import json
import pandas as pd
from dotenv import load_dotenv  # Import dotenv

# Load environment variables from .env file
load_dotenv()

# CONFIGURATION
PROJECT_ID = os.getenv('PROJECT_ID')  # Load from .env
DATASET_ID = os.getenv('DATASET_ID')  # Load from .env

# Set Google Application Credentials
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # Load from .env
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

client = bigquery.Client()

# Table IDs
table_ids = {
    "foot_traffic": 'farmer-zack-dashboard.Farmer_Zack_Grocery_Data.foot_traffic',
    "products": 'farmer-zack-dashboard.Farmer_Zack_Grocery_Data.products',
    "stores": 'farmer-zack-dashboard.Farmer_Zack_Grocery_Data.stores',
    "transactions": 'farmer-zack-dashboard.Farmer_Zack_Grocery_Data.transactions'
}

# Clear all tables before inserting new data
for table_name, table_id in table_ids.items():
    delete_query = f"DELETE FROM `{table_id}` WHERE TRUE"
    client.query(delete_query).result()  # Executes the delete query and waits for completion
    print(f"Cleared table: {table_name}")

def create_data():
    # --- STORES ---
    stores = [
        {"store_id": 313, "location": "Detroit"},
        {"store_id": 586, "location": "Warren"},
        {"store_id": 248, "location": "Ferndale"}
    ]

    # --- PRODUCTS ---
    categories = ['Dairy', 'Bakery', 'Produce', 'Meat', 'Beverages']
    products = [{
            'product_id': i,
            'name': f"Product {i}",
            'category': random.choice(categories)
        } for i in range(1, 21)]

    # --- FOOT TRAFFIC ---
    foot_traffic = []
    start_date = datetime(2025, 1, 1)
    for day in range(125):  # 3 months
        date = start_date + timedelta(days=day)
        for store in stores:
            visitor_count = random.randint(100, 500)
            foot_traffic.append({
                'store_id': store['store_id'],
                'date': date.strftime('%Y-%m-%d'),
                'visitor_count': visitor_count
            })

    # --- TRANSACTIONS ---
    transactions = []
    transaction_id = 1
    for entry in foot_traffic:
        # Correlate number of transactions with visitor count
        num_transactions = max(1, entry['visitor_count'] // 10) 
        for _ in range(num_transactions):
            list_price = round(random.uniform(5.0, 25.0), 2) 
            price = round(list_price * random.uniform(0.7, 1.0), 2)  
            transactions.append({
                'transaction_id': transaction_id,
                'store_id': entry['store_id'],
                'product_id': random.choice(products)['product_id'],
                'date': entry['date'],
                'quantity': random.randint(1, 5),
                'list_price': list_price,
                'price': price
            })
            transaction_id += 1
    print(f"Generated {len(transactions)} transactions.")

    return (
            pd.DataFrame(stores),
            pd.DataFrame(products),
            pd.DataFrame(foot_traffic),
            pd.DataFrame(transactions)
        )

def load_to_bigquery(df, table_name):
    # Convert 'date' columns to datetime if they exist
    for column in df.columns:
        if 'date' in column.lower():
            df[column] = pd.to_datetime(df[column])

    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    print(f"Uploaded to {table_id} ({len(df)} rows)")

def clear_dataframes():
    """Clears the DataFrames by resetting them to empty DataFrames."""
    global stores_df, products_df, traffic_df, transactions_df
    stores_df = pd.DataFrame()
    products_df = pd.DataFrame()
    traffic_df = pd.DataFrame()
    transactions_df = pd.DataFrame()
    print("All DataFrames have been cleared.")

def main():
    print("Clearing existing data...")
    clear_dataframes()  # Clear DataFrames before generating new data

    print("Generating dummy grocery store data...")
    stores_df, products_df, traffic_df, transactions_df = create_data()

    print("Uploading data to BigQuery...")
    load_to_bigquery(stores_df, 'stores')
    load_to_bigquery(products_df, 'products')
    load_to_bigquery(traffic_df, 'foot_traffic')
    load_to_bigquery(transactions_df, 'transactions')

    print("All tables uploaded successfully.")

if __name__ == '__main__':
    main()
