import streamlit as st
import base64

st.set_page_config(page_title="Animated Login System", layout="wide")

# ---------------- BACKGROUND SETUP ----------------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Optional: uncomment and set your background
# set_background("background.png")

# ---------------- LOGIN / SIGNUP UI ----------------
def login_signup_ui():
    st.markdown("<h2 style='text-align:center; color:white;'>🌟 Animated Login System 🌟</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Sign In")
        email = st.text_input("Email", key="signin_email")
        password = st.text_input("Password", type="password", key="signin_password")
        if st.button("Login", key="signin_btn"):
            if email and password:
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("Please enter email and password")

    with col2:
        st.subheader("Create Account")
        name = st.text_input("Name", key="signup_name")
        email_su = st.text_input("Email", key="signup_email")
        password_su = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up", key="signup_btn"):
            if name and email_su and password_su:
                st.success("✅ Account created successfully! Please login.")
            else:
                st.error("Fill all fields to sign up")

# ---------------- DASHBOARD PAGES ----------------
def home_page():
    st.title("🏠 Home")
    st.write("Welcome to the Home page!")

def dashboard_page():
    st.title("📊 Dashboard")
    st.write("This is the dashboard.")

def profile_page():
    st.title("👤 Profile")
    st.write("Your profile details go here.")

def feedback_page():
    st.title("💬 Feedback")
    st.text_area("Enter your feedback here:")

# ---------------- MAIN APP ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

if not st.session_state.logged_in:
    login_signup_ui()
else:
    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("🏠 Home"): st.session_state.page = "Home"
    if st.sidebar.button("📊 Dashboard"): st.session_state.page = "Dashboard"
    if st.sidebar.button("👤 Profile"): st.session_state.page = "Profile"
    if st.sidebar.button("💬 Feedback"): st.session_state.page = "Feedback"
    if st.sidebar.button("🚪 Logout"): st.session_state.logged_in = False

    # Render pages
    if st.session_state.page == "Home": home_page()
    elif st.session_state.page == "Dashboard": dashboard_page()
    elif st.session_state.page == "Profile": profile_page()
    elif st.session_state.page == "Feedback": feedback_page()
