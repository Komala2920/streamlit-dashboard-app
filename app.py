from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Simple in-memory database
users = {"admin": "12345"}

# ---------------- Home / Login Page ----------------
@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>B-Techno | Login</title>
      <style>
        body {
          background: linear-gradient(135deg, #2a5298, #1e3c72);
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
          font-family: "Segoe UI", sans-serif;
        }
        .container {
          width: 900px;
          height: 600px;
          background: #fff;
          border-radius: 14px;
          display: flex;
          overflow: hidden;
          box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .signin-container {
          width: 40%;
          background: linear-gradient(135deg, #2a5298, #1e3c72);
          color: #fff;
          padding: 40px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .signin-container h2 {text-align: center; margin-bottom: 20px;}
        .signin-container input {
          margin: 10px 0;
          padding: 12px;
          border: none;
          border-radius: 8px;
          width: 100%;
        }
        .btn {
          padding: 12px;
          background: #46c7c7;
          color: #fff;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          transition: 0.3s;
          width: 100%;
        }
        .btn:hover {background: #37a3a3;}
        .illustration-container {
          width: 60%;
          text-align: center;
          padding: 50px;
        }
        .illustration-container img {width: 80%; margin-bottom: 20px;}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="signin-container">
          <h2>Sign In</h2>
          <form action="/login" method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button class="btn" type="submit">Sign In</button>
          </form>

          <p style="margin-top:20px;text-align:center;">Don’t have an account?</p>
          <form action="/signup" method="POST">
            <input type="text" name="username" placeholder="New Username" required>
            <input type="password" name="password" placeholder="New Password" required>
            <button class="btn" type="submit">Sign Up</button>
          </form>
        </div>

        <div class="illustration-container">
          <img src="https://i.ibb.co/6tL9pQz/software-illustration.png" alt="Illustration">
          <h3>Technical Analysis of Software Requirements</h3>
          <p>Curabitur sed lectus in dui consectetur rhoncus sit amet nec sapien.</p>
        </div>
      </div>
    </body>
    </html>
    """)

# ---------------- Login Logic ----------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in users and users[username] == password:
        session["user"] = username
        return redirect(url_for("dashboard"))
    return "Invalid credentials. <a href='/'>Try again</a>"

# ---------------- Signup Logic ----------------
@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]

    if username in users:
        return "User already exists. <a href='/'>Try again</a>"
    users[username] = password
    return redirect(url_for("home"))

# ---------------- Dashboard Page ----------------
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template_string("""
        <html>
        <head>
          <title>Dashboard</title>
          <style>
            body {
              background: #f4f6f8;
              font-family: "Segoe UI", sans-serif;
              text-align: center;
              padding: 50px;
            }
            .btn {
              padding: 12px 20px;
              background: #2a5298;
              color: #fff;
              border: none;
              border-radius: 8px;
              cursor: pointer;
              transition: 0.3s;
            }
            .btn:hover {background: #1e3c72;}
          </style>
        </head>
        <body>
          <h2>👋 Welcome, {{user}}!</h2>
          <p>📊 This is your dashboard page.</p>
          <a class="btn" href="/logout">Logout</a>
        </body>
        </html>
        """, user=session["user"])
    return redirect(url_for("home"))

# ---------------- Logout ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True)
