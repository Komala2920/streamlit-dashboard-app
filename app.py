import streamlit as st
import bcrypt
from pymongo import MongoClient

# ---- MongoDB Setup ----
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["authDemo"]
users = db["users"]

# ---- Helper Functions ----
def create_user(name, email, password):
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = {"name": name, "email": email, "password": hashed}
    try:
        users.insert_one(user)
        return True
    except:
        return False

def login_user(email, password):
    user = users.find_one({"email": email})
    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return user
    return None

# ---- Streamlit UI ----
st.set_page_config(page_title="Auth System", page_icon="🔐", layout="centered")

st.markdown("<h1 style='text-align: center; color: #20bfa9;'>🔐 Authentication</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Sign Up", "Login"])

# ---- Signup ----
with tab1:
    st.subheader("Create Account")
    name = st.text_input("Name", key="signup_name")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_password")
    if st.button("Sign Up"):
        if name and email and password:
            if create_user(name, email, password):
                st.success("✅ User registered successfully!")
            else:
                st.error("⚠️ Email already exists or error occurred.")
        else:
            st.warning("Please fill all fields.")

# ---- Login ----
with tab2:
    st.subheader("Welcome Back!")
    email_login = st.text_input("Email", key="login_email")
    password_login = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        user = login_user(email_login, password_login)
        if user:
            st.success(f"✅ Welcome, {user['name']}!")
        else:
            st.error("❌ Invalid credentials.")
