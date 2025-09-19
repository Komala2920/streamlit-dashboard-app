# -------------------------
# Global Dark Theme
# -------------------------
def global_dark_theme():
    st.markdown(
        """
        <style>
        body {
            background-color: #0e0c2a;
            background-image: radial-gradient(circle at 20% 30%, #1d1b3a 25%, transparent 40%),
                              radial-gradient(circle at 80% 70%, #1d1b3a 25%, transparent 40%);
            color: white;
        }
        .block-container {
            padding-top: 2rem;
        }
        .login-box {
            background-color: #1c1a3a;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0px 8px 24px rgba(0,0,0,0.4);
            width: 380px;
            margin: 100px auto;
            text-align: center;
        }
        .login-box h1 {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #2a274d;
            color: white;
            border-radius: 8px;
        }
        .stButton>button {
            background: #1376ff;
            color: white;
            border-radius: 8px;
            width: 100%;
            padding: 10px;
            border: none;
            font-size: 16px;
        }
        .stButton>button:hover {
            background: #0d5ed6;
        }
        .forgot {
            margin-top: 10px;
            font-size: 13px;
        }
        .forgot a {
            color: #8aa8ff;
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------
# Modified Login Page
# -------------------------
def show_login():
    global_dark_theme()

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1>Global Balance</h1>", unsafe_allow_html=True)  # renamed here ✅

    email = st.text_input("Email address")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        ok, name = verify_user(email, password)
        if ok:
            st.success("Welcome back, " + (name or email))
            st.session_state.logged_in = True
            st.session_state.user_email = email
        else:
            st.error("Invalid credentials")

    st.markdown("<div class='forgot'><a href='#'>Forgot your password?</a></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Keep signup expander below login
    st.markdown("---")
    st.info("Don't have an account? Sign up below.")
    with st.expander("Sign up"):
        name = st.text_input("Full name", key="signup_name")
        email_s = st.text_input("Email", key="signup_email")
        password_s = st.text_input("Password", type="password", key="signup_password")
        if st.button("Create account"):
            ok, msg = create_user(email_s, name, password_s)
            if ok:
                st.success("Account created — you can login now.")
            else:
                st.error(msg)
