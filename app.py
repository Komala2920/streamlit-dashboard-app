import streamlit as st
import sqlite3
import hashlib

# ---------------------- DATABASE ----------------------
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
conn.commit()

# ---------------------- UTILS -------------------------
def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, make_hash(password)))
    return c.fetchone()

def add_user(username, password):
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, make_hash(password)))
    conn.commit()

# ---------------------- CSS (Theme like your pic) ----------------------
st.markdown("""
    <style>
    body {
        background: #0f172a;
        font-family: 'Segoe UI', sans-serif;
        color: white;
    }
    .main {
        background: linear-gradient(135deg,#0f172a 0%,#0b3b63 40%,#2c6b5f 100%);
        border-radius: 15px;
        padding: 30px;
        color: white;
    }
    .stButton button {
        background: #0ea5e9;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: #0284c7;
        transform: scale(1.05);
    }
    .nav-btn {
        display:inline-block;
        margin: 0.3em;
        padding: 0.5em 1em;
        background:#0ea5e9;
        color:white;
        border-radius:6px;
        font-weight:500;
        cursor:pointer;
        text-decoration:none;
    }
    .nav-btn:hover {
        background:#0284c7;
    }
    .logo {
        font-size: 28px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- SESSION ----------------------
if "page" not in st.session_state:
    st.session_state.page = "login"
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------------- PAGES ----------------------
def login_page():
    st.markdown("<div class='logo'>ArBitrage</div>", unsafe_allow_html=True)
    st.subheader("🔐 Sign In")
    username = st.text_input("Login / Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        user = check_user(username, password)
        if user:
            st.session_state.user = username
            st.session_state.page = "home"
            st.success("✅ Login successful")
        else:
            st.error("❌ Invalid username or password")
    if st.button("Go to Sign Up"):
        st.session_state.page = "signup"

def signup_page():
    st.markdown("<div class='logo'>ArBitrage</div>", unsafe_allow_html=True)
    st.subheader("📝 Create Account")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    if st.button("Register"):
        if username and password:
            add_user(username, password)
            st.success("✅ Account created. Please login.")
            st.session_state.page = "login"
        else:
            st.error("⚠ Please enter valid details")
    if st.button("Back to Login"):
        st.session_state.page = "login"

def nav_bar():
    st.markdown(
        """
        <div style="text-align:center; margin-top:20px;">
            <a class="nav-btn" href="?page=home">🏠 Home</a>
            <a class="nav-btn" href="?page=dashboard">📊 Dashboard</a>
            <a class="nav-btn" href="?page=profile">👤 Profile</a>
            <a class="nav-btn" href="?page=feedback">💬 Feedback</a>
            <a class="nav-btn" href="?page=logout">🚪 Logout</a>
        </div>
        """,
        unsafe_allow_html=True
    )

def home_page():
    st.markdown("<div class='logo'>ArBitrage</div>", unsafe_allow_html=True)
    nav_bar()
    st.header("🏠 Welcome to Dashboard")
    st.write(f"Hello, **{st.session_state.user}** 👋")
    st.success("This is your trading dashboard style UI.")

def dashboard_page():
    st.markdown("<div class='logo'>ArBitrage</div>", unsafe_allow_html=True)
    nav_bar()
    st.header("📊 Dashboard")
    st.write("Your stats / graphs will be here.")
    st.line_chart({"Performance": [10, 20, 15, 30, 25, 40]})

def profile_page():
    st.markdown("<div class='logo'>ArBitrage</div>", unsafe_allow_html=True)
    nav_bar()
    st.header("👤 Profile")
    st.write(f"Username: **{st.session_state.user}**")
    st.write("Email: user@example.com (dummy)")
    st.info("You can extend this page with more details.")

def feedback_page():
    st.markdown("<div class='logo'>ArBitrage</div>", unsafe_allow_html=True)
    nav_bar()
    st.header("💬 Feedback")
    feedback = st.text_area("Write your feedback:")
    if st.button("Submit Feedback"):
        st.success("✅ Thanks for your feedback!")

def logout_page():
    st.session_state.user = None
    st.session_state.page = "login"
    st.success("🚪 You have been logged out.")

# ---------------------- ROUTING ----------------------
if st.session_state.user:
    query_params = st.experimental_get_query_params()
    if "page" in query_params:
        st.session_state.page = query_params["page"][0]

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()
    elif st.session_state.page == "profile":
        profile_page()
    elif st.session_state.page == "feedback":
        feedback_page()
    elif st.session_state.page == "logout":
        logout_page()
else:
    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "signup":
        signup_page()
