import pandas as pd
import sqlite3
from models import extract_product_categories


def load_and_clean_events():

    df = pd.read_csv("data/events.csv", nrows=3000)

    # Rename columns
    df = df.rename(columns={
        "visitorid": "user_id",
        "itemid": "product_id",
        "event": "action"
    })

    # Convert event names
    df["action"] = df["action"].replace({
        "addtocart": "cart",
        "transaction": "purchase"
    })

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms").astype(str)

    # Keep required columns
    df = df[["user_id", "product_id", "action", "timestamp"]]

    return df


def insert_interactions(df):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT INTO interactions (user_id, product_id, action, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (row["user_id"], row["product_id"], row["action"], row["timestamp"])
        )

    conn.commit()
    conn.close()

    print("Interactions inserted")


def get_interaction_product_ids():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT product_id FROM interactions")

    product_ids = [row[0] for row in cursor.fetchall()]

    conn.close()

    print("Total products in interactions:", len(product_ids))

    return set(product_ids)


def insert_products(df):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    for _, row in df.iterrows():

        cursor.execute(
            """
            INSERT OR IGNORE INTO products (product_id, category)
            VALUES (?, ?)
            """,
            (row["product_id"], row["category"])
        )

    conn.commit()
    conn.close()

    print("Products inserted")


if __name__ == "__main__":

    #load interactions
    events_df = load_and_clean_events()

    #insert interactions
    insert_interactions(events_df)

    #get product IDs
    product_ids = get_interaction_product_ids()

    # extract categories
    category_df = extract_product_categories(product_ids)

    #insert products
    insert_products(category_df)

