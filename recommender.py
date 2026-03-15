import sqlite3


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


