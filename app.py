from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import (
    get_db_connection,
    create_users_table,
    create_products_table,
    create_interactions_table
)
from recommender import (
    get_trending_products,
    get_popular_products,
    get_user_recommendations,
    collaborative_recommend,
    hybrid_recommend,
    get_product_details
)

app = Flask(__name__)
app.secret_key = "secret123"


# Initialize DB
create_users_table()
create_products_table()
create_interactions_table()


@app.route("/")
def home():
    return render_template("index.html")


# ---------------- AUTH ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            return redirect(url_for("products"))
        else:
            return "Invalid Credentials"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# ---------------- PRODUCTS ----------------

@app.route("/products")
def products():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("products.html")


@app.route("/products/list")
def list_products():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT product_id, category FROM products LIMIT 100")
    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"product_id": r["product_id"], "category": r["category"]}
        for r in rows
    ])


# ---------------- INTERACTIONS ----------------

@app.route("/interact/<int:product_id>/<action>")
def interact(product_id, action):

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Login required"})

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO interactions (user_id, product_id, action) VALUES (?, ?, ?)",
        (user_id, product_id, action)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": f"{action} recorded"})


# ---------------- RECOMMENDATIONS ----------------

@app.route("/recommend/popular")
def recommend_popular():
    products = get_popular_products()
    return jsonify(get_product_details(products))


@app.route("/recommend/trending")
def recommend_trending():
    products = get_trending_products()
    return jsonify(get_product_details(products))


@app.route("/recommend/user")
def recommend_user():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify([])

    products = get_user_recommendations(user_id)
    return jsonify(get_product_details(products))


@app.route("/recommend/collaborative")
def recommend_collaborative():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify([])

    products = collaborative_recommend(user_id)
    return jsonify(get_product_details(products))


@app.route("/recommend/hybrid")
def recommend_hybrid():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify([])

    return jsonify(hybrid_recommend(user_id))


# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)