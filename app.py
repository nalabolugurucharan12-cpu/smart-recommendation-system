from flask import Flask, render_template, request
from database import get_db_connection, create_users_table, create_products_table, create_interactions_table
from recommender import get_popular_products



app = Flask(__name__)

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
        # To get data from login form
        username = request.form.get("username")
        password = request.form.get("password")
        conn = get_db_connection()
        cursor = conn.cursor()

        # To check if user exists
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

@app.route("/products")
def products():
    return render_template("products.html")


#sample-products route to add sample products to the database
@app.route("/add-sample-products")
def add_sample_products():

    conn = get_db_connection()
    cursor = conn.cursor()
    
    products = [
        ("iPhone 13", "Electronics", 70000),
        ("Running Shoes", "Sports", 3000),
        ("Laptop", "Electronics", 60000),
        ("T-shirt", "Clothing", 800),
        ("Headphones", "Electronics", 2500)
    ]

    cursor.executemany(
        "INSERT INTO products (name, category, price) VALUES (?, ?, ?)",
        products
    )

    conn.commit()
    conn.close()

    return "Sample products added successfully!"

@app.route("/interact/<int:product_id>/<action>")
def record_interaction(product_id, action):

    # Temporary user_id 
    user_id = 1  

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

    return str(products)




if __name__ == "__main__":
    app.run(debug=True)

