import streamlit as st
import pandas as pd
import os

USER_FILE = "users.csv"

# ------------------ Helpers ------------------
if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["name", "email", "password"])
    df.to_csv(USER_FILE, index=False)

def load_users():
    return pd.read_csv(USER_FILE)

def save_user(name, email, password):
    df = load_users()
    if email in df["email"].values:
        return False
    new_user = pd.DataFrame([[name, email, password]], columns=["name", "email", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

def authenticate(email, password):
    df = load_users()
    user = df[(df["email"] == email) & (df["password"] == password)]
    if not user.empty:
        return user.iloc[0]["name"]
    return None

# ------------------ UI Config ------------------
st.set_page_config(page_title="Sliding Login", layout="centered")

st.markdown("""
<style>
.container {
    width: 800px;
    max-width: 100%;
    min-height: 480px;
    position: relative;
    overflow: hidden;
    margin: auto;
    background: #fff;
    border-radius: 15px;
    box-shadow: 0 14px 28px rgba(0,0,0,0.25),
                0 10px 10px rgba(0,0,0,0.22);
    transition: all 0.6s ease-in-out;
    display: flex;
}
.panel {
    flex: 1;
    padding: 40px;
    transition: transform 0.6s ease-in-out, opacity 0.6s ease-in-out;
}
.hidden {
    transform: translateX(100%);
    opacity: 0;
    pointer-events: none;
}
.visible {
    transform: translateX(0%);
    opacity: 1;
}
h2 {
    color: #20c997;
}
</style>
""", unsafe_allow_html=True)

# Session state for sliding toggle
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

# ------------------ Layout ------------------
st.markdown("<div class='container'>", unsafe_allow_html=True)

# Sign In Panel
signin_class = "panel visible" if not st.session_state.show_signup else "panel hidden"
st.markdown(f"<div class='{signin_class}'>", unsafe_allow_html=True)
st.subheader("Sign In")
with st.form("signin"):
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    submitted = st.form_submit_button("Sign In")
    if submitted:
        user = authenticate(email, password)
        if user:
            st.success(f"🎉 Welcome back, {user}!")
        else:
            st.error("❌ Invalid credentials")
if st.button("Go to Sign Up"):
    st.session_state.show_signup = True
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Sign Up Panel
signup_class = "panel visible" if st.session_state.show_signup else "panel hidden"
st.markdown(f"<div class='{signup_class}'>", unsafe_allow_html=True)
st.subheader("Create Account")
with st.form("signup"):
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")
    submitted = st.form_submit_button("Sign Up")
    if submitted:
        ok = save_user(name, email, password)
        if ok:
            st.success("✅ Account created successfully! Please sign in.")
            st.session_state.show_signup = False
            st.rerun()
        else:
            st.error("❌ Email already exists!")
if st.button("Go to Sign In"):
    st.session_state.show_signup = False
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
