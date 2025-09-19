import streamlit as st
import sqlite3
import base64

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
    button, .stButton button {{
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
    }}
    button:hover {{
        background: linear-gradient(90deg, #0072ff, #00c6ff);
        color: #fff;
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

# ========= Sidebar Navigation =========
menu = ["Login", "Sign Up", "Home", "Dashboard", "Profile", "Feedback", "Logout"]
choice = st.sidebar.radio("Navigation", menu)

# ========= Authentication =========
if choice == "Sign Up":
    st.subheader("🔐 Create an Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (new_user, new_pass))
            conn.commit()
            st.success("✅ Account created successfully! Go to Login.")
        except:
            st.warning("⚠ Username already exists.")

elif choice == "Login":
    st.subheader("🔑 Login to Global Balance")
    user = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, passwd))
        data = c.fetchone()
        if data:
            st.success(f"🎉 Welcome {user}!")
            st.session_state["user"] = user
        else:
            st.error("❌ Invalid credentials.")

# ========= Pages =========
elif choice == "Home":
    st.subheader("🏠 Home")
    st.write("Welcome to *Global Balance*! Explore the dashboard for insights.")

elif choice == "Dashboard":
    st.subheader("📊 Dashboard")
    st.write("Interactive data visualization will go here.")
    # Example chart
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    df = pd.DataFrame(np.random.randn(10, 2), columns=["Balance A", "Balance B"])
    st.line_chart(df)

elif choice == "Profile":
    st.subheader("👤 Profile")
    if "user" in st.session_state:
        st.write(f"Logged in as: *{st.session_state['user']}*")
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
