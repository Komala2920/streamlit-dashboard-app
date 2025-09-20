import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import pandas as pd
import subprocess
import sys

# Function to install a package if missing
def install_package(package):
    try:
        __import__(package)
    except ModuleNotFoundError:
        st.warning(f"⚠️ {package} not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        st.success(f"✅ {package} installed! Please rerun the app.")
        st.stop()

# Ensure Plotly is installed
install_package("plotly")

# Now safe to import Plotly
import plotly.express as px


# ---------------------- DATABASE ----------------------
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS feedback(username TEXT, rating INTEGER, usability TEXT, comment TEXT, suggestions TEXT)')
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

# ---------------------- CSS STYLING ----------------------
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    font-family: 'Segoe UI', sans-serif;
    color: #f1f5f9;
}
.stButton>button {
    background: #0ea5e9;
    color: #fff;
    border-radius: 12px;
    padding: 0.7em 1.5em;
    border: none;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: #0284c7;
    transform: translateY(-2px);
}
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}
h1, h2, h3, h4 {
    color: #f1f5f9;
}
.stText, p {
    color: #e2e8f0;
}
.css-1emrehy.edgvbvh3 button {
    width: 100% !important;
    min-width: 100% !important;
    max-width: 100% !important;
    height: 55px !important;
    margin-bottom: 12px;
    font-size: 16px;
    border-radius: 12px;
    background-color: #0ea5e9;
    color: #fff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
.css-1emrehy.edgvbvh3 button:hover {
    background-color: #0284c7;
}
iframe {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- SESSION ----------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------- LOGIN / SIGNUP ----------------------
if st.session_state.user is None:
    st.markdown("<h1 style='text-align:center; color:#38bdf8;'>Global Balance</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In"):
            user = check_user(username, password)
            if user:
                st.session_state.user = username
                st.session_state.page = "Home"
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

# ---------------------- DASHBOARD APP ----------------------
else:
    # --- Sidebar Navigation ---
    st.sidebar.title("🌐 Global Balance")
    nav_items = ["🏠 Home", "📊 Dashboard", "👤 Profile", "💬 Feedback", "🚪 Logout"]
    for item in nav_items:
        if st.sidebar.button(item):
            if item == "🚪 Logout":
                st.session_state.user = None
                st.session_state.page = "Home"
                st.success("🚪 You have been logged out.")
            else:
                st.session_state.page = item

    # --- Top Bar ---
    st.markdown("""
    <div style='background-color:#0f172a; padding:10px; color:#38bdf8; font-size:22px; font-weight:bold; text-align:center'>
        Global Balance Dashboard
    </div>
    """, unsafe_allow_html=True)

    # ---------------------- HOME ----------------------
    if st.session_state.page == "🏠 Home":
        st.header(f"🏠 Welcome, {st.session_state.user} 👋")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌐 Overview")
        st.markdown("""
        Global Balance lets you monitor global economic and financial data.
        Interactive dashboards, profile management, and feedback all in one professional environment.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("✨ Features")
        st.markdown("""
        - Interactive Dashboards 📊  
        - Profile Management 👤  
        - Feedback Portal 💬  
        - Secure Login & Signup 🔐  
        - Quick Navigation Tips 📝
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Quick Tips")
        st.markdown("""
        Use sidebar to navigate. Explore dashboards for insights. Keep profile updated. Submit feedback for improvements.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------- DASHBOARD ----------------------
    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")

        # KPI Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Total GDP", "44 Trillion", "+2.5%")
        col2.metric("Total Population", "3.8 Billion", "+0.8%")
        col3.metric("Countries Tracked", 195, "0")

        # Charts with Plotly fallback
        try:
            import plotly.express as px
            df = pd.DataFrame({
                "Country": ["USA", "India", "China", "Germany", "UK"],
                "GDP": [21, 2.9, 14, 4.2, 2.8],
                "Population": [331, 1380, 1441, 83, 68]
            })

            st.subheader("GDP by Country")
            fig = px.bar(df, x="Country", y="GDP", color="Country", text="GDP")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Population Distribution")
            fig2 = px.pie(df, names="Country", values="Population", color="Country")
            st.plotly_chart(fig2, use_container_width=True)

        except ModuleNotFoundError:
            st.warning("⚠️ Plotly is not installed. Install Plotly to see interactive charts.")

        # Embedded Power BI
        st.subheader("🌐 Income Inequality Dashboard")
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Income Inequality Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)

    # ---------------------- PROFILE ----------------------
    elif st.session_state.page == "👤 Profile":
        st.header("👤 Edit Profile")
        col1, col2 = st.columns([1,3])
        with col1:
            st.image("https://via.placeholder.com/120", width=120)
            st.text(st.session_state.user)
        with col2:
            with st.form("profile_form"):
                first_name = st.text_input("First Name", "Arthur")
                last_name = st.text_input("Last Name", "Nancy")
                email = st.text_input("Email", "user@example.com")
                password = st.text_input("Password", "********", type="password")
                submitted = st.form_submit_button("💾 Save")
                if submitted:
                    st.success("✅ Profile updated successfully!")

    # ---------------------- FEEDBACK ----------------------
    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        with st.form("feedback_form"):
            col1, col2 = st.columns(2)
            with col1:
                rating = st.slider("Rate your experience", 1, 5, 5)
                usability = st.selectbox("Ease of use", ["Very Easy", "Easy", "Neutral", "Difficult", "Very Difficult"])
            with col2:
                comment = st.text_area("Your comments")
                suggestions = st.text_area("Suggestions / Feature Requests")
            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                c.execute(
                    "INSERT INTO feedback(username, rating, usability, comment, suggestions) VALUES (?, ?, ?, ?, ?)",
                    (st.session_state.user, rating, usability, comment, suggestions)
                )
                conn.commit()
                st.success("✅ Feedback submitted!")

        st.subheader("📋 Your Previous Feedback")
        c.execute("SELECT rating, usability, comment, suggestions FROM feedback WHERE username=?", (st.session_state.user,))
        rows = c.fetchall()
        if rows:
            df_feedback = pd.DataFrame(rows, columns=["Rating","Usability","Comment","Suggestions"])
            st.dataframe(df_feedback)
        else:
            st.info("You haven't submitted any feedback yet.")

