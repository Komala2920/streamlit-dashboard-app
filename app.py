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
    st.info(f"(Demo) OTP sent to {email}: *{otp}*")
    return True

# ---------------------- PROFESSIONAL CSS ----------------------
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
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    margin: 0 auto;
    width: 80%;
    max-width: 900px;
}
.big-input input, .big-input select, .big-input textarea {
    height: 50px !important;
    font-size: 16px !important;
    border-radius: 10px !important;
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

    # --- Profile Page ---
    if st.session_state.page == "👤 Profile":
        st.header("👤 Edit Profile")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("profile_form"):
            col_left, col_right = st.columns(2)
            with col_left:
                first_name = st.text_input("First Name", key="first", placeholder="Enter first name")
                gender = st.selectbox("Gender", ["Select a Option","Male", "Female", "Other"], index=0, key="gender")
            with col_right:
                last_name = st.text_input("Last Name", key="last", placeholder="Enter last name")
                email = st.text_input("Email", key="email", placeholder="Enter email")
                linkedin = st.text_input("LinkedIn", key="linkedin", placeholder="Enter LinkedIn URL")
            submitted = st.form_submit_button("💾 Save")
            if submitted:
                st.success("✅ Profile updated successfully!")
        st.markdown('</div>', unsafe_allow_html=True)

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
