import streamlit as st
import sqlite3

# ---------------------------
# Database Setup (SQLite)
# ---------------------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')

def add_userdata(username, password):
    c.execute('INSERT INTO users(username,password) VALUES (?,?)', (username, password))
    conn.commit()

def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username =? AND password = ?', (username, password))
    return c.fetchall()

# ---------------------------
# CSS Styling
# ---------------------------
def load_css():
    st.markdown("""
        <style>
        body {
            background: linear-gradient(135deg, #2a5298, #1e3c72);
            color: white;
        }
        .main {
            background-color: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 12px;
        }
        .stButton>button {
            background: #46c7c7;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background: #37a3a3;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)

# ---------------------------
# Pages
# ---------------------------
def home():
    st.title("🏠 Home")
    st.write("Welcome to **B-Techno App**. Navigate using the sidebar.")

def dashboard():
    st.title("📊 Dashboard")
    st.write("This is your dashboard. Display stats, graphs, or reports here.")
    st.bar_chart({"Data": [3, 5, 2, 8, 7]})

def profile(username):
    st.title("👤 Profile")
    st.write(f"Hello, **{username}** 👋")
    st.write("This is your profile page.")

def feedback():
    st.title("📝 Feedback")
    fb = st.text_area("Write your feedback here:")
    if st.button("Submit Feedback"):
        st.success("✅ Thank you for your feedback!")

# ---------------------------
# Main App
# ---------------------------
def main():
    load_css()
    st.sidebar.title("🔹 Navigation")

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Choose Action", menu)

    create_usertable()

    if choice == "Login":
        st.title("🔑 Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            result = login_user(username, password)
            if result:
                st.success(f"Welcome {username}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error("Incorrect Username/Password")

    elif choice == "Sign Up":
        st.title("🆕 Create Account")
        new_user = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            add_userdata(new_user, new_password)
            st.success("✅ Account created successfully!")
            st.info("Go to Login to access your account.")

    # If logged in → show app
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        app_menu = ["Home", "Dashboard", "Profile", "Feedback", "Logout"]
        app_choice = st.sidebar.radio("Go to", app_menu)

        if app_choice == "Home":
            home()
        elif app_choice == "Dashboard":
            dashboard()
        elif app_choice == "Profile":
            profile(st.session_state["username"])
        elif app_choice == "Feedback":
            feedback()
        elif app_choice == "Logout":
            st.session_state["logged_in"] = False
            st.success("You have been logged out.")

if __name__ == "__main__":
    main()
