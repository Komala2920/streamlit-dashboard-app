import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components

# ---------------------- DATABASE ----------------------
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT,
    first_name TEXT,
    last_name TEXT,
    email TEXT
)''')
conn.commit()

# ---------------------- UTILS -------------------------
def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, make_hash(password)))
    return c.fetchone()

def add_user(username, password, first_name="", last_name="", email=""):
    c.execute('INSERT INTO users(username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)',
              (username, make_hash(password), first_name, last_name, email))
    conn.commit()

def get_user_details(username):
    c.execute("SELECT first_name, last_name, email FROM users WHERE username=?", (username,))
    return c.fetchone()

def update_profile(username, first_name, last_name, email):
    c.execute("UPDATE users SET first_name=?, last_name=?, email=? WHERE username=?",
              (first_name, last_name, email, username))
    conn.commit()

def update_password(username, new_password):
    c.execute("UPDATE users SET password=? WHERE username=?", (make_hash(new_password), username))
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
        transform: scale(1.02);
    }
    .logo {
        font-size: 28px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 15px;
        text-align: center;
    }
    iframe {
        border-radius: 12px;
    }
    .css-1emrehy.edgvbvh3 button {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        height: 50px !important;
        margin-bottom: 10px;
        font-size: 16px;
        display: block;
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
                st.session_state.page = "🏠 Home"
                st.success("✅ Login successful")
            else:
                st.error("❌ Invalid username or password")

    with tab2:
        new_user = st.text_input("Choose Username", key="signup_user")
        new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
        new_email = st.text_input("Email", key="signup_email")
        first_name = st.text_input("First Name", key="signup_fname")
        last_name = st.text_input("Last Name", key="signup_lname")

        if st.button("Register"):
            if new_user and new_pass:
                try:
                    add_user(new_user, new_pass, first_name, last_name, new_email)
                    st.success("✅ Account created. Now login.")
                except:
                    st.error("⚠ Username already exists.")
            else:
                st.error("⚠ Please enter valid details.")

# ---------------------- MAIN APP ----------------------
else:
    st.markdown("<div class='logo'>Global Balance</div>", unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    nav_items = ["🏠 Home", "📊 Dashboard", "👤 Profile", "💬 Feedback", "🚪 Logout"]
    for item in nav_items:
        if st.sidebar.button(item, key=item):
            if item == "🚪 Logout":
                st.session_state.user = None
                st.session_state.page = "🏠 Home"
                st.success("🚪 You have been logged out.")
            else:
                st.session_state.page = item

    # --- Pages ---
    if st.session_state.page == "👤 Profile":
        st.header("👤 Profile")

        user_data = get_user_details(st.session_state.user)
        if user_data:
            fname, lname, email = user_data
        else:
            fname, lname, email = "", "", ""

        st.subheader("🔹 Update Profile Info")
        new_fname = st.text_input("First Name", value=fname)
        new_lname = st.text_input("Last Name", value=lname)
        new_email = st.text_input("Email", value=email)

        if st.button("Save Profile"):
            update_profile(st.session_state.user, new_fname, new_lname, new_email)
            st.success("✅ Profile updated successfully")

        st.subheader("🔹 Change Password")
        current_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")

        if st.button("Update Password"):
            if check_user(st.session_state.user, current_pass):
                if new_pass == confirm_pass and new_pass.strip() != "":
                    update_password(st.session_state.user, new_pass)
                    st.success("✅ Password updated successfully")
                else:
                    st.error("⚠ Passwords do not match or empty")
            else:
                st.error("❌ Current password is incorrect")

    elif st.session_state.page == "🏠 Home":
        st.header("🏠 Welcome Home")
        st.write(f"Hello, **{st.session_state.user}** 👋")

    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Income Inequality Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)

    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        feedback = st.text_area("Write your feedback:")
        if st.button("Submit Feedback"):
            st.success("✅ Thanks for your feedback!")
