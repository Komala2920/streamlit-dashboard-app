# app.py
import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import altair as alt

DB_PATH = "app_data.db"

# -------------------------
# Database helpers
# -------------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            name TEXT,
            password_hash TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_db_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(email, name, password):
    conn = get_db_conn()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
                  (email, name, hash_password(password)))
        conn.commit()
        return True, "User created"
    except sqlite3.IntegrityError:
        return False, "Email already registered"
    finally:
        conn.close()

def verify_user(email, password):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT password_hash, name FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        stored_hash, name = row
        return stored_hash == hash_password(password), name
    return False, None

# -------------------------
# Custom CSS for Dark Theme
# -------------------------
def load_dark_theme():
    st.markdown(
        """
        <style>
        body {
            background-color: #0e0c2a;
            background-image: radial-gradient(circle at 20% 30%, #1d1b3a 25%, transparent 40%),
                              radial-gradient(circle at 80% 70%, #1d1b3a 25%, transparent 40%);
            color: white;
        }
        .block-container {
            padding-top: 4rem;
        }
        .login-box {
            background-color: #1c1a3a;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0px 8px 24px rgba(0,0,0,0.4);
            width: 400px;
            margin: auto;
            text-align: center;
        }
        .login-box h1 {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #2a274d;
            color: white;
            border-radius: 8px;
        }
        .stButton>button {
            background: #007bff;
            color: white;
            border-radius: 8px;
            width: 100%;
            padding: 10px;
            border: none;
            font-size: 16px;
        }
        .stButton>button:hover {
            background: #0056d6;
        }
        .forgot {
            margin-top: 10px;
            font-size: 13px;
        }
        .forgot a {
            color: #8aa8ff;
            text-decoration: none;
        }
        </style>
        """, unsafe_allow_html=True
    )

# -------------------------
# Pages
# -------------------------
def show_login():
    load_dark_theme()
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1>gratafy</h1>", unsafe_allow_html=True)

    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        ok, name = verify_user(email, password)
        if ok:
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success(f"Welcome, {name or email}")
        else:
            st.error("Invalid email or password")

    st.markdown("<div class='forgot'><a href='#'>Forgot your password?</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Main
# -------------------------
def main():
    init_db()
    st.set_page_config(page_title="Gratafy", page_icon="🔑", layout="centered")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

    if not st.session_state.logged_in:
        show_login()
    else:
        st.title("Welcome to the App 🎉")
        st.write("You are now logged in.")

if __name__ == "__main__":
    main()
