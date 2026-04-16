import sqlite3

DB_NAME = "users.db"


def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- USERS ----------------

def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- PRODUCTS ----------------

def create_products_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            category TEXT
        )
    """)

    conn.commit()

    # 🔥 IMPORTANT: index for fast recommendation queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product_id ON products(product_id)")

    conn.commit()
    conn.close()


# ---------------- INTERACTIONS ----------------

def create_interactions_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            product_id INTEGER,
            action TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        )
    """)

    # 🔥 Indexes (VERY IMPORTANT for ML + queries)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user ON interactions(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_product ON interactions(product_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_time ON interactions(timestamp)")

    conn.commit()
    conn.close()