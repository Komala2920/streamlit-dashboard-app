import streamlit as st
import sqlite3
import base64
import pandas as pd
import numpy as np
import streamlit.components.v1 as components   # 👈 Added for embedding Power BI

# ========= Background Setup =========
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background: rgba(0,0,0,0);
    }}
    .main {{
        background-color: rgba(0, 0, 0, 0.65);
        padding: 25px;
        border-radius: 15px;
        color: white;
    }}
    .nav-container {{
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 25px;
    }}
    .nav-button {{
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 8px;
        padding: 10px 18px;
        font-size: 15px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s ease;
        border: none;
    }}
    .nav-button:hover {{
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        transform: translateY(-2px);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ========= Database Setup =========
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT UNIQUE, password TEXT)''')
conn.commit()

# ========= Apply Background =========
set_background("background.jpg")

# ========= App Title =========
st.markdown("<h1 style='text-align: center; color: cyan;'>🌍 Global Balance</h1>", unsafe_allow_html=True)

# ========= Navigation Setup =========
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

if "user" not in st.session_state:  
    # Before login → only Login & Sign Up
    nav_items = ["Login", "Sign Up"]
else:  
    # After login → full menu
    nav_items = ["Home", "Dashboard", "Profile", "Feedback", "Logout"]

st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
cols = st.columns(len(nav_items))
for i, item in enumerate(nav_items):
    if cols[i].button(item, key=f"nav_{item}"):
        st.session_state["page"] = item
st.markdown("</div>", unsafe_allow_html=True)

choice = st.session_state["page"]

# ========= Authentication =========
if choice == "Sign Up":
    st.subheader("🔐 Create an Account")
    new_user = st.text_input("Username", key="signup_user")
    new_pass = st.text_input("Password", type="password", key="signup_pass")
    if st.button("Sign Up", key="signup_btn"):
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (new_user, new_pass))
            conn.commit()
            st.success("✅ Account created successfully! Go to Login.")
        except:
            st.warning("⚠ Username already exists.")

elif choice == "Login":
    st.subheader("🔑 Login to Global Balance")
    user = st.text_input("Username", key="login_user")
    passwd = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login", key="login_btn"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, passwd))
        data = c.fetchone()
        if data:
            st.success(f"🎉 Welcome {user}!")
            st.session_state["user"] = user
            st.session_state["page"] = "Home"   # redirect to Home after login
        else:
            st.error("❌ Invalid credentials.")

# ========= Pages =========
elif choice == "Home":
    st.subheader("🏠 Home")
    st.write("Welcome to *Global Balance*! Explore the dashboard for insights.")

elif choice == "Dashboard":
    st.subheader("📊 Dashboard")
    if "user" in st.session_state:
        st.write("Here is your embedded Power BI dashboard:")

        # 👉 Replace with your actual Power BI embed link
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"

        # Embed Power BI Dashboard
        components.iframe(powerbi_url, width=2000, height=900, scrolling=True)
    else:
        st.warning("⚠ Please log in to view the dashboard.")

elif choice == "Profile":
    st.subheader("👤 Profile")
    if "user" in st.session_state:
        st.write(f"Logged in as: *{st.session_state['user']}*")
    else:
        st.warning("⚠ Please log in to view your profile.")

elif choice == "Feedback":
    st.subheader("💬 Feedback")
    feedback = st.text_area("Share your feedback:", key="feedback_text")
    if st.button("Submit Feedback", key="feedback_btn"):
        st.success("🙌 Thank you for your feedback!")

elif choice == "Logout":
    if "user" in st.session_state:
        st.session_state.clear()
        st.success("✅ You have logged out successfully.")
        st.session_state["page"] = "Login"
    else:
        st.warning("⚠ You are not logged in.")
