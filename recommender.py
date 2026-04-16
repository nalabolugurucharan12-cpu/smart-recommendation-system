import sqlite3
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


DB_NAME = "users.db"


def get_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT user_id, product_id, action, timestamp FROM interactions",
        conn
    )
    conn.close()
    return df


# ------------------ COLLABORATIVE ------------------

def collaborative_recommend(user_id, limit=10):

    df = get_data()

    if df.empty:
        return []

    # Clean timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # Assign weights
    weight_map = {
        "view": 1,
        "cart": 3,
        "purchase": 5
    }
    df["action_weight"] = df["action"].map(weight_map).fillna(1)

    # Recency weighting
    current_time = df["timestamp"].max()
    df["days_old"] = (current_time - df["timestamp"]).dt.days
    df["recency_weight"] = 1 / (1 + df["days_old"])

    df["final_weight"] = df["action_weight"] * df["recency_weight"]

    # Aggregate
    df_grouped = df.groupby(["user_id", "product_id"])["final_weight"].sum().reset_index()

    # Pivot matrix
    user_item = df_grouped.pivot(
        index="user_id",
        columns="product_id",
        values="final_weight"
    ).fillna(0)

    if user_id not in user_item.index:
        return []

    # Similarity
    similarity = cosine_similarity(user_item)
    similarity_df = pd.DataFrame(similarity, index=user_item.index, columns=user_item.index)

    # Get similar users
    similar_users = similarity_df[user_id].sort_values(ascending=False)[1:6].index

    # Get their products
    similar_products = df_grouped[df_grouped["user_id"].isin(similar_users)]

    product_scores = (
        similar_products.groupby("product_id")["final_weight"]
        .sum()
        .sort_values(ascending=False)
    )

    # Remove already seen
    seen = set(df[df["user_id"] == user_id]["product_id"])
    product_scores = product_scores[~product_scores.index.isin(seen)]

    return list(product_scores.head(limit).index)


# ------------------ POPULAR ------------------

def get_popular_products(limit=50):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, COUNT(*) as count
        FROM interactions
        GROUP BY product_id
        ORDER BY count DESC
        LIMIT ?
    """, (limit,))

    result = [r[0] for r in cursor.fetchall()]
    conn.close()

    return result


# ------------------ TRENDING ------------------

def get_trending_products(limit=50):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, COUNT(*) as count
        FROM interactions
        WHERE timestamp >= datetime('now', '-7 days')
        GROUP BY product_id
        ORDER BY count DESC
        LIMIT ?
    """, (limit,))

    result = [r[0] for r in cursor.fetchall()]
    conn.close()

    return result


# ------------------ CONTENT BASED ------------------

def get_user_recommendations(user_id, limit=10):

    conn = sqlite3.connect(DB_NAME)
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
        SELECT product_id
        FROM products
        WHERE category IN ({','.join(['?']*len(categories))})
        LIMIT ?
    """

    cursor.execute(query, (*categories, limit))
    result = [r[0] for r in cursor.fetchall()]

    conn.close()
    return result


# ------------------ FINAL HYBRID ------------------

def hybrid_recommend(user_id, limit=30):

    collab = collaborative_recommend(user_id, 15)
    content = get_user_recommendations(user_id, 15)
    trending = get_trending_products(20)
    popular = get_popular_products(20)

    # Cold start
    if not collab and not content:
        combined = trending + popular
    else:
        combined = collab + content + trending + popular

    # Remove duplicates
    combined = list(dict.fromkeys(combined))

    return get_product_details(combined[:limit])


# ------------------ PRODUCT DETAILS ------------------

def get_product_details(product_ids):

    if not product_ids:
        return []

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = f"""
        SELECT product_id, category
        FROM products
        WHERE product_id IN ({','.join(['?']*len(product_ids))})
    """

    cursor.execute(query, product_ids)
    rows = cursor.fetchall()
    conn.close()

    category_map = {r[0]: r[1] for r in rows}

    return [
        {
            "product_id": pid,
            "category": category_map.get(pid, "Unknown")
        }
        for pid in product_ids
    ]