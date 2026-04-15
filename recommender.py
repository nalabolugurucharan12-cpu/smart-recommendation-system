import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def collaborative_recommend(user_id, limit=5):

    conn = sqlite3.connect("users.db")

    df = pd.read_sql_query(
        "SELECT user_id, product_id, action, timestamp FROM interactions",
        conn
    )
    conn.close()

    if df.empty:
        return []

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    weight_map = {
        "view": 1,
        "cart": 3,
        "purchase": 5
    }

    df["action_weight"] = df["action"].map(weight_map)

    current_time = df["timestamp"].max()
    df["days_old"] = (current_time - df["timestamp"]).dt.days

    df["recency_weight"] = 1 / (1 + df["days_old"])
    df["final_weight"] = df["action_weight"] * df["recency_weight"]

    df_grouped = df.groupby(["user_id", "product_id"])["final_weight"].sum().reset_index()

    user_item = df_grouped.pivot(
        index="user_id",
        columns="product_id",
        values="final_weight"
    ).fillna(0)

    if user_id not in user_item.index:
        return []

    similarity = cosine_similarity(user_item)

    similarity_df = pd.DataFrame(
        similarity,
        index=user_item.index,
        columns=user_item.index
    )

    similar_users = similarity_df[user_id].sort_values(ascending=False)[1:6]
    similar_user_ids = similar_users.index

    similar_products = df_grouped[df_grouped["user_id"].isin(similar_user_ids)]

    product_scores = (
        similar_products.groupby("product_id")["final_weight"]
        .sum()
        .sort_values(ascending=False)
    )

    # REMOVE ALREADY SEEN PRODUCTS
    seen_products = set(df[df["user_id"] == user_id]["product_id"])
    product_scores = product_scores[~product_scores.index.isin(seen_products)]

    return list(product_scores.head(limit).index)


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


#  HYBRID RECOMMENDE
def hybrid_recommend(user_id, limit=5):

    collab = collaborative_recommend(user_id, limit=10)
    content = [p[0] for p in get_user_recommendations(user_id, limit=10)]
    trending = [p[0] for p in get_trending_products(limit=10)]
    popular = [p[0] for p in get_popular_products(limit=10)]

    #  COLD START HANDLING
    if not collab and not content:
        # Try trending first
        if trending:
            return trending[:limit]
        # Final fallback
        return popular[:limit]

    # Combine all
    combined = collab + content + trending + popular

    # Remove duplicates while preserving order
    seen = set()
    final = []

    for p in combined:
        if p not in seen:
            seen.add(p)
            final.append(p)

        if len(final) == limit:
            break

    return final