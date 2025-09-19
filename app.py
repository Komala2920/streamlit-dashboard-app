import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Login & Signup", layout="centered")

# ----------------------------
# Custom HTML + placeholders for Streamlit widgets
# ----------------------------
html_code = """
<div class="container" id="container">
  <div class="form-container sign-up-container">
    <div id="signup_form"></div>
  </div>
  <div class="form-container sign-in-container">
    <div id="signin_form"></div>
  </div>
  <div class="overlay-container">
    <div class="overlay">
      <div class="overlay-panel overlay-left">
        <h1>Welcome Back!</h1>
        <p>To keep connected with us please login</p>
        <button id="signIn">Sign In</button>
      </div>
      <div class="overlay-panel overlay-right">
        <h1>Hello, Friend!</h1>
        <p>Enter your personal details and start your journey with us</p>
        <button id="signUp">Sign Up</button>
      </div>
    </div>
  </div>
</div>

<style>
  * { box-sizing: border-box; font-family: "Poppins", sans-serif; }
  body { background: #f6f5f7; }
  .container {
    background: #fff; border-radius: 10px;
    box-shadow: 0 14px 28px rgba(0,0,0,0.25),
                0 10px 10px rgba(0,0,0,0.22);
    position: relative; overflow: hidden;
    width: 768px; max-width: 100%; min-height: 480px;
    margin: auto; margin-top: 30px;
  }
  .form-container {
    position: absolute; top: 0; height: 100%;
    transition: all 0.6s ease-in-out;
    display: flex; justify-content: center; align-items: center;
    padding: 20px; flex-direction: column;
  }
  .sign-in-container { left: 0; width: 50%; z-index: 2; }
  .sign-up-container { left: 0; width: 50%; opacity: 0; z-index: 1; }
  .container.right-panel-active .sign-in-container { transform: translateX(100%); }
  .container.right-panel-active .sign-up-container {
    transform: translateX(100%); opacity: 1; z-index: 5; animation: show 0.6s;
  }
  @keyframes show {
    0%, 49.99% { opacity: 0; z-index: 1; }
    50%, 100% { opacity: 1; z-index: 5; }
  }
  .overlay-container {
    position: absolute; top: 0; left: 50%; width: 50%; height: 100%;
    overflow: hidden; transition: transform 0.6s ease-in-out; z-index: 100;
  }
  .container.right-panel-active .overlay-container { transform: translateX(-100%); }
  .overlay {
    background: linear-gradient(to right, #20c997, #17a2b8);
    color: #fff; position: relative; left: -100%;
    height: 100%; width: 200%; transform: translateX(0);
    transition: transform 0.6s ease-in-out;
  }
  .container.right-panel-active .overlay { transform: translateX(50%); }
  .overlay-panel {
    position: absolute; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 0 40px; text-align: center;
    top: 0; height: 100%; width: 50%;
    transition: transform 0.6s ease-in-out;
  }
  .overlay-left { transform: translateX(-20%); left: 0; }
  .container.right-panel-active .overlay-left { transform: translateX(0); }
  .overlay-right { right: 0; transform: translateX(0); }
  .container.right-panel-active .overlay-right { transform: translateX(20%); }
  button {
    border-radius: 20px; border: 1px solid #fff; background: transparent;
    color: #fff; font-size: 14px; font-weight: bold; padding: 12px 45px;
    letter-spacing: 1px; text-transform: uppercase;
    transition: transform 80ms ease-in; cursor: pointer;
  }
</style>

<script>
  const signUpButton = document.getElementById('signUp');
  const signInButton = document.getElementById('signIn');
  const container = document.getElementById('container');
  signUpButton.addEventListener('click', () => { container.classList.add("right-panel-active"); });
  signInButton.addEventListener('click', () => { container.classList.remove("right-panel-active"); });
</script>
"""

# Render the animated container
components.html(html_code, height=500, scrolling=False)

# ----------------------------
# Streamlit Forms Inside Animation Slots
# ----------------------------
tab = st.session_state.get("tab", "signin")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔑 Sign In")
    signin_email = st.text_input("Email", key="signin_email")
    signin_pass = st.text_input("Password", type="password", key="signin_pass")
    if st.button("Sign In"):
        st.success(f"Welcome back, {signin_email}!")

with col2:
    st.markdown("### 🆕 Sign Up")
    signup_name = st.text_input("Name", key="signup_name")
    signup_email = st.text_input("Email", key="signup_email")
    signup_pass = st.text_input("Password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        st.success(f"Account created for {signup_name}!")
