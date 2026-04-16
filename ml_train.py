import pandas as pd
import sqlite3
from models import extract_product_categories

DB_NAME = "users.db"


# ---------------- LOAD DATA ----------------

def load_and_clean_events():

    df = pd.read_csv("data/events.csv", nrows=5000)

    df = df.rename(columns={
        "visitorid": "user_id",
        "itemid": "product_id",
        "event": "action"
    })

    df["action"] = df["action"].replace({
        "addtocart": "cart",
        "transaction": "purchase"
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    df = df[["user_id", "product_id", "action", "timestamp"]]

    return df


# ---------------- INSERT USERS ----------------

def insert_users(df):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    users = df["user_id"].drop_duplicates().tolist()

    cursor.executemany(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (?, ?, ?)",
        [(uid, f"user_{uid}", "pass123") for uid in users]
    )

    conn.commit()
    conn.close()

    print(f"Inserted {len(users)} users")


# ---------------- INSERT INTERACTIONS ----------------

def insert_interactions(df):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    data = df.to_records(index=False)

    cursor.executemany("""
        INSERT INTO interactions (user_id, product_id, action, timestamp)
        VALUES (?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()

    print(f"Inserted {len(df)} interactions")


# ---------------- GET PRODUCT IDS ----------------

def get_product_ids():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT product_id FROM interactions")

    product_ids = [row[0] for row in cursor.fetchall()]

    conn.close()

    print(f"Total products: {len(product_ids)}")

    return product_ids


# ---------------- INSERT PRODUCTS ----------------

def insert_products(df):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    data = df.to_records(index=False)

    cursor.executemany("""
        INSERT OR IGNORE INTO products (product_id, category)
        VALUES (?, ?)
    """, data)

    conn.commit()
    conn.close()

    print(f"Inserted {len(df)} products")


# ---------------- MAIN PIPELINE ----------------

if __name__ == "__main__":

    print("🚀 Starting ML pipeline...")

    # Load data
    events_df = load_and_clean_events()

    # Insert users first (important!)
    insert_users(events_df)

    # Insert interactions
    insert_interactions(events_df)

    # Get product IDs
    product_ids = get_product_ids()

    # Extract categories
    category_df = extract_product_categories(product_ids)

    # Insert products
    insert_products(category_df)

    print("✅ Data pipeline completed successfully!")