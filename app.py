import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Animated Login Page", layout="centered")

# ----------------------------
# CSS + JS Animation (Frontend Only)
# ----------------------------
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Poppins", sans-serif; }
    body { background: #f6f5f7; }
    .container {
      background: #fff;
      border-radius: 10px;
      box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
      position: relative;
      overflow: hidden;
      width: 768px;
      max-width: 100%;
      min-height: 480px;
      margin: auto;
      margin-top: 20px;
    }
    .form-container { position: absolute; top: 0; height: 100%; transition: all 0.6s ease-in-out; }
    .sign-in-container { left: 0; width: 50%; z-index: 2; }
    .sign-up-container { left: 0; width: 50%; opacity: 0; z-index: 1; }
    .container.right-panel-active .sign-in-container { transform: translateX(100%); }
    .container.right-panel-active .sign-up-container {
      transform: translateX(100%);
      opacity: 1; z-index: 5; animation: show 0.6s;
    }
    @keyframes show {
      0%, 49.99% { opacity: 0; z-index: 1; }
      50%, 100% { opacity: 1; z-index: 5; }
    }
    .overlay-container {
      position: absolute; top: 0; left: 50%; width: 50%; height: 100%; overflow: hidden;
      transition: transform 0.6s ease-in-out; z-index: 100;
    }
    .container.right-panel-active .overlay-container { transform: translateX(-100%); }
    .overlay {
      background: linear-gradient(to right, #20c997, #17a2b8);
      color: #fff; position: relative; left: -100%; height: 100%; width: 200%;
      transform: translateX(0); transition: transform 0.6s ease-in-out;
    }
    .container.right-panel-active .overlay { transform: translateX(50%); }
    .overlay-panel {
      position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center;
      padding: 0 40px; text-align: center; top: 0; height: 100%; width: 50%; transition: transform 0.6s ease-in-out;
    }
    .overlay-left { transform: translateX(-20%); left: 0; }
    .container.right-panel-active .overlay-left { transform: translateX(0); }
    .overlay-right { right: 0; transform: translateX(0); }
    .container.right-panel-active .overlay-right { transform: translateX(20%); }
    button {
      border-radius: 20px; border: 1px solid #fff; background: transparent; color: #fff;
      font-size: 14px; font-weight: bold; padding: 12px 45px; letter-spacing: 1px;
      text-transform: uppercase; transition: transform 80ms ease-in; cursor: pointer; margin-top: 10px;
    }
  </style>
</head>
<body>
  <div class="container" id="container">
    <!-- Overlay Panels Only (UI) -->
    <div class="overlay-container">
      <div class="overlay">
        <div class="overlay-panel overlay-left">
          <h1>Welcome Back!</h1>
          <p>To keep connected with us please login</p>
          <button id="signIn">Sign In</button>
        </div>
        <div class="overlay-panel overlay-right">
          <h1>Hello, Friend!</h1>
          <p>Enter your details and start your journey</p>
          <button id="signUp">Sign Up</button>
        </div>
      </div>
    </div>
  </div>
  <script>
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');
    const container = document.getElementById('container');
    signUpButton.addEventListener('click', () => { container.classList.add("right-panel-active"); });
    signInButton.addEventListener('click', () => { container.classList.remove("right-panel-active"); });
  </script>
</body>
</html>
"""

components.html(html_code, height=400, scrolling=False)

# ----------------------------
# Streamlit Functional Forms (Backend Capture)
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔑 Sign In")
    email_login = st.text_input("Email", key="login_email")
    password_login = st.text_input("Password", type="password", key="login_pass")
    if st.button("Sign In"):
        st.success(f"Logged in as {email_login}")

with col2:
    st.subheader("🆕 Sign Up")
    name_signup = st.text_input("Name", key="signup_name")
    email_signup = st.text_input("Email", key="signup_email")
    password_signup = st.text_input("Password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        st.success(f"Account created for {name_signup}")
