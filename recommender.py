import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def collaborative_recommend(user_id, limit=5):

    conn = sqlite3.connect("users.db")

    df = pd.read_sql_query(
        "SELECT user_id, product_id, action FROM interactions",
        conn
    )

    conn.close()

    # Assign weights
    weight_map = {
        "view": 1,
        "cart": 3,
        "purchase": 5
    }

    df["weight"] = df["action"].map(weight_map)

    # Aggregate weights per user-product
    df_grouped = df.groupby(["user_id", "product_id"])["weight"].sum().reset_index()

    # Create weighted matrix
    user_item = df_grouped.pivot(
        index="user_id",
        columns="product_id",
        values="weight"
    ).fillna(0)

    if user_id not in user_item.index:
        return []

    # Compute similarity
    similarity = cosine_similarity(user_item)

    similarity_df = pd.DataFrame(
        similarity,
        index=user_item.index,
        columns=user_item.index
    )

    # Get similar users
    similar_users = similarity_df[user_id].sort_values(ascending=False)[1:6]

    similar_user_ids = similar_users.index

    # Get products from similar users
    similar_products = df_grouped[df_grouped["user_id"].isin(similar_user_ids)]

    product_scores = (
        similar_products.groupby("product_id")["weight"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )

    return list(product_scores.index)


def get_popular_products(limit=5):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, COUNT(*) as interaction_count
        FROM interactions
        GROUP BY product_id
        ORDER BY interaction_count DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()

    return results


def get_trending_products(limit=5):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, COUNT(*) as interaction_count
        FROM interactions
        WHERE timestamp >= datetime('now', '-7 days')
        GROUP BY product_id
        ORDER BY interaction_count DESC
        LIMIT ?
    """, (limit,))

    results = cursor.fetchall()
    conn.close()

    return results


def get_user_recommendations(user_id, limit=5):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Find categories user interacted with
    cursor.execute("""
        SELECT DISTINCT p.category
        FROM interactions i
        JOIN products p ON i.product_id = p.product_id
        WHERE i.user_id = ?
    """, (user_id,))

    categories = [row[0] for row in cursor.fetchall()]

    if not categories:
        conn.close()
        return []

    # Recommend products from same categories
    query = f"""
        SELECT product_id, category
        FROM products
        WHERE category IN ({','.join(['?']*len(categories))})
        LIMIT ?
    """

    cursor.execute(query, (*categories, limit))

    results = cursor.fetchall()
    conn.close()

    return results


if __name__ == "__main__":

    print("Popular products:")
    print(get_popular_products())

    print("\nTrending products:")
    print(get_trending_products())

    print("\nUser recommendations for user 1:")
    print(get_user_recommendations(1))


