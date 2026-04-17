import os
import shutil
import sqlite3
import tempfile
from urllib.parse import urlparse

ROOT_DIR = os.path.dirname(__file__)
ROOT_DB_NAME = os.path.join(ROOT_DIR, "users.db")
DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_path():
    if DATABASE_URL:
        parsed = urlparse(DATABASE_URL)
        if parsed.scheme in ("sqlite", "sqlite3"):
            db_path = parsed.path or ""
            if os.name == "nt" and db_path.startswith("/") and len(db_path) > 2 and db_path[2] == ":":
                db_path = db_path[1:]
            return os.path.abspath(db_path) if db_path else ROOT_DB_NAME

    if os.environ.get("VERCEL") or not os.access(ROOT_DIR, os.W_OK):
        tmp_dir = os.path.join(tempfile.gettempdir(), "smart-recommendation-system")
        os.makedirs(tmp_dir, exist_ok=True)
        tmp_db = os.path.join(tmp_dir, "users.db")

        if not os.path.exists(tmp_db) and os.path.exists(ROOT_DB_NAME):
            shutil.copy2(ROOT_DB_NAME, tmp_db)

        return tmp_db

    return ROOT_DB_NAME


DB_NAME = get_db_path()


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