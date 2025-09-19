import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Login | Signup", layout="centered")

# CSV file for storing users
USER_FILE = "users.csv"

# Create file if it doesn’t exist
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["name", "email", "password"])
    df.to_csv(USER_FILE, index=False)

# Load users
def load_users():
    return pd.read_csv(USER_FILE)

# Save new user
def save_user(name, email, password):
    df = load_users()
    if email in df["email"].values:
        return False  # already exists
    new_user = pd.DataFrame([[name, email, password]], columns=["name", "email", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

# Authenticate user
def authenticate(email, password):
    df = load_users()
    user = df[(df["email"] == email) & (df["password"] == password)]
    if not user.empty:
        return user.iloc[0]["name"]
    return None

# Custom CSS
st.markdown("""
    <style>
    body {
        font-family: 'Poppins', sans-serif;
    }
    .left-panel {
        background: linear-gradient(to right, #20c997, #17a2b8);
        color: #fff;
        border-radius: 15px 0 0 15px;
        padding: 40px;
        height: 100%;
    }
    .right-panel h2 {
        color: #20c997;
    }
    input[type=text], input[type=password], input[type=email] {
        width: 80%;
        padding: 10px;
        margin: 10px 0;
        border-radius: 8px;
        border: 1px solid #ccc;
    }
    button {
        border-radius: 20px;
        border: none;
        background: #20c997;
        color: #fff;
        font-size: 14px;
        font-weight: bold;
        padding: 10px 30px;
        margin-top: 15px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Session state for switching between login/signup
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "user" not in st.session_state:
    st.session_state.user = None

col1, col2 = st.columns([1,1])

# Left panel
with col1:
    st.markdown("""
        <div class="left-panel">
            <h1>Welcome!</h1>
            <p>Login or create a new account to continue</p>
        </div>
    """, unsafe_allow_html=True)

# Right panel
with col2:
    if st.session_state.user:
        st.success(f"✅ Logged in as {st.session_state.user}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
    elif not st.session_state.show_signup:
        st.markdown("<h2>Sign In</h2>", unsafe_allow_html=True)
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In"):
            user = authenticate(email, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome back, {user}!")
                st.rerun()
            else:
                st.error("Invalid email or password")
        st.write("Don't have an account?")
        if st.button("Go to Sign Up"):
            st.session_state.show_signup = True
            st.rerun()
    else:
        st.markdown("<h2>Create Account</h2>", unsafe_allow_html=True)
        name = st.text_input("Name", key="signup_name")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if name and email and password:
                if save_user(name, email, password):
                    st.success("Account created successfully! Please log in.")
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error("Email already registered. Try logging in.")
            else:
                st.warning("Please fill in all fields")
        st.write("Already have an account?")
        if st.button("Go to Sign In"):
            st.session_state.show_signup = False
            st.rerun()
