from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database import get_db_connection, create_users_table, create_products_table, create_interactions_table
from recommender import get_trending_products, get_popular_products, get_user_recommendations,collaborative_recommend, hybrid_recommend


app = Flask(__name__)
app.secret_key = "secret123"  # For session management, in production use a secure key

# Initialize tables
create_users_table()
create_products_table()
create_interactions_table()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
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

        return "User Registered Successfully"

    return render_template("register.html")


@app.route("/products")
def products():
    return render_template("products.html")


@app.route("/interact/<int:product_id>/<action>")
def record_interaction(product_id, action):

    user_id = 1  # temporary

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO interactions (user_id, product_id, action) VALUES (?, ?, ?)",
        (user_id, product_id, action)
    )

    conn.commit()
    conn.close()

    return f"Recorded {action} for product {product_id}"


@app.route("/recommend/popular")
def recommend_popular():
    products = get_popular_products()
    return jsonify(products)


@app.route("/recommend/trending")
def recommend_trending():
    products = get_trending_products()
    return jsonify(products)


@app.route("/recommend/user/<int:user_id>")
def recommend_user(user_id):
    products = get_user_recommendations(user_id)
    return jsonify(products)


@app.route("/recommend/collaborative/<int:user_id>")
def recommend_collaborative(user_id):
    products = collaborative_recommend(user_id)
    return jsonify(products)


@app.route("/recommend/hybrid")
def recommend_hybrid_logged_in():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "User not logged in"})

    products = hybrid_recommend(user_id)
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)