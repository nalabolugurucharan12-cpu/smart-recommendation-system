import pandas as pd


def extract_product_categories(product_ids):

    categories = []

    files = [
        "data/item_properties_part1.csv",
        "data/item_properties_part2.csv"
    ]

    for file in files:

        # Read large files in chunks
        for chunk in pd.read_csv(file, chunksize=100000):

            # Keep only category rows
            chunk = chunk[chunk["property"] == "categoryid"]

            # Keep only products that appear in interactions
            chunk = chunk[chunk["itemid"].isin(product_ids)]

            # Keep relevant columns
            chunk = chunk[["itemid", "value"]]

            # Rename columns
            chunk = chunk.rename(columns={
                "itemid": "product_id",
                "value": "category"
            })

            categories.append(chunk)

    category_df = pd.concat(categories)

    # Remove duplicates
    category_df = category_df.drop_duplicates(subset="product_id")

    print("Extracted categories:")
    print(category_df.head())

    return category_df

