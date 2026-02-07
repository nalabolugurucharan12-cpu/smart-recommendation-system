from flask import Flask, render_template, request

app = Flask(__name__)

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
        print("Username:", username)
        print("Password:", password)

        return "Login Successful (temporary response)"

    return render_template("login.html")


# Products page
@app.route("/products")
def products():
    return render_template("products.html")


if __name__ == "__main__":
    app.run(debug=True)

