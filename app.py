import streamlit as st
import base64

st.set_page_config(page_title="Animated Login System", layout="wide")

# ---------------- BACKGROUND SETUP ----------------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(gif_file):
    bin_str = get_base64(gif_file)
    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background: url("data:image/gif;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Set animated GIF background
set_background("/mnt/data/Web Design Trends That Will Dominate In 2019 _ B3 Multimedia Solutions.gif")

# ---------------- LOGIN / SIGNUP UI ----------------
def login_signup_ui():
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "signin"

    st.markdown(
        """
        <style>
        .container {
            width: 800px;
            height: 450px;
            margin: 60px auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
            position: relative;
        }
        .slider {
            display: flex;
            width: 1600px; /* double container width */
            height: 100%;
            transition: transform 0.8s ease;
        }
        .panel {
            width: 800px;
            padding: 50px;
            text-align: center;
        }
        .signin { background: #20c997; color: white; }
        .signup { background: white; color: #333; }
        .stButton button {
            background: linear-gradient(45deg, #20c997, #17a2b8);
            color: white;
            border-radius: 25px;
            padding: 10px 25px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background: linear-gradient(45deg, #17a2b8, #20c997);
            transform: scale(1.05);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h2 style='text-align:center; color:white;'>🌟 Sliding Login System 🌟</h2>", unsafe_allow_html=True)

    # container with sliding effect
    transform_value = "translateX(0)" if st.session_state.auth_mode == "signin" else "translateX(-800px)"
    st.markdown(f"""
        <div class="container">
            <div class="slider" style="transform: {transform_value};">
                <div class="panel signin">
                    <h2>Welcome Back 👋</h2>
                    <p>Please login with your credentials</p>
                </div>
                <div class="panel signup">
                    <h2>Create Account ✨</h2>
                    <p>Join us by creating a new account</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- Streamlit form inputs ---
    if st.session_state.auth_mode == "signin":
        email = st.text_input("Email", key="signin_email")
        password = st.text_input("Password", type="password", key="signin_password")
        if st.button("Login", key="signin_btn"):
            if email and password:
                st.session_state.logged_in = True
                st.success("✅ Logged in successfully!")
            else:
                st.error("Please enter email and password")
        if st.button("➡️ Go to Sign Up"):
            st.session_state.auth_mode = "signup"

    else:  # signup mode
        name = st.text_input("Name", key="signup_name")
        email_su = st.text_input("Email", key="signup_email")
        password_su = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up", key="signup_btn"):
            if name and email_su and password_su:
                st.success("✅ Account created successfully! Please login.")
            else:
                st.error("Fill all fields to sign up")
        if st.button("⬅️ Back to Sign In"):
            st.session_state.auth_mode = "signin"


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
    st.sidebar.title("Navigation")
    if st.sidebar.button("🏠 Home"): st.session_state.page = "Home"
    if st.sidebar.button("📊 Dashboard"): st.session_state.page = "Dashboard"
    if st.sidebar.button("👤 Profile"): st.session_state.page = "Profile"
    if st.sidebar.button("💬 Feedback"): st.session_state.page = "Feedback"
    if st.sidebar.button("🚪 Logout"): st.session_state.logged_in = False

    if st.session_state.page == "Home": home_page()
    elif st.session_state.page == "Dashboard": dashboard_page()
    elif st.session_state.page == "Profile": profile_page()
    elif st.session_state.page == "Feedback": feedback_page()
