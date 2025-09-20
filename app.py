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
         st.header("👤 Edit Profile")

    # --- Profile Card ---
    with st.container():
        col1, col2 = st.columns([1, 3])

        with col1:
            st.image("https://via.placeholder.com/120", width=120)  # Profile Picture
            st.text(st.session_state.user)  # logged-in username

        with col2:
            with st.form("profile_form"):
                col_left, col_right = st.columns(2)

                with col_left:
                    first_name = st.text_input("First Name", "Arthur")
                    password = st.text_input("Password", "********", type="password")
                    phone = st.text_input("Phone", "477-046-1827")
                    nation = st.text_input("Nation", "Colombia")
                    gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=0)
                    twitter = st.text_input("Twitter", "twitter.com/envato")
                    facebook = st.text_input("Facebook", "facebook.com/envato")

                with col_right:
                    last_name = st.text_input("Last Name", "Nancy")
                    email = st.text_input("Email", "user@example.com")
                    address = st.text_input("Address", "116 Jaskolski Stravenue Suite 883")
                    import pandas as pd
                    dob = st.date_input(
                        "Date of Birth",
                        min_value=pd.to_datetime("2000-01-01"),
                        max_value=pd.to_datetime("2025-12-31")
                    )
                    language = st.selectbox("Language", ["English", "Spanish", "French"], index=0)
                    linkedin = st.text_input("LinkedIn", "linkedin.com/envato")
                    google = st.text_input("Google", "zachary Ruiz")

                slogan = st.text_input("Slogan", "Land acquisition Specialist")

                submitted = st.form_submit_button("💾 Save")
                if submitted:
                    st.success("✅ Profile updated successfully!")


    elif st.session_state.page == "💬 Feedback":
        st.header("💬 Feedback")

        st.markdown("""
        We value your feedback! Please share your thoughts to help us improve **Global Balance**.
        """)

        with st.form("feedback_form"):
            # Columns for layout
            col1, col2 = st.columns(2)

            with col1:
                rating = st.slider("Rate your experience", 1, 5, 5)  # 1-5 stars
                usability = st.selectbox("How easy was it to use the platform?", 
                                         ["Very Easy", "Easy", "Neutral", "Difficult", "Very Difficult"], index=1)
            with col2:
                comment = st.text_area("Your comments", placeholder="Write your feedback here...")
                suggestions = st.text_area("Suggestions / Feature Requests", placeholder="Any ideas or features you want?")

            submitted = st.form_submit_button("Submit Feedback")
            if submitted:
                # Create feedback table if it doesn't exist
                c.execute(
                    "CREATE TABLE IF NOT EXISTS feedback(username TEXT, rating INTEGER, usability TEXT, comment TEXT, suggestions TEXT)"
                )
                # Insert feedback into table
                c.execute(
                    "INSERT INTO feedback(username, rating, usability, comment, suggestions) VALUES (?, ?, ?, ?, ?)",
                    (st.session_state.user, rating, usability, comment, suggestions)
                )
                conn.commit()
                st.success("✅ Thank you! Your feedback has been submitted.")

