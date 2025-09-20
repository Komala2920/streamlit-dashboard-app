import streamlit as st

st.set_page_config(page_title="Login Page", layout="centered")

# ---------------- CSS ----------------
page_bg = """
<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #1f2235;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.container {
  display: flex;
  width: 900px;
  height: 550px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  border-radius: 12px;
  overflow: hidden;
}

.left {
  flex: 1;
  background: linear-gradient(135deg, #2c3e91, #3a60d2);
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  text-align: center;
}

.left h1 {
  font-size: 26px;
  margin-bottom: 10px;
}

.left p {
  margin-bottom: 20px;
}

.left button {
  padding: 12px 30px;
  background: #00d1ff;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.left button:hover {
  background: #00a8cc;
}

.right {
  flex: 1;
  background: #2a2c3a;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: #fff;
}

.right h2 {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  margin-bottom: 6px;
  color: #ccc;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 6px;
  background: #1c1e2a;
  color: #fff;
  font-size: 14px;
}

.form-group input:focus {
  outline: 2px solid #00d1ff;
}

.btn {
  padding: 12px;
  width: 100%;
  border: none;
  border-radius: 6px;
  background: #00d1ff;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn:hover {
  background: #00a8cc;
}

.small-text {
  margin-top: 15px;
  font-size: 12px;
  color: #aaa;
}

.small-text a {
  color: #00d1ff;
  text-decoration: none;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- HTML ----------------
html_code = """
<div class="container">
  <!-- Left side (Sign Up) -->
  <div class="left">
    <h1>Hello! Welcome to the ArBitrage trading platform</h1>
    <p>Don’t have an account yet?</p>
    <button onclick="alert('Redirecting to signup page...')">Sign Up</button>
  </div>

  <!-- Right side (Sign In) -->
  <div class="right">
    <h2>Sign In</h2>
    <form>
      <div class="form-group">
        <label for="login">Login or Email</label>
        <input type="text" id="login" placeholder="Enter your login or email" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" placeholder="Enter your password" required>
      </div>
      <button type="submit" class="btn">Sign In</button>
    </form>
    <p class="small-text">
      By clicking "Sign Up" button, you agree to our <a href="#">Terms & Conditions</a>.
    </p>
  </div>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)
