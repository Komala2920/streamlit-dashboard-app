import streamlit as st

# --- Custom CSS (copied from your HTML) ---
st.markdown("""
<style>
* {margin: 0; padding: 0; box-sizing: border-box; font-family: "Segoe UI", sans-serif;}

body {
  background: linear-gradient(135deg, #2a5298, #1e3c72);
  color: #333;
}

.container {
  width: 90%;
  max-width: 900px;
  margin: 40px auto;
  background: #fff;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  padding: 20px;
}

.stButton>button {
  margin: 5px;
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  background: #2a5298;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}
.stButton>button:hover {background: #1e3c72;}
</style>
""", unsafe_allow_html=True)

# --- Simple in-memory user "database" ---
users = {"admin": "12345"}

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- Functions ---
def login(username, password):
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("✅ Login successful!")
    else:
        st.error("❌ Invalid username or password")

def signup(username, password):
    if username in users:
        st.warning("⚠️ User already exists!")
    else:
        users[username] = password
        st.success("🎉 Account created! You can log in now.")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""


# --- UI ---
st.markdown("<div class='container'>", unsafe_allow_html=True)

if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])

    with tab1:
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Sign In"):
            login(username, password)

    with tab2:
        st.subheader("Create Account")
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Sign Up"):
            signup(new_user, new_pass)

else:
    st.subheader(f"👋 Welcome, {st.session_state.username}!")

    # Navigation buttons
    page = st.radio("Navigate", ["Home", "Dashboard", "Profile", "Feedback", "Logout"], horizontal=True)

    if page == "Home":
        st.write("🏠 This is the Home page with welcome content.")
    elif page == "Dashboard":
        st.write("📊 Dashboard with charts and analytics.")
        st.line_chart({"Data": [1, 5, 2, 6, 2, 8]})
    elif page == "Profile":
        st.write(f"👤 Profile details for user: {st.session_state.username}")
    elif page == "Feedback":
        feedback = st.text_area("📝 Enter your feedback:")
        if st.button("Submit Feedback"):
            st.success("✅ Thanks for your feedback!")
    elif page == "Logout":
        logout()
        st.info("🔒 Logged out successfully.")

st.markdown("</div>", unsafe_allow_html=True)
