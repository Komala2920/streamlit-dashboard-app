import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import pandas as pd

# ---------------------- DATABASE ----------------------
conn = sqlite3.connect('users.db', check_same_thread=False)
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

# ---------------------- PROFESSIONAL CSS ----------------------
st.markdown("""
<style>
/* Background */
body {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
    font-family: 'Segoe UI', sans-serif;
    color: #f1f5f9;
}

/* Buttons */
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

/* Cards */
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* Headers */
h1, h2, h3, h4 {
    color: #f1f5f9;
}

/* Text */
.stText, p {
    color: #e2e8f0;
}

/* Sidebar Buttons */
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

/* Iframe Styling */
iframe {
    border-radius: 12px;
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
    st.markdown("<div style='text-align:center; font-size:32px; font-weight:bold; color:#38bdf8; margin-bottom:20px'>Global Balance</div>", unsafe_allow_html=True)
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
    st.markdown("<div style='text-align:center; font-size:32px; font-weight:bold; color:#38bdf8; margin-bottom:20px'>Global Balance</div>", unsafe_allow_html=True)

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

    # --- Home Page ---
    if st.session_state.page == "🏠 Home":
        st.header("🏠 Welcome Home")
        st.write(f"Hello, *{st.session_state.user}* 👋")

        # Overview Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌐 Overview")
        st.markdown("""
        *Global Balance* is a comprehensive platform to monitor and analyze global economic and financial data.  
        Real-time dashboards, profile management, and feedback system in a professional, secure environment.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Features Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("✨ Features")
        st.markdown("""
        1. *Interactive Dashboards* 📊  
        2. *Profile Management* 👤  
        3. *Feedback Portal* 💬  
        4. *Secure Login & Signup* 🔐  
        5. *Guided Navigation & Tips* 📝
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Quick Tips Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Quick Tips")
        st.markdown("""
        1. Use the sidebar to navigate between Home, Dashboard, Profile, and Feedback pages.  
        2. Explore the *Dashboard* for interactive visual insights.  
        3. Keep your profile updated for a personalized experience.  
        4. Share feedback to help us enhance the platform.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Dashboard Page ---
    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")
        st.subheader("🌐 Overview")
        st.markdown("""
        The dashboard provides an interactive view of *global economic and financial metrics*, including income inequality, GDP trends, and other key financial indicators.  
        """)

        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Income Inequality Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)

    # --- Profile Page ---
    elif st.session_state.page == "👤 Profile":
        st.header("👤 Edit Profile")
        with st.container():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image("https://via.placeholder.com/120", width=120)
                st.text(st.session_state.user)
            with col2:
                with st.form("profile_form"):
                    col_left, col_right = st.columns(2)
                    with col_left:
                        first_name = st.text_input("First Name")
                        password = st.text_input("Password",type="password")
                        gender = st.selectbox("Gender", ["Male", "Female", "Other","Select a Option"], index=0)
                    with col_right:
                        last_name = st.text_input("Last Name")
                        email = st.text_input("Email")
                        dob = st.date_input("Date of Birth", min_value=pd.to_datetime("2000-01-01"), max_value=pd.to_datetime("2025-12-31"))
                        language = st.selectbox("Language", ["English", "Spanish", "French","Select a Option"], index=0)
                        linkedin = st.text_input("LinkedIn")
                    submitted = st.form_submit_button("💾 Save")
                    if submitted:
                        st.success("✅ Profile updated successfully!")

    # --- Feedback Page ---
    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        st.markdown("We value your feedback! Please share your thoughts to help us improve *Global Balance*.")

        with st.form("feedback_form"):
            col1, col2 = st.columns(2)
            with col1:
                rating = st.slider("Rate your experience", 1, 5, 5)
                usability = st.selectbox(
                    "How easy was it to use the platform?", 
                    ["Very Easy", "Easy", "Neutral", "Difficult", "Very Difficult"], 
                    index=1
                )
            with col2:
                comment = st.text_area("Your comments", placeholder="Write your feedback here...")
                suggestions = st.text_area("Suggestions / Feature Requests", placeholder="Any ideas or features you want?")

            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                c.execute("""
                    CREATE TABLE IF NOT EXISTS feedback(
                        username TEXT, 
                        rating INTEGER, 
                        usability TEXT, 
                        comment TEXT, 
                        suggestions TEXT
                    )
                """)
                c.execute(
                    "INSERT INTO feedback(username, rating, usability, comment, suggestions) VALUES (?, ?, ?, ?, ?)",
                    (st.session_state.user, rating, usability, comment, suggestions)
                )
                conn.commit()
                st.success("✅ Thank you! Your feedback has been submitted.")

        # Show previous feedback
        st.subheader("📋 Your Previous Feedback")
        c.execute("SELECT rating, usability, comment, suggestions FROM feedback WHERE username=?", (st.session_state.user,))
        rows = c.fetchall()
        if rows:
            feedback_df = pd.DataFrame(rows, columns=["Rating", "Usability", "Comment", "Suggestions"])
            st.dataframe(feedback_df)
        else:
            st.info("You haven't submitted any feedback yet.")                  



