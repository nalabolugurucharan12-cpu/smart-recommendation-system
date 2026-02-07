from flask import Flask, render_template, request
from database import get_db_connection, create_users_table


app = Flask(__name__)

create_users_table()

# Home page
@app.route("/")
def home():
    return render_template("index.html")


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


if __name__ == "__main__":
    app.run(debug=True)

