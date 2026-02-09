import pandas as pd
import sqlite3


def load_and_clean_events():

    df = pd.read_csv("data/events.csv", nrows=3000)

    # To rename columns to match with system
    df = df.rename(columns={
        "visitorid": "user_id",
        "itemid": "product_id",
        "event": "action"
    })

    # Convert event names to our format

    df["action"] = df["action"].replace({
        "addtocart": "cart",
        "transaction": "purchase"
    })

 # Convert timestamp (milliseconds to readable datetime)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms').astype(str)

 # To keep only required columns
    df = df[["user_id", "product_id", "action", "timestamp"]]

    return df


def insert_into_database(df):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO interactions (user_id, product_id, action, timestamp) VALUES (?, ?, ?, ?)",
            (row["user_id"], row["product_id"], row["action"], row["timestamp"])
        )

    conn.commit()
    conn.close()

    print("Data inserted into interactions table")


if __name__ == "__main__":
    df = load_and_clean_events()
    insert_into_database(df)


