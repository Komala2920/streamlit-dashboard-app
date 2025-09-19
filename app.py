import streamlit as st

# Page setup
st.set_page_config(page_title="Login & Signup UI", layout="centered")

# --- Layout ---
col1, col2 = st.columns([2, 3])

# --- Left Panel (Login) ---
with col1:
    st.markdown(
        """
        <div style="background:#1abc9c; height:100vh; 
                    display:flex; flex-direction:column; 
                    justify-content:center; align-items:center; 
                    text-align:center; color:white; padding:30px; border-radius:10px;">
            <h1>Welcome Back!</h1>
            <p>To keep connected with us please login with your personal info</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Sign In"):
        if login_email == "test@example.com" and login_password == "1234":
            st.success("✅ Login Successful!")
        else:
            st.error("❌ Invalid Email or Password")

# --- Right Panel (Signup) ---
with col2:
    st.markdown(
        "<h2 style='color:#1abc9c; text-align:center;'>Create Account</h2>",
        unsafe_allow_html=True
    )

    signup_name = st.text_input("Name", key="signup_name")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_pass")

    if st.button("Sign Up"):
        if signup_name and signup_email and signup_password:
            st.success(f"🎉 Account created for {signup_name}!")
        else:
            st.warning("⚠ Please fill all fields")
