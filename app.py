import streamlit as st
import sqlite3
import streamlit.components.v1 as components

# ========= Database Setup =========
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT UNIQUE, password TEXT)''')
conn.commit()

# ========= App Title =========
st.markdown("<h1 style='text-align: center; color: cyan;'>🌍 Global Balance</h1>", unsafe_allow_html=True)

# ========= Sidebar =========
menu = ["Login/SignUp", "Home", "Dashboard", "Profile", "Feedback", "Logout"]
choice = st.sidebar.radio("Navigation", menu)

# ========= Sliding Login/Signup =========
if choice == "Login/SignUp":
    st.subheader("🔐 Sliding Sign In / Sign Up")

    # Load HTML + CSS + JS for animation
    sliding_html = """
    <style>
    body {font-family: 'Arial', sans-serif;}
    .container {position: relative; width: 768px; max-width: 100%; min-height: 480px; margin: auto;
                background: #fff; box-shadow: 0 14px 28px rgba(0,0,0,0.25); border-radius: 10px;
                overflow: hidden;}
    .form-container {position: absolute; top: 0; height: 100%; transition: all 0.6s ease-in-out;}
    .sign-in-container {left: 0; width: 50%; z-index: 2;}
    .sign-up-container {left: 0; width: 50%; opacity: 0; z-index: 1;}
    .container.right-panel-active .sign-in-container {transform: translateX(100%);}
    .container.right-panel-active .sign-up-container {transform: translateX(100%); opacity: 1; z-index: 5;}
    .overlay-container {position: absolute; top: 0; left: 50%; width: 50%; height: 100%;
                        background: linear-gradient(to right, #00b09b, #96c93d); color: white;
                        transition: transform 0.6s ease-in-out; z-index: 100;}
    .container.right-panel-active .overlay-container {transform: translateX(-100%);}
    .form {background: #fff; display: flex; flex-direction: column; padding: 50px; height: 100%; justify-content: center;}
    .form input {margin: 8px 0; padding: 12px; border: 1px solid #ddd; border-radius: 5px;}
    button {border-radius: 20px; border: 1px solid #00b09b; background-color: #00b09b; color: #fff;
            font-size: 12px; font-weight: bold; padding: 12px 45px; letter-spacing: 1px;
            text-transform: uppercase; transition: transform 80ms ease-in;}
    button:active {transform: scale(0.95);}
    button:focus {outline: none;}
    </style>

    <div class="container" id="container">
      <div class="form-container sign-up-container">
        <form action="#">
          <h2>Create Account</h2>
          <input type="text" placeholder="Name" />
          <input type="email" placeholder="Email" />
          <input type="password" placeholder="Password" />
          <button>Sign Up</button>
        </form>
      </div>
      <div class="form-container sign-in-container">
        <form action="#">
          <h2>Sign in</h2>
          <input type="text" placeholder="Username" />
          <input type="password" placeholder="Password" />
          <button>Sign In</button>
        </form>
      </div>
      <div class="overlay-container">
        <div class="overlay">
          <h1>Welcome Back!</h1>
          <p>To keep connected with us, please login</p>
          <button class="ghost" id="signIn">Sign In</button>
          <button class="ghost" id="signUp">Sign Up</button>
        </div>
      </div>
    </div>

    <script>
    const container = document.getElementById('container');
    const signUpButton = document.getElementById('signUp');
    const signInButton = document.getElementById('signIn');

    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });
    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });
    </script>
    """

    components.html(sliding_html, height=600)

# ========= Other Pages =========
elif choice == "Home":
    st.subheader("🏠 Home")
    st.write("Welcome to Global Balance! Explore the dashboard for insights.")

elif choice == "Dashboard":
    st.subheader("📊 Dashboard")
    import pandas as pd, numpy as np
    df = pd.DataFrame(np.random.randn(10, 2), columns=["Balance A", "Balance B"])
    st.line_chart(df)

elif choice == "Profile":
    st.subheader("👤 Profile")
    if "user" in st.session_state:
        st.write(f"Logged in as: {st.session_state['user']}")
    else:
        st.warning("⚠ Please log in to view your profile.")

elif choice == "Feedback":
    st.subheader("💬 Feedback")
    feedback = st.text_area("Share your feedback:")
    if st.button("Submit Feedback"):
        st.success("🙌 Thank you for your feedback!")

elif choice == "Logout":
    if "user" in st.session_state:
        st.session_state.clear()
        st.success("✅ You have logged out successfully.")
    else:
        st.warning("⚠ You are not logged in.")
