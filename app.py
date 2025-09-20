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
                st.session_state.page = "🏠 Home"  # Reset to login
                st.success("🚪 You have been logged out.")
            else:
                st.session_state.page = item

    # --- Page Content ---
    if st.session_state.page == "🏠 Home":
        st.header("🏠 Welcome Home")
        st.write(f"Hello, **{st.session_state.user}** 👋")

        # --- Overview Section ---
        st.subheader("🌐 Overview")
        st.markdown("""
        **Global Balance** is a comprehensive platform to monitor and analyze global economic and financial data.  
        It provides users with real-time dashboards, profile management, and a feedback system — all in one secure and interactive environment.  

        **Why use Global Balance?**
        - Access up-to-date financial reports and statistics.  
        - Understand global economic patterns through visualizations.  
        - Manage your user profile securely and efficiently.  
        - Share feedback to improve the platform and community engagement.
        """)

        # --- Features Section ---
        st.subheader("✨ Features")
        st.markdown("""
        1. **Interactive Dashboards** 📊  
           View global financial metrics, trends, and income inequality data using embedded Power BI dashboards.  
           Provides intuitive charts and tables for better insights.

        2. **Profile Management** 👤  
           Maintain and update your account information.  
           Customize settings and monitor your activity securely.

        3. **Feedback Portal** 💬  
           Share suggestions, report issues, or provide ideas to enhance the platform.  
           Feedback is acknowledged and valued for continuous improvement.

        4. **Secure Login & Signup** 🔐  
           Passwords are hashed and securely stored.  
           Smooth and safe authentication ensures privacy and security.

        5. **Guided Navigation & Tips** 📝  
           Easily navigate between pages using the sidebar.  
           Quick tips help you make the most out of the platform.
        """)

        # --- Quick Tips Section ---
        st.subheader("📌 Quick Tips")
        st.markdown("""
        1. Use the sidebar to navigate between Home, Dashboard, Profile, and Feedback pages.  
        2. Explore the **Dashboard** for interactive visual insights.  
        3. Keep your profile updated for a personalized experience.  
        4. Share feedback to help us enhance the platform.  
        5. Highlights give you quick access to key features.
        """)


    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")

        # --- Dashboard Overview ---
        st.subheader("🌐 Dashboard Overview")
        st.markdown("""
        The dashboard provides an interactive view of **global economic and financial metrics**, including income inequality, GDP trends, and other key financial indicators.  
        It allows you to explore patterns, compare countries, and analyze trends over time.
        """)

        # --- How to Use Dashboard ---
        st.subheader("📝 How to Use")
        st.markdown("""
        - Use filters and slicers in the dashboard to customize your view by region, year, or indicators.  
        - Hover over charts and maps to see detailed data points.  
        - Export visuals for reports or presentations.  
        - Analyze trends to gain insights into global financial patterns.
        """)

        # --- Dashboard Embed ---
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Income Inequality Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)

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
