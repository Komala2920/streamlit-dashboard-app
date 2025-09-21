import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import pandas as pd
import smtplib
import random

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
    # ⚠️ Replace with real email sending logic
    # Demo: OTP will be displayed on screen
    st.info(f"(Demo) OTP sent to {email}: **{otp}**")
    return True

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

    # --- Dashboard Page ---
    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")
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
                # Removed image and username text
                pass  
            with col2:
                with st.form("profile_form"):
                    col_left, col_right = st.columns(2)
                    with col_left:
                        first_name = st.text_input("First Name")
                        gender = st.selectbox("Gender", ["Select a Option","Male", "Female", "Other"], index=0)
                    with col_right:
                        last_name = st.text_input("Last Name")
                        email = st.text_input("Email")
                        linkedin = st.text_input("LinkedIn")
                    submitted = st.form_submit_button("💾 Save")
                    if submitted:
                        st.success("✅ Profile updated successfully!")

        # --- Password Management Section ---
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
                    # Directly update password (no current password check)
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

        # Show previous feedback
        st.subheader("📋 Your Previous Feedback")
        c.execute("SELECT rating, usability, comment, suggestions FROM feedback WHERE username=?", (st.session_state.user,))
        rows = c.fetchall()
        if rows:
            feedback_df = pd.DataFrame(rows, columns=["Rating", "Usability", "Comment", "Suggestions"])
            st.dataframe(feedback_df)
        else:
            st.info("You haven't submitted any feedback yet.")
