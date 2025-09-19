import streamlit as st
import sqlite3
import bcrypt

# ========== DATABASE SETUP ==========
conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              name TEXT, email TEXT UNIQUE, password TEXT)''')
conn.commit()

# ========== HELPER FUNCTIONS ==========
def create_user(name, email, password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed))
        conn.commit()
        return True
    except:
        return False

def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=?", (email,))
    user = c.fetchone()
    if user and bcrypt.checkpw(password.encode(), user[3]):
        return {"id": user[0], "name": user[1], "email": user[2]}
    return None

# ========== STREAMLIT CONFIG ==========
st.set_page_config(page_title="Dashboard App", page_icon="🖥️", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    body {background-color: #f3f5f7;}
    .main-title {text-align: center; color: #20bfa9; font-size: 32px; font-weight: bold;}
    .sidebar .sidebar-content {background-color: #20bfa9; color: white;}
    .stButton button {
        border-radius: 25px;
        background-color: #20bfa9;
        color: white;
        border: none;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #17a58f;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# ========== SESSION STATE ==========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Login"

# ========== PAGES ==========
def login_page():
    st.markdown("<h2 class='main-title'>🔐 Login</h2>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.session_state.page = "Home"
            st.success(f"Welcome back, {user['name']}!")
        else:
            st.error("Invalid email or password")

    st.write("Don't have an account?")
    if st.button("Sign Up Here"):
        st.session_state.page = "Signup"

def signup_page():
    st.markdown("<h2 class='main-title'>📝 Sign Up</h2>", unsafe_allow_html=True)
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if create_user(name, email, password):
            st.success("Account created! Please log in.")
            st.session_state.page = "Login"
        else:
            st.error("Email already exists!")

    if st.button("Back to Login"):
        st.session_state.page = "Login"

def home_page():
    st.markdown("<h2 class='main-title'>🏠 Home</h2>", unsafe_allow_html=True)
    st.write("Welcome to the Home Page!")

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    st.write("Here is your interactive dashboard content...")

def profile_page():
    st.markdown("<h2 class='main-title'>👤 Profile</h2>", unsafe_allow_html=True)
    st.write(f"**Name:** {st.session_state.user['name']}")
    st.write(f"**Email:** {st.session_state.user['email']}")

def feedback_page():
    st.markdown("<h2 class='main-title'>💬 Feedback</h2>", unsafe_allow_html=True)
    feedback = st.text_area("Enter your feedback here:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "Login"
    st.success("Logged out successfully!")

# ========== SIDEBAR NAVIGATION ==========
if st.session_state.logged_in:
    st.sidebar.title("📌 Navigation")
    if st.sidebar.button("🏠 Home"):
        st.session_state.page = "Home"
    if st.sidebar.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"
    if st.sidebar.button("👤 Profile"):
        st.session_state.page = "Profile"
    if st.sidebar.button("💬 Feedback"):
        st.session_state.page = "Feedback"
    if st.sidebar.button("🚪 Logout"):
        logout()

# ========== ROUTER ==========
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        login_page()
    elif st.session_state.page == "Signup":
        signup_page()
else:
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Dashboard":
        dashboard_page()
    elif st.session_state.page == "Profile":
        profile_page()
    elif st.session_state.page == "Feedback":
        feedback_page()
