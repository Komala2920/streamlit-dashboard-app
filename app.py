import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import pandas as pd
import random
import requests
import os

# ---------------------- OPTIONAL CHATBOT ----------------------
try:
    import openai
    OPENAI_AVAILABLE = True
    # For real deployment, set your API key here or via environment variable
    # openai.api_key = "YOUR_OPENAI_API_KEY"
except ModuleNotFoundError:
    OPENAI_AVAILABLE = False


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
def st_lottie_url(url: str, height: int = 300, key: str = None):
    lottie_html = f"""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <lottie-player src="{url}"  background="transparent"  speed="1"
                   style="width:100%; height:{height}px;" loop autoplay></lottie-player>
    """
    components.html(lottie_html, height=height + 50)

# ---------------------- GLOBAL CSS ----------------------
st.markdown("""
<style>
.stApp { 
    background: linear-gradient(to bottom right, #0f172a, #1e293b) !important;
    font-family: 'Segoe UI', sans-serif;
    color: #f1f5f9;
}

/* Login/Signup container */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: stretch;
    width: 100%;
    max-width: 950px;
    margin: 40px auto;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

/* Left (Sign Up) */
.auth-left {
    flex: 1;
    background: #1e293b;
    padding: 50px 30px;
    text-align: center;
}
.auth-left h2 {
    font-size: 24px;
    color: #38bdf8;
    margin-bottom: 10px;
}
.auth-left button {
    margin-top: 20px;
    background: #0ea5e9 !important;
    color: #fff !important;
    font-weight: 600;
    border-radius: 12px;
    padding: 10px 20px;
}

/* Right (Login) */
.auth-right {
    flex: 1;
    background: #0f172a;
    padding: 50px 40px;
}
.auth-right h2 {
    font-size: 24px;
    color: #38bdf8;
    margin-bottom: 20px;
}
.stButton>button {
    background: #0ea5e9;
    color: #fff;
    border-radius: 12px;
    padding: 0.7em 1.5em;
    border: none;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: #0284c7;
    transform: translateY(-2px);
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
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------- LOGIN / SIGNUP ----------------------
if st.session_state.user is None and st.session_state.page not in ["forgot_password"]:
    st.markdown("<div style='text-align:center; font-size:32px; font-weight:bold; color:#38bdf8;'>Global Balance</div>", unsafe_allow_html=True)

    st.markdown('<div class="auth-container">', unsafe_allow_html=True)

    # Left side - Sign Up
    st.markdown('<div class="auth-left">', unsafe_allow_html=True)
    st.markdown("<h2>Hello! Welcome to Global Balance</h2>", unsafe_allow_html=True)
    st.write("Don’t have an account yet?")
    new_user = st.text_input("Choose Username", key="signup_user")
    new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
    email = st.text_input("Email", key="signup_email")
    if st.button("Sign Up"):
        if new_user and new_pass and email:
            add_user(new_user, new_pass, email)
            st.success("✅ Account created. Now login.")
        else:
            st.error("⚠ Please enter valid details.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Right side - Login
    st.markdown('<div class="auth-right">', unsafe_allow_html=True)
    st.markdown("<h2>Sign In</h2>", unsafe_allow_html=True)
    username = st.text_input("Login or Email", key="login_user")
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
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

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

   # --------Sidebar Navigation ---------
    st.sidebar.title("Navigation")
    top_items = ["🏠 Home", "📊 Dashboard", "👤 Profile", "💬 Feedback", "🤖 Chatbot" ]
    for item in top_items:
        if st.sidebar.button(item, key=item):
            st.session_state.page = item
    # Add a spacer to push Logout to the bottom
    st.sidebar.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)

    # Bottom section (Logout)
    if st.sidebar.button("🚪 Logout", key="logout_sidebar"):
        st.session_state.user = None
        st.session_state.page = "🏠 Home"
        st.success("🚪 You have been logged out.")

    # --- Home Page ---
    if st.session_state.page == "🏠 Home":
        st.header("🏠 Welcome Home")
        st.write(f"Hello, {st.session_state.user} 👋")

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
        st.title("📊 Dashboard")
        st.write("This is your dashboard with analytics and reports.")
        st_lottie_url("https://assets2.lottiefiles.com/packages/lf20_49rdyysj.json", height=200)
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
        st_lottie_url("https://assets1.lottiefiles.com/packages/lf20_jtbfg2nb.json", height=200)
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
        # --- Robot Lottie 1 ---
        st_lottie_url("https://assets9.lottiefiles.com/packages/lf20_9wpyhdzo.json", height=200)

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

   # ---------------------- Chatbot Page ----------------------
    elif st.session_state.page == "🤖 Chatbot":
        st.header("🤖 Chatbot")

        # --- Lottie Animation ---
        st_lottie_url("https://assets2.lottiefiles.com/packages/lf20_1pxqjqps.json", height=200)
       
        # Initialize chat history if not exists
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

        # Display chat history
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.markdown(f"**You:** {chat['content']}")
            else:
                st.markdown(f"**Bot:** {chat['content']}")

    # User input only on Chatbot page
    user_input = st.text_input("Type your message here:", key="chat_input")
    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            # Demo or OpenAI bot reply
            if OPENAI_AVAILABLE:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=st.session_state.chat_history
                    )
                    bot_reply = response.choices[0].message["content"]
                except Exception as e:
                    bot_reply = f"(Error calling OpenAI API: {str(e)})"
            else:
                # Demo chatbot responses
                msg = user_input.lower()
                if "hello" in msg or "hi" in msg:
                    bot_reply = "Hello! How can I help you today?"
                elif "how are you" in msg:
                    bot_reply = "I'm just a bot, but I'm doing great! 😄"
                else:
                    bot_reply = "I'm not sure about that, but I'm learning every day! 🤖"

            st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
            st.rerun()                           
