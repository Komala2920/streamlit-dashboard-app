import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components

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
                st.session_state.page = "🏠 Home"
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

    # --- Sidebar Navigation ---
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
        st.info("""
        Welcome to **Global Balance**, your personal dashboard for monitoring global financial metrics.
        Navigate using the sidebar to explore data, view your profile, and submit feedback.
        """)
        if st.button("Learn More About the Dashboard"):
            st.write("""
            The Dashboard section contains interactive visualizations powered by **Power BI**.
            Explore trends, income inequality, and other global financial insights.
            """)

    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")
        st.info("""
        This page contains an embedded Power BI report showing **global income inequality metrics**.
        You can interact with the charts, filter data, and analyze trends.
        """)
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)
        if st.button("Dashboard Tips"):
            st.success("🔹 Tip: Hover over bars and charts to see detailed values.\n🔹 Use filters on the right to customize your view.")

    elif st.session_state.page == "👤 Profile":
        st.header("👤 Profile")
        st.write(f"**Username:** {st.session_state.user}")
        st.write("**Email:** user@example.com (dummy)")
        st.info("You can extend this page with more profile details such as account settings, preferences, and activity logs.")
        if st.button("Edit Profile (Demo)"):
            st.warning("This feature is under development! Coming soon.")

    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        st.info("Your feedback helps us improve the website and dashboard experience.")
        feedback = st.text_area("Write your feedback:")
        if st.button("Submit Feedback"):
            if feedback.strip():
                st.success("✅ Thanks for your feedback!")
            else:
                st.error("⚠ Please write something before submitting.")
        if st.button("View Feedback Tips"):
            st.write("""
            🔹 Be specific about what you liked or disliked.  
            🔹 Suggest features or improvements.  
            🔹 Your input is anonymous and valuable!
            """)
