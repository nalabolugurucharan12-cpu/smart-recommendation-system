import sqlite3

def get_popular_products(limit=5):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # To count interactions of every product 
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

if __name__ == "__main__":
    popular = get_popular_products()

    print("Popular Products:")
    for product in popular:
        print(product)
