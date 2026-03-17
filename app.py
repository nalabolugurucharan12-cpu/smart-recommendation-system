from flask import Flask, render_template, request
from database import get_db_connection, create_users_table, create_products_table, create_interactions_table
from recommender import get_trending_products, get_popular_products, get_user_recommendations, collaborative_recommend

app = Flask(__name__)

# Initialize tables
create_users_table()
create_products_table()
create_interactions_table()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Login route
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
            return "Login Successful"
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# Registration route
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


# Products page
@app.route("/products")
def products():
    return render_template("products.html")


# Record interaction
@app.route("/interact/<int:product_id>/<action>")
def record_interaction(product_id, action):

    user_id = 1  # temporary user

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO interactions (user_id, product_id, action) VALUES (?, ?, ?)",
        (user_id, product_id, action)
    )

    conn.commit()
    conn.close()

    return f"Recorded {action} for product {product_id}"


# Popular recommendations
@app.route("/recommend/popular")
def recommend_popular():

    products = get_popular_products()
    return str(products)


# Trending recommendations
@app.route("/recommend/trending")
def recommend_trending():

    products = get_trending_products()
    return str(products)

# User based recommendations
@app.route("/recommend/user/<int:user_id>")
def recommend_user(user_id):

    products = get_user_recommendations(user_id)

    return str(products)

# Collaborative filtering recommendations
@app.route("/recommend/collaborative/<int:user_id>")
def recommend_collaborative(user_id):

    products = collaborative_recommend(user_id)

    return str(products)


if __name__ == "__main__":
    app.run(debug=True)