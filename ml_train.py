import pandas as pd


def load_and_clean_events():

    # Load small portion
    df = pd.read_csv(".gitignore/Project_dataset/events.csv", nrows=3000)

    print("Original Data:")
    print(df.head())

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

    # Convert timestamp (milliseconds → readable datetime)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')

    # To keep only required columns
    df = df[["user_id", "product_id", "action", "timestamp"]]

    print("\nCleaned Data:")
    print(df.head())

    return df


if __name__ == "__main__":
    load_and_clean_events()

