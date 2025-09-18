from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user (for demo)
USER = {"username": "admin", "password": "12345"}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USER["username"] and password == USER["password"]:
            return "<h2>✅ Login Successful! Welcome {}</h2>".format(username)
        else:
            return "<h2>❌ Invalid Credentials</h2><a href='/'>Try Again</a>"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
