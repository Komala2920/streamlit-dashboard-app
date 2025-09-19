import streamlit as st

st.set_page_config(page_title="Animated Login System", layout="wide")

# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------
# LOGIN PAGE
# -------------------------
def login_ui():
    st.markdown(
        """
        <style>
        .login-box {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            max-width: 400px;
            margin: auto;
            text-align: center;
        }
        .login-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #20c997;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Sign In</div>', unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if email and password:   # simple check (replace with DB check later)
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Please enter email and password")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# DASHBOARD UI
# -------------------------
def dashboard_ui():
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Go to:", ["Home", "Dashboard", "Profile", "Feedback", "Logout"])
    st.session_state.page = choice

    if choice == "Home":
        st.title("🏠 Home")
        st.write("Welcome to the Home Page!")

    elif choice == "Dashboard":
        st.title("📊 Dashboard")
        st.write("Your dashboard content goes here.")

    elif choice == "Profile":
        st.title("👤 Profile")
        st.write("User profile details displayed here.")

    elif choice == "Feedback":
        st.title("💬 Feedback")
        feedback = st.text_area("Enter your feedback here:")
        if st.button("Submit"):
            st.success("Thanks for your feedback!")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.rerun()

# -------------------------
# MAIN APP
# -------------------------
if not st.session_state.logged_in:
    login_ui()
else:
    dashboard_ui()
