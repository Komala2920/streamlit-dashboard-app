import streamlit as st

st.set_page_config(page_title="ArBitrage Platform", layout="centered")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "login"

def navigate(page):
    st.session_state.page = page

# ---------------- CSS ----------------
page_bg = """
<style>
body {
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #1f2235;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- NAVIGATION BAR ----------------
if st.session_state.page != "login":
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: 
        if st.button("🏠 Home"): navigate("home")
    with col2: 
        if st.button("📊 Dashboard"): navigate("dashboard")
    with col3: 
        if st.button("👤 Profile"): navigate("profile")
    with col4: 
        if st.button("💬 Feedback"): navigate("feedback")
    with col5: 
        if st.button("🚪 Logout"): navigate("login")

# ---------------- PAGES ----------------
if st.session_state.page == "login":
    col1, col2 = st.columns(2)

    # Left Side (Sign Up)
    with col1:
        st.markdown("## Hello! Welcome to the ArBitrage trading platform")
        st.write("Don’t have an account yet?")
        if st.button("Sign Up", key="signup"):
            navigate("home")   # redirect to Home page

    # Right Side (Sign In)
    with col2:
        st.markdown("### Sign In")
        login = st.text_input("Login or Email", key="login_input")
        password = st.text_input("Password", type="password", key="password_input")
        if st.button("Sign In", key="signin"):
            if login and password:   # fake validation
                navigate("home")
            else:
                st.error("Please enter login and password!")

elif st.session_state.page == "home":
    st.subheader("🏠 Welcome to Home Page")
    st.write("This is the home section of your platform.")

elif st.session_state.page == "dashboard":
    st.subheader("📊 Dashboard")
    st.write("Your trading dashboard will be shown here.")

elif st.session_state.page == "profile":
    st.subheader("👤 Profile")
    st.write("Manage your profile and settings here.")

elif st.session_state.page == "feedback":
    st.subheader("💬 Feedback")
    feedback = st.text_area("Enter your feedback:")
    if st.button("Submit Feedback"):
        st.success("✅ Thanks for your feedback!")
