import streamlit as st
import sqlite3
import hashlib
import streamlit.components.v1 as components
import os

# ---------------------- DATABASE ----------------------
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users(
        username TEXT,
        password TEXT,
        firstname TEXT,
        lastname TEXT,
        email TEXT,
        profile_pic TEXT
    )
''')
conn.commit()

# ---------------------- UTILS -------------------------
def make_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, make_hash(password)))
    return c.fetchone()

def add_user(username, password):
    c.execute('INSERT INTO users(username, password, firstname, lastname, email, profile_pic) VALUES (?, ?, ?, ?, ?, ?)',
              (username, make_hash(password), "", "", "", None))
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

        # Overview Section
        st.subheader("🌐 Overview")
        st.markdown("""
        **Global Balance** is a comprehensive platform to monitor and analyze global economic and financial data.  
        It provides users with real-time dashboards, profile management, and a feedback system — all in one secure and interactive environment.  
        """)

    elif st.session_state.page == "📊 Dashboard":
        st.header("📊 Dashboard")
        st.subheader("🌐 Dashboard Overview")
        st.markdown("Explore interactive financial data with Power BI.")
        dashboard_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.html(f"""
            <iframe title="Global Income Inequality Dashboard" width="100%" height="600" 
            src="{dashboard_url}" frameborder="0" allowFullScreen="true"></iframe>
        """, height=620)

    elif st.session_state.page == "👤 Profile":
        st.header("👤 Profile Management")

        # Load user info
        c.execute("SELECT firstname, lastname, email, profile_pic FROM users WHERE username=?", (st.session_state.user,))
        user_data = c.fetchone()
        if user_data:
            first_name, last_name, email, profile_pic = user_data
        else:
            first_name, last_name, email, profile_pic = "", "", "", None

        tab1, tab2, tab3 = st.tabs(["Profile Info", "Change Password", "Preferences"])

        # --- Profile Info ---
        with tab1:
            if profile_pic and os.path.exists(profile_pic):
                st.image(profile_pic, width=120, caption="Current Profile Picture")
                if st.button("🗑️ Remove Profile Picture"):
                    try:
                        os.remove(profile_pic)
                    except:
                        pass
                    profile_pic = None
                    c.execute("UPDATE users SET profile_pic=? WHERE username=?", (None, st.session_state.user))
                    conn.commit()
                    st.success("✅ Profile picture removed!")
            else:
                st.info("No profile picture uploaded")

            uploaded_pic = st.file_uploader("Upload New Profile Picture", type=["jpg", "jpeg", "png"])
            if uploaded_pic:
                os.makedirs("profile_pics", exist_ok=True)
                pic_path = os.path.join("profile_pics", f"{st.session_state.user}_{uploaded_pic.name}")
                with open(pic_path, "wb") as f:
                    f.write(uploaded_pic.getbuffer())
                profile_pic = pic_path
                st.image(profile_pic, width=120, caption="Preview")

            new_first = st.text_input("First Name", value=first_name)
            new_last = st.text_input("Last Name", value=last_name)
            new_email = st.text_input("Email", value=email)

            if st.button("💾 Save Profile"):
                c.execute("UPDATE users SET firstname=?, lastname=?, email=?, profile_pic=? WHERE username=?",
                          (new_first, new_last, new_email, profile_pic, st.session_state.user))
                conn.commit()
                st.success("✅ Profile updated successfully!")

        # --- Change Password ---
        with tab2:
            current_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm New Password", type="password")

            if st.button("🔑 Update Password"):
                c.execute("SELECT password FROM users WHERE username=?", (st.session_state.user,))
                db_pass = c.fetchone()
                if db_pass and make_hash(current_pass) == db_pass[0]:
                    if new_pass == confirm_pass and new_pass.strip() != "":
                        c.execute("UPDATE users SET password=? WHERE username=?", (make_hash(new_pass), st.session_state.user))
                        conn.commit()
                        st.success("✅ Password updated successfully!")
                    else:
                        st.error("⚠️ New passwords do not match or empty")
                else:
                    st.error("❌ Current password is incorrect")

        # --- Preferences ---
        with tab3:
            theme = st.radio("Theme", ["Light", "Dark"], horizontal=True)
            language = st.selectbox("Language", ["English", "తెలుగు", "हिन्दी"])
            notifications = st.checkbox("Enable Email Notifications", value=True)

            if st.button("⚙️ Save Preferences"):
                st.success(f"✅ Preferences saved! (Theme: {theme}, Language: {language}, Notifications: {notifications})")

    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")
        feedback = st.text_area("Write your feedback:")
        if st.button("Submit Feedback"):
            st.success("✅ Thanks for your feedback!")
