import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components

# ---------------------- DATABASE ----------------------
conn = sqlite3.connect('users.db')
c = conn.cursor()
# Added additional columns for profile info
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

def add_user(username, password):
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, make_hash(password)))
    conn.commit()

def update_profile(username, first_name, last_name, email):
    c.execute('UPDATE users SET first_name=?, last_name=?, email=? WHERE username=?',
              (first_name, last_name, email, username))
    conn.commit()

def change_password(username, current_password, new_password):
    user = check_user(username, current_password)
    if user:
        c.execute('UPDATE users SET password=? WHERE username=?', (make_hash(new_password), username))
        conn.commit()
        return True
    return False

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
/* Sidebar buttons all same size */
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
                st.session_state.page = "🏠 Home"  # Redirect to home after login
                st.success("✅ Login successful")
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

    # --- Sidebar Navigation (Vertical) ---
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

    # --- Page Content ---
    if st.session_state.page == "🏠 Home":
        st.header("🏠 Welcome Home")
        st.write(f"Hello, **{st.session_state.user}** 👋")
        st.subheader("🌐 Overview")
        st.markdown("""
        **Global Balance** is a comprehensive platform to monitor and analyze global economic and financial data.  
        Access dashboards, manage your profile, and provide feedback in one secure environment.
        """)
        st.subheader("✨ Features")
        st.markdown("""
        - Interactive Dashboards 📊  
        - Profile Management 👤  
        - Feedback Portal 💬  
        - Secure Login & Signup 🔐  
        """)

    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")
        st.subheader("🌐 Dashboard Overview")
        st.markdown("""
        Explore global economic metrics like income inequality, GDP trends, and other indicators.  
        Use filters to customize views and hover over charts for detailed info.
        """)
        st.subheader("📝 How to Use")
        st.markdown("""
        - Apply filters and slicers to focus on specific regions or years.  
        - Hover to see detailed data points.  
        - Export visuals for reports.
        """)
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Income Inequality Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)

    elif st.session_state.page == "👤 Profile":
        st.header("👤 Profile")

        # Fetch user data
        c.execute('SELECT first_name, last_name, email FROM users WHERE username=?', (st.session_state.user,))
        data = c.fetchone()
        first_name = data[0] if data[0] else ""
        last_name = data[1] if data[1] else ""
        email = data[2] if data[2] else ""

        st.subheader("📝 Personal Information")
        first_name_input = st.text_input("First Name", value=first_name)
        last_name_input = st.text_input("Last Name", value=last_name)
        email_input = st.text_input("Email", value=email)

        if st.button("Update Profile"):
            update_profile(st.session_state.user, first_name_input, last_name_input, email_input)
            st.success("✅ Profile updated successfully.")

        st.subheader("🔒 Change Password")
        current_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        if st.button("Reset Password"):
            if new_pass != confirm_pass:
                st.error("❌ New passwords do not match.")
            elif change_password(st.session_state.user, current_pass, new_pass):
                st.success("✅ Password updated successfully.")
            else:
                st.error("❌ Current password is incorrect.")

    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        feedback = st.text_area("Write your feedback:")
        if st.button("Submit Feedback"):
            st.success("✅ Thanks for your feedback!")
