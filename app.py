import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import pandas as pd
import random
from streamlit_lottie import st_lottie
import requests

# ---------------------- DATABASE ----------------------
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, email TEXT)',)
conn.commit()

# ---------------------- UTILS -------------------------
def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, make_hash(password)))
    return c.fetchone()

def add_user(username, password, email):
    c.execute('INSERT INTO users(username, password, email) VALUES (?, ?, ?)', 
              (username, make_hash(password), email))
    conn.commit()

def get_user_by_email(email):
    c.execute("SELECT username FROM users WHERE email=?", (email,))
    return c.fetchone()

def update_password(email, new_password):
    c.execute("UPDATE users SET password=? WHERE email=?", (make_hash(new_password), email))
    conn.commit()

def send_otp(email, otp):
    st.info(f"(Demo) OTP sent to {email}: *{otp}*")
    return True

# ---------------------- LOTTIE HELPER ----------------------
def load_lottie(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ---------------------- GLOBAL CSS ----------------------
st.markdown("""
<style>
/* Apply background everywhere */
.stApp { 
    background: linear-gradient(to bottom right, #0f172a, #1e293b) !important;
    font-family: 'Segoe UI', sans-serif;
    color: #f1f5f9;
}

/* Button styling */
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

/* Card design */
.card {
    background: #1e293b;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    margin-bottom: 20px;
}

/* Headings and text */
h1, h2, h3, h4, label {
    color: #f1f5f9 !important;
}
p, .stText, .stMarkdown {
    color: #e2e8f0 !important;
}

/* Input fields */
input, textarea, select {
    border-radius: 10px !important;
    padding: 8px !important;
}

/* Tabs */
.css-1emrehy.edgvbvh3 button {
    width: 100% !important;
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

/* Iframes */
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
if "otp" not in st.session_state:
    st.session_state.otp = None
if "reset_email" not in st.session_state:
    st.session_state.reset_email = None

# ---------------------- LOGIN / SIGNUP ----------------------
if st.session_state.user is None and st.session_state.page not in ["forgot_password"]:
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

        if st.button("Forgot Password?"):
            st.session_state.page = "forgot_password"
            st.experimental_rerun()

    with tab2:
        new_user = st.text_input("Choose Username", key="signup_user")
        new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
        email = st.text_input("Email", key="signup_email")
        if st.button("Register"):
            if new_user and new_pass and email:
                add_user(new_user, new_pass, email)
                st.success("✅ Account created. Now login.")
            else:
                st.error("⚠ Please enter valid details.")

# ---------------------- FORGOT PASSWORD ----------------------
elif st.session_state.page == "forgot_password":
    st.title("🔑 Forgot Password")

    email = st.text_input("Enter your registered Email")
    if st.button("Send OTP"):
        result = get_user_by_email(email)
        if result:
            otp = str(random.randint(100000, 999999))
            st.session_state.otp = otp
            st.session_state.reset_email = email
            if send_otp(email, otp):
                st.success("✅ OTP sent to your email (demo shows OTP on screen).")
        else:
            st.error("❌ Email not found in system")

    if st.session_state.otp:
        entered_otp = st.text_input("Enter OTP")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")

        if st.button("Reset Password"):
            if entered_otp == st.session_state.otp:
                if new_password == confirm_password:
                    update_password(st.session_state.reset_email, new_password)
                    st.success("✅ Password reset successfully! Please login.")
                    st.session_state.page = "login"
                    st.session_state.otp = None
                    st.session_state.reset_email = None
                    st.experimental_rerun()
                else:
                    st.error("❌ Passwords do not match")
            else:
                st.error("❌ Invalid OTP")

# ---------------------- MAIN APP ----------------------
elif st.session_state.user is not None:
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
        st.write(f"Hello, {st.session_state.user} 👋")

        # --- Lottie Animation ---
        lottie_home = load_lottie("https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json")
        st_lottie(lottie_home, height=200, key="home_animation")

        # Overview Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌐 What is Global Balance?")
        st.markdown("""
        Global Balance is a unified platform for analyzing and monitoring *global economic & financial insights*.  
        Our mission is to provide decision-makers, analysts, and researchers with the tools to visualize, compare, and understand world economies.
        
        - 📊 *Visual Dashboards*: Track real-time data  
        - 🌍 *Global Coverage*: Access multi-country insights  
        - 🔐 *Secure & Private*: Enterprise-level user authentication  
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Features Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("✨ Why Use Global Balance?")
        st.markdown("""
        1. Interactive Dashboards 📊 with filters & drill-down analysis  
        2. Profile Management 👤 to personalize your data experience  
        3. Feedback Portal 💬 for continuous improvement  
        4. Research Support 📖 providing contextual explanations  
        5. Insights & Reports 📑 downloadable in multiple formats  
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        # Tips Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("💡 Quick Tips")
        st.markdown("""
        - Use the sidebar to *switch pages* quickly  
        - Visit the Dashboard to view *interactive charts*  
        - Update your profile to stay connected with new features  
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Dashboard Page ---
    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Global Economic Dashboard")
         # --- Lottie Animation ---
        lottie_dashboard = load_lottie("https://assets9.lottiefiles.com/packages/lf20_hdy0htc1.json")
        st_lottie(lottie_dashboard, height=200, key="dashboard_animation")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🌍 Real-Time Insights")
        st.markdown("""
        The dashboard integrates *world development indicators* such as:
        - GDP Growth 📈
        - Income Inequality 📊
        - Employment & Unemployment Trends 💼
        - Regional Comparisons 🌐  
        
        Explore country-wise comparisons and global patterns directly inside the app.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Economic Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📑 How to Use?")
        st.markdown("""
        - Hover on charts to see *detailed tooltips*  
        - Use filters to analyze by *region, income group, or year*  
        - Click on visual elements to *drill down into data*  
        """)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📌 Key Highlights")
        st.markdown("""
        ✅ Emerging economies show rapid growth in the last decade  
        ✅ Developed nations display lower inequality but slower growth  
        ✅ Africa and Asia remain regions of *great potential & challenges*  
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Profile Page ---
    elif st.session_state.page == "👤 Profile":
        st.header("👤 Edit Profile")
         # --- Lottie Animation ---
        lottie_profile = load_lottie("https://assets3.lottiefiles.com/packages/lf20_iwmd6
        
        # Profile Card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("profile_form"):
            col_left, col_right = st.columns(2)
            with col_left:
                first_name = st.text_input("First Name", placeholder="Enter first name")
                username = st.text_input("Username", placeholder="Enter user name")
                gender = st.selectbox("Gender", ["Select a Option","Male", "Female", "Other"], index=0)
            with col_right:
                last_name = st.text_input("Last Name", placeholder="Enter last name")
                email = st.text_input("Email", placeholder="Enter email")
                linkedin = st.text_input("LinkedIn", placeholder="Enter LinkedIn URL")
            submitted = st.form_submit_button("💾 Save")
            if submitted:
                st.success("✅ Profile updated successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Password Management Card
        st.subheader("🔑 Password Management")
        with st.form("password_form", clear_on_submit=True):
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")
            reset_submitted = st.form_submit_button("Update Password")

            if reset_submitted:
                if not new_password or not confirm_password:
                    st.error("⚠ Please fill out all fields.")
                elif new_password != confirm_password:
                    st.error("❌ New passwords do not match.")
                else:
                    c.execute("UPDATE users SET password=? WHERE username=?", 
                              (make_hash(new_password), st.session_state.user))
                    conn.commit()
                    st.success("✅ Password updated successfully!")

    # --- Feedback Page ---
    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        with st.form("feedback_form"):
            rating = st.slider("Rate your experience", 1, 5, 5)
            usability = st.selectbox("How easy was it to use the platform?", 
                                    ["Very Easy", "Easy", "Neutral", "Difficult", "Very Difficult"], index=1)
            comment = st.text_area("Your comments")
            suggestions = st.text_area("Suggestions / Feature Requests")

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

        st.subheader("📋 Your Previous Feedback")
        c.execute("SELECT rating, usability, comment, suggestions FROM feedback WHERE username=?", (st.session_state.user,))
        rows = c.fetchall()
        if rows:
            feedback_df = pd.DataFrame(rows, columns=["Rating", "Usability", "Comment", "Suggestions"])
            st.dataframe(feedback_df)
        else:
            st.info("You haven't submitted any feedback yet.")        




