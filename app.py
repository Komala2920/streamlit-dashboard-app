import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components
from streamlit_js_eval import streamlit_js_eval

USER_FILE = "users.csv"

# ------------------ Helpers ------------------
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["name", "email", "password"])
    df.to_csv(USER_FILE, index=False)

def load_users():
    return pd.read_csv(USER_FILE)

def save_user(name, email, password):
    df = load_users()
    if email in df["email"].values:
        return False
    new_user = pd.DataFrame([[name, email, password]], columns=["name", "email", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

def authenticate(email, password):
    df = load_users()
    user = df[(df["email"] == email) & (df["password"] == password)]
    if not user.empty:
        return user.iloc[0]["name"]
    return None

# ------------------ HTML with JS (sliding animation) ------------------
html_code = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css?family=Poppins:400,700');
    body {
      font-family: 'Poppins', sans-serif;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      background: #f6f5f7;
      margin: 0;
    }
    .container {
      background: #fff;
      border-radius: 15px;
      box-shadow: 0 14px 28px rgba(0,0,0,0.25), 
                  0 10px 10px rgba(0,0,0,0.22);
      position: relative;
      overflow: hidden;
      width: 768px;
      max-width: 100%;
      min-height: 480px;
    }
    .form-container {
      position: absolute;
      top: 0;
      height: 100%;
      transition: all 0.6s ease-in-out;
    }
    .sign-in-container {
      left: 0;
      width: 50%;
      z-index: 2;
    }
    .sign-up-container {
      left: 0;
      width: 50%;
      opacity: 0;
      z-index: 1;
    }
    .container.right-panel-active .sign-in-container {
      transform: translateX(100%);
    }
    .container.right-panel-active .sign-up-container {
      transform: translateX(100%);
      opacity: 1;
      z-index: 5;
    }
    form {
      background: #fff;
      display: flex;
      flex-direction: column;
      padding: 0 50px;
      height: 100%;
      justify-content: center;
      align-items: center;
      text-align: center;
    }
    input {
      background: #eee;
      border: none;
      padding: 12px 15px;
      margin: 8px 0;
      width: 100%;
      border-radius: 8px;
    }
    button {
      border-radius: 20px;
      border: 1px solid #20c997;
      background: #20c997;
      color: #fff;
      font-size: 14px;
      font-weight: bold;
      padding: 12px 45px;
      margin-top: 15px;
      cursor: pointer;
    }
    .overlay-container {
      position: absolute;
      top: 0;
      left: 50%;
      width: 50%;
      height: 100%;
      overflow: hidden;
      transition: transform 0.6s ease-in-out;
      z-index: 100;
    }
    .container.right-panel-active .overlay-container {
      transform: translateX(-100%);
    }
    .overlay {
      background: linear-gradient(to right, #20c997, #17a2b8);
      color: #fff;
      position: relative;
      left: -100%;
      height: 100%;
      width: 200%;
      transform: translateX(0);
      transition: transform 0.6s ease-in-out;
      display: flex;
    }
    .container.right-panel-active .overlay {
      transform: translateX(50%);
    }
    .overlay-panel {
      position: absolute;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      top: 0;
      height: 100%;
      width: 50%;
      padding: 0 40px;
    }
    .overlay-left {
      transform: translateX(-20%);
      left: 0;
    }
    .overlay-right {
      right: 0;
      transform: translateX(0);
    }
    .container.right-panel-active .overlay-left {
      transform: translateX(0);
    }
    .container.right-panel-active .overlay-right {
      transform: translateX(20%);
    }
  </style>
</head>
<body>
  <div class="container" id="container">
    <div class="form-container sign-up-container">
      <form id="signupForm">
        <h1>Create Account</h1>
        <input type="text" placeholder="Name" id="s_name"/>
        <input type="email" placeholder="Email" id="s_email"/>
        <input type="password" placeholder="Password" id="s_pass"/>
        <button type="button" onclick="signup()">Sign Up</button>
      </form>
    </div>
    <div class="form-container sign-in-container">
      <form id="signinForm">
        <h1>Sign in</h1>
        <input type="email" placeholder="Email" id="l_email"/>
        <input type="password" placeholder="Password" id="l_pass"/>
        <button type="button" onclick="signin()">Sign In</button>
      </form>
    </div>
    <div class="overlay-container">
      <div class="overlay">
        <div class="overlay-panel overlay-left">
          <h1>Welcome Back!</h1>
          <p>To keep connected, please login</p>
          <button class="ghost" id="signIn">Sign In</button>
        </div>
        <div class="overlay-panel overlay-right">
          <h1>Hello, Friend!</h1>
          <p>Enter details and start your journey</p>
          <button class="ghost" id="signUp">Sign Up</button>
        </div>
      </div>
    </div>
  </div>

<script>
  const container = document.getElementById('container');
  document.getElementById('signUp').addEventListener('click', () => container.classList.add("right-panel-active"));
  document.getElementById('signIn').addEventListener('click', () => container.classList.remove("right-panel-active"));

  function signup(){
      const data = {
        type: "signup",
        name: document.getElementById("s_name").value,
        email: document.getElementById("s_email").value,
        pass: document.getElementById("s_pass").value
      };
      window.parent.postMessage({isStreamlitMessage: true, ...data}, "*");
  }
  function signin(){
      const data = {
        type: "signin",
        email: document.getElementById("l_email").value,
        pass: document.getElementById("l_pass").value
      };
      window.parent.postMessage({isStreamlitMessage: true, ...data}, "*");
  }
</script>
</body>
</html>
"""

# ------------------ Render ------------------
components.html(html_code, height=600)

# ------------------ Capture JS → Python ------------------
event = streamlit_js_eval(js_expressions="window.lastMsg", key="msg", want_output=True)

if isinstance(event, dict) and "type" in event:
    if event["type"] == "signup":
        ok = save_user(event["name"], event["email"], event["pass"])
        if ok:
            st.success("✅ Account created successfully! Please sign in.")
        else:
            st.error("❌ Email already exists!")
    elif event["type"] == "signin":
        user = authenticate(event["email"], event["pass"])
        if user:
            st.success(f"🎉 Welcome back, {user}!")
        else:
            st.error("❌ Invalid credentials")
