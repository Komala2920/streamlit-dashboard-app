import streamlit as st
import sqlite3

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )''')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    data = c.fetchone()
    conn.close()
    return data

# ---------- PAGE SETUP ----------
def home_page():
    st.markdown("<h2 style='color:#4CAF50;'>🏠 Home</h2>", unsafe_allow_html=True)
    st.write("Welcome to the Home Page!")

def dashboard_page():
    st.markdown("<h2 style='color:#2196F3;'>📊 Dashboard</h2>", unsafe_allow_html=True)
    st.write("Your analytics and data go here.")

def profile_page(username):
    st.markdown("<h2 style='color:#FF9800;'>👤 Profile</h2>", unsafe_allow_html=True)
    st.write(f"Logged in as: **{username}**")

def feedback_page():
    st.markdown("<h2 style='color:#9C27B0;'>📝 Feedback</h2>", unsafe_allow_html=True)
    feedback = st.text_area("Leave your feedback here")
    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback!")

# ---------- MAIN APP ----------
def main():
    st.set_page_config(page_title="Streamlit Dashboard", layout="wide")
    init_db()

    # Inject CSS
    st.markdown("""
        <style>
        body { background-color: #f0f2f6; font-family: 'Segoe UI', sans-serif; }
        .stButton>button { background-color: #6200EE; color: white; border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if not st.session_state.logged_in:
        menu = ["Login", "Sign Up"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            st.subheader("🔐 Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                user = login_user(username, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome {username}!")
                else:
                    st.error("Invalid credentials")

        elif choice == "Sign Up":
            st.subheader("🆕 Create Account")
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type='password')
            if st.button("Sign Up"):
                add_user(new_user, new_pass)
                st.success("Account created successfully. You can now log in.")
    else:
        nav = st.sidebar.radio("Navigate", ["Home", "Dashboard", "Profile", "Feedback", "Logout"])
        st.sidebar.markdown("---")
        st.sidebar.write(f"👤 Logged in as: **{st.session_state.username}**")

        if nav == "Home":
            home_page()
        elif nav == "Dashboard":
            dashboard_page()
        elif nav == "Profile":
            profile_page(st.session_state.username)
        elif nav == "Feedback":
            feedback_page()
        elif nav == "Logout":
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.success("You have been logged out.")

if __name__ == '__main__':
    main()
