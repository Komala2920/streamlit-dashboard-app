import streamlit as st
import base64

# -------------------------
# PAGE CONFIG (must be first)
# -------------------------
st.set_page_config(page_title="Animated Login System", layout="wide")

# -------------------------
# BACKGROUND IMAGE SETUP
# -------------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def set_background(base64_str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpeg;base64,{base64_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .login-title {{
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 1rem;
            text-align: center;
            color: #003366; /* Dark Blue */
        }}
        .switch-link {{
            color: #007bff;
            cursor: pointer;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Load and apply background
bg_image = get_base64_image("background.jpeg")
set_background(bg_image)

# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "Login"

# -------------------------
# LOGIN / SIGN UP UI
# -------------------------
def auth_ui():
    if st.session_state.auth_mode == "Login":
        st.markdown('<div class="login-title">🔐 Sign In</div>', unsafe_allow_html=True)
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if email and password:
                st.session_state.logged_in = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Please enter email and password")

        if st.button("Don't have an account? Sign Up"):
            st.session_state.auth_mode = "Sign Up"
            st.rerun()

    else:
        st.markdown('<div class="login-title">📝 Sign Up</div>', unsafe_allow_html=True)
        new_email = st.text_input("Email")
        new_password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Create Account", use_container_width=True):
            if new_email and new_password and confirm_password:
                if new_password == confirm_password:
                    st.success("Account created successfully! Please log in.")
                    st.session_state.auth_mode = "Login"
                    st.rerun()
                else:
                    st.error("Passwords do not match.")
            else:
                st.error("Please fill in all fields.")

        if st.button("Already have an account? Login"):
            st.session_state.auth_mode = "Login"
            st.rerun()

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
        st.session_state.auth_mode = "Login"
        st.rerun()

# -------------------------
# MAIN APP
# -------------------------
if not st.session_state.logged_in:
    auth_ui()
else:
    dashboard_ui()
