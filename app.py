import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import pandas as pd
import random
import streamlit.components.v1 as components
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

st.set_page_config(page_title="Login Page", layout="centered")

# ---------------- CSS ----------------
page_bg = """
<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #1f2235;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.container {
  display: flex;
  width: 900px;
  height: 550px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.3);
  border-radius: 12px;
  overflow: hidden;
}

.left {
  flex: 1;
  background: linear-gradient(135deg, #2c3e91, #3a60d2);
  color: #fff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  text-align: center;
}

.left h1 {
  font-size: 26px;
  margin-bottom: 10px;
}

.left p {
  margin-bottom: 20px;
}

.left button {
  padding: 12px 30px;
  background: #00d1ff;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.left button:hover {
  background: #00a8cc;
}

.right {
  flex: 1;
  background: #2a2c3a;
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: #fff;
}

.right h2 {
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 14px;
  margin-bottom: 6px;
  color: #ccc;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 6px;
  background: #1c1e2a;
  color: #fff;
  font-size: 14px;
}

.form-group input:focus {
  outline: 2px solid #00d1ff;
}

.btn {
  padding: 12px;
  width: 100%;
  border: none;
  border-radius: 6px;
  background: #00d1ff;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.btn:hover {
  background: #00a8cc;
}

.small-text {
  margin-top: 15px;
  font-size: 12px;
  color: #aaa;
}

.small-text a {
  color: #00d1ff;
  text-decoration: none;
}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- HTML ----------------
html_code = """
<div class="container">
  <!-- Left side (Sign Up) -->
  <div class="left">
    <h1>Hello! Welcome to the ArBitrage trading platform</h1>
    <p>Don’t have an account yet?</p>
    <button onclick="alert('Redirecting to signup page...')">Sign Up</button>
  </div>

  <!-- Right side (Sign In) -->
  <div class="right">
    <h2>Sign In</h2>
    <form>
      <div class="form-group">
        <label for="login">Login or Email</label>
        <input type="text" id="login" placeholder="Enter your login or email" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" placeholder="Enter your password" required>
      </div>
      <button type="submit" class="btn">Sign In</button>
    </form>
    <p class="small-text">
      By clicking "Sign Up" button, you agree to our <a href="#">Terms & Conditions</a>.
    </p>
  </div>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)

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
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

def switch_tab(tab):
    st.session_state.auth_mode = tab

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
                     st.rerun()
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





