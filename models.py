import pandas as pd


def extract_product_categories(product_ids):

    categories = []

    files = [
        "data/item_properties_part1.csv",
        "data/item_properties_part2.csv"
    ]

    product_ids = set(product_ids)

    for file in files:

        for chunk in pd.read_csv(file, chunksize=100000):

            # Keep only category rows
            chunk = chunk[chunk["property"] == "categoryid"]

            # Filter only required products
            chunk = chunk[chunk["itemid"].isin(product_ids)]

            if chunk.empty:
                continue

            # Select required columns
            chunk = chunk[["itemid", "value"]]

            # Rename
            chunk = chunk.rename(columns={
                "itemid": "product_id",
                "value": "category"
            })

            categories.append(chunk)

    if not categories:
        return pd.DataFrame(columns=["product_id", "category"])

    category_df = pd.concat(categories)

    # Remove duplicates (keep latest)
    category_df = category_df.drop_duplicates(subset="product_id", keep="last")

    print(f"Extracted {len(category_df)} product categories")

    return category_df