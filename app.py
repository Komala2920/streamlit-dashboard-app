import streamlit as st
import sqlite3

# ---------------------- DATABASE ---------------------- #
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS feedback (username TEXT, message TEXT)")
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def check_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()
    conn.close()
    return data

def add_feedback(username, message):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO feedback VALUES (?, ?)", (username, message))
    conn.commit()
    conn.close()

# Initialize database
init_db()

# ---------------------- CUSTOM CSS ---------------------- #
st.markdown("""
    <style>
    body {
        background-color: #f4f6f9;
        font-family: "Segoe UI", sans-serif;
    }
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-size: 32px;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #ecf0f1;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        padding: 8px 20px;
    }
    .stButton>button:hover {
        background-color: #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- SESSION ---------------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# ---------------------- PAGES ---------------------- #
def home():
    st.markdown("<div class='main-title'>🏠 Home</div>", unsafe_allow_html=True)
    st.write("Welcome to the **Streamlit Web App** with Power BI integration.")

def dashboard():
    st.markdown("<div class='main-title'>📊 Dashboard</div>", unsafe_allow_html=True)
    st.write("Here is your embedded Power BI dashboard:")
    powerbi_url = "https://app.powerbi.com/groups/me/reports/4d41c1bc-17bb-491e-8da8-861aaede731f/24434bd2ed4071702132?redirectedFromSignup=1&experience=power-bi"  # Replace with your public link
    st.components.v1.iframe(powerbi_url, width=1200, height=700, scrolling=True)

def profile():
    st.markdown("<div class='main-title'>👤 Profile</div>", unsafe_allow_html=True)
    st.write(f"Username: **{st.session_state.username}**")

def feedback():
    st.markdown("<div class='main-title'>💬 Feedback</div>", unsafe_allow_html=True)
    msg = st.text_area("Enter your feedback:")
    if st.button("Submit Feedback"):
        if msg.strip() != "":
            add_feedback(st.session_state.username, msg)
            st.success("✅ Feedback submitted successfully!")
        else:
            st.error("Feedback cannot be empty!")

def login():
    st.markdown("<div class='main-title'>🔑 Login</div>", unsafe_allow_html=True)
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_user(user, pw):
            st.session_state.logged_in = True
            st.session_state.username = user
            st.success("Login successful ✅")
        else:
            st.error("Invalid username or password")

def signup():
    st.markdown("<div class='main-title'>📝 Sign Up</div>", unsafe_allow_html=True)
    user = st.text_input("Choose a Username")
    pw = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        try:
            add_user(user, pw)
            st.success("✅ Account created! Please login now.")
        except:
            st.error("⚠️ User already exists, try another username.")

# ---------------------- NAVIGATION ---------------------- #
if not st.session_state.logged_in:
    menu = st.sidebar.radio("Navigation", ["Login", "Sign Up"])
    if menu == "Login":
        login()
    else:
        signup()
else:
    menu = st.sidebar.radio("Navigation", ["Home", "Dashboard", "Profile", "Feedback", "Logout"])

    if menu == "Home":
        home()
    elif menu == "Dashboard":
        dashboard()
    elif menu == "Profile":
        profile()
    elif menu == "Feedback":
        feedback()
    elif menu == "Logout":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("✅ Logged out successfully")
