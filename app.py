import streamlit as st

st.set_page_config(page_title="Manual Login Dashboard", layout="wide")

# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------
# LOGIN UI (Manual with Streamlit inputs)
# -------------------------
def login_ui():
    st.title("🔑 Login System")

    st.subheader("Sign In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # ✅ Hardcoded credentials (can be replaced with DB later)
        if email == "admin@gmail.com" and password == "12345":
            st.session_state.logged_in = True
            st.session_state.page = "Home"
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid email or password")

    st.divider()

    st.subheader("Sign Up (Demo)")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Sign Up"):
        # This doesn’t save users permanently (demo only)
        st.success(f"User {new_email} registered successfully!")

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
        if st.button("Submit Feedback"):
            st.success("Thanks for your feedback!")

    elif choice == "Logout":
        st.session_state.logged_in = False
        st.success("Logged out successfully!")
        st.rerun()

# -------------------------
# MAIN APP
# -------------------------
if not st.session_state.logged_in:
    login_ui()
else:
    dashboard_ui()
