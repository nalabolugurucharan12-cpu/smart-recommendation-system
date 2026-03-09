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


if __name__ == "__main__":

    print("Popular products:")
    print(get_popular_products())

    print("\nTrending products:")
    print(get_trending_products())

