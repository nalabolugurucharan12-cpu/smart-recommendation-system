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

import sqlite3


def get_trending_products(limit=5):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(timestamp) FROM interactions")
    latest_time = cursor.fetchone()[0]

    cursor.execute("""
        SELECT product_id, COUNT(*) as interaction_count
        FROM interactions
        WHERE timestamp >= datetime(?, '-7 days')
        GROUP BY product_id
        ORDER BY interaction_count DESC
        LIMIT ?
    """, (latest_time, limit))

    results = cursor.fetchall()
    conn.close()

    return results


