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

# ---------------------- CSS ----------------------
st.markdown("""
    <style>
    body {
        background: #0f172a;
        font-family: 'Segoe UI', sans-serif;
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
    .logo {
        font-size: 28px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 15px;
    }
    .navbar {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-bottom: 25px;
    }
    .nav-item {
        background: #0ea5e9;
        color: white;
        padding: 0.5em 1.2em;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 500;
        transition: 0.3s;
        cursor: pointer;
    }
    .nav-item:hover {
        background: #0284c7;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- SESSION ----------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"

# ---------------------- LOGIN / SIGNUP ----------------------
if st.session_state.user is None:
    st.markdown("<div class='logo'>Global Balance</div>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In"):
            user = check_user(username, password)
            if user:
                st.session_state.user = username
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    with tab2:
        new_user = st.text_input("Choose Username", key="signup_user")
        new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
        if st.button("Register"):
            if new_user and new_pass:
                add_user(new_user, new_pass)
                st.success("✅ Account created. Now login.")
            else:
                st.error("⚠ Please enter valid details.")

# ---------------------- MAIN APP ----------------------
else:
    st.markdown("<div class='logo'>Global Balance</div>", unsafe_allow_html=True)

    # --- Top Navigation ---
    nav_items = ["🏠 Home", "📊 Dashboard", "👤 Profile", "💬 Feedback", "🚪 Logout"]
    nav_cols = st.columns(len(nav_items))
    for i, item in enumerate(nav_items):
        if nav_cols[i].button(item, key=item):
            st.session_state.page = item
            if item == "🚪 Logout":
                st.session_state.user = None
                st.success("🚪 You have been logged out.")
                st.rerun()

    # --- Page Content ---
    if st.session_state.page == "🏠 Home":
        st.header("🏠 Welcome Home")
        st.write(f"Hello, **{st.session_state.user}** 👋")
        st.success("This is your Global Balance dashboard.")

    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")
        st.write("Your performance chart:")
        st.line_chart({"Performance": [10, 20, 15, 30, 25, 40]})

    elif st.session_state.page == "👤 Profile":
        st.header("👤 Profile")
        st.write(f"Username: **{st.session_state.user}**")
        st.write("Email: user@example.com (dummy)")
        st.info("You can extend this page with more profile details.")

    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        feedback = st.text_area("Write your feedback:")
        if st.button("Submit Feedback"):
            st.success("✅ Thanks for your feedback!")
