# app.py
import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import altair as alt
from pathlib import Path

# Optional: Lottie
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except Exception:
    LOTTIE_AVAILABLE = False

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
    c.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

def store_feedback(user_email, message):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("INSERT INTO feedback (user_email, message) VALUES (?, ?)", (user_email, message))
    conn.commit()
    conn.close()

def get_feedbacks(limit=100):
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT user_email, message, created_at FROM feedback ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

# -------------------------
# UI CSS Styling
# -------------------------
def local_css():
    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #e6f0ff, #ffffff);
        }

        .login-box {
            background: #fff;
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
            animation: fadeIn 0.8s ease;
        }

        .stButton>button {
            border-radius: 10px;
            padding: 10px 16px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            background: linear-gradient(90deg,#1376ff,#1ea1ff);
            color: white;
            border: none;
            box-shadow: 0 6px 14px rgba(20,80,200,0.12);
        }
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 26px rgba(20,80,200,0.18);
        }

        input, textarea {
            border-radius: 8px !important;
        }
        </style>
        """, unsafe_allow_html=True
    )

def load_lottie_url(url: str):
    import requests
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

# -------------------------
# Pages
# -------------------------
def show_login():
    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    st.markdown("## Login")

    cols = st.columns([1, 1])
    with cols[0]:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, name = verify_user(email, password)
            if ok:
                st.success("Welcome back, " + (name or email))
                st.session_state.logged_in = True
                st.session_state.user_email = email
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

    with cols[1]:
        if LOTTIE_AVAILABLE:
            lottie = load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_jcikwtux.json")
            if lottie:
                st_lottie(lottie, height=400)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/552/552220.png", width=300)

    st.markdown("---")
    st.info("Don't have an account? Sign up below.")
    with st.expander("Sign up"):
        name = st.text_input("Full name", key="signup_name")
        email_s = st.text_input("Email", key="signup_email")
        password_s = st.text_input("Password", type="password", key="signup_password")
        if st.button("Create account"):
            ok, msg = create_user(email_s, name, password_s)
            if ok:
                st.success("Account created — you can login now.")
            else:
                st.error(msg)

def show_home():
    st.title("Home")
    st.write("👋 Welcome to Global Balance!")
    sample = pd.DataFrame({
        "category": ["A", "B", "C", "D"],
        "value": [45, 28, 90, 55]
    })
    st.subheader("Quick Overview")
    bar = alt.Chart(sample).mark_bar().encode(
        x="category",
        y="value"
    ).properties(height=240)
    st.altair_chart(bar, use_container_width=True)

def show_dashboard():
    st.title("Dashboard")
    st.write("Charts and analytics inspired by the illustration.")
    powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
    st.markdown(f"""
        <iframe title="PowerBI Dashboard"
            width="100%" height="600"
            src="{powerbi_url}"
            frameborder="0" allowFullScreen="true"></iframe>
    """, unsafe_allow_html=True)

def show_profile():
    st.title("Profile")
    email = st.session_state.get("user_email", "")
    conn = get_db_conn()
    c = conn.cursor()
    c.execute("SELECT name, email FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    if row:
        name, email = row
        st.success(f"**{name}**\n\n{email}")
    else:
        st.write("No profile info found.")

def show_feedback():
    st.title("Feedback")
    email = st.session_state.get("user_email", "")
    message = st.text_area("Your feedback", height=140)
    if st.button("Send feedback"):
        if not email:
            st.error("Please login to send feedback")
        elif not message.strip():
            st.error("Please enter a message")
        else:
            store_feedback(email, message)
            st.success("Thanks! Your feedback was recorded.")
    st.markdown("### Recent feedback")
    rows = get_feedbacks(10)
    for r in rows:
        st.write(f"📧 {r[0]} — {r[2]}")
        st.write(r[1])
        st.markdown("---")

# -------------------------
# Main
# -------------------------
def main():
    init_db()
    st.set_page_config(page_title="Global Balance", page_icon="💠", layout="wide")
    local_css()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.user_email = ""

    if not st.session_state.logged_in:
        show_login()
    else:
        pages = {
            "Home": show_home,
            "Dashboard": show_dashboard,
            "Profile": show_profile,
            "Feedback": show_feedback
        }
        st.sidebar.title("Navigation")
        choice = st.sidebar.radio("Go to", list(pages.keys()))
        pages[choice]()

if __name__ == "__main__":
    main()
