import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Animated Login System", layout="wide")

# -------------------------
# SESSION STATE
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

# -------------------------
# LOGIN UI
# -------------------------
def login_ui():
    st.markdown(
        """
        <style>
        .container {
          background: #fff;
          border-radius: 10px;
          box-shadow: 0 14px 28px rgba(0,0,0,0.25),
                      0 10px 10px rgba(0,0,0,0.22);
          position: relative;
          overflow: hidden;
          width: 80%;
          margin: auto;
          min-height: 80vh;
          display: flex;
        }
        .form-container {
          position: absolute;
          top: 0;
          height: 100%;
          transition: all 0.6s ease-in-out;
        }
        .sign-in-container {
          left: 0;
          width: 50%;
          z-index: 2;
        }
        .container.right-panel-active .sign-in-container {
          transform: translateX(100%);
        }
        .sign-up-container {
          left: 0;
          width: 50%;
          opacity: 0;
          z-index: 1;
        }
        .container.right-panel-active .sign-up-container {
          transform: translateX(100%);
          opacity: 1;
          z-index: 5;
          animation: show 0.6s;
        }
        @keyframes show {
          0% { opacity: 0; }
          100% { opacity: 1; }
        }
        .overlay-container {
          position: absolute;
          top: 0;
          left: 50%;
          width: 50%;
          height: 100%;
          overflow: hidden;
          transition: transform 0.6s ease-in-out;
          z-index: 100;
        }
        .container.right-panel-active .overlay-container {
          transform: translateX(-100%);
        }
        .overlay {
          background: linear-gradient(to right,#20c997,#17a2b8);
          background-repeat: no-repeat;
          background-size: cover;
          background-position: 0 0;
          color: #FFFFFF;
          position: relative;
          left: -100%;
          height: 100%;
          width: 200%;
          transform: translateX(0);
          transition: transform 0.6s ease-in-out;
        }
        .container.right-panel-active .overlay {
          transform: translateX(50%);
        }
        .overlay-panel {
          position: absolute;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 0 40px;
          text-align: center;
          top: 0;
          height: 100%;
          width: 50%;
          transition: transform 0.6s ease-in-out;
        }
        .overlay-left {
          transform: translateX(-20%);
          left: 0;
        }
        .container.right-panel-active .overlay-left {
          transform: translateX(0);
        }
        .overlay-right {
          right: 0;
          transform: translateX(0);
        }
        .container.right-panel-active .overlay-right {
          transform: translateX(20%);
        }
        </style>

        <div class="container" id="container">
            <div class="form-container sign-in-container" id="signin-box"></div>
            <div class="form-container sign-up-container" id="signup-box"></div>
            <div class="overlay-container">
              <div class="overlay">
                <div class="overlay-panel overlay-left">
                  <h1>Welcome Back!</h1>
                  <p>To keep connected with us please login</p>
                  <button class="btn" id="signIn">Sign In</button>
                </div>
                <div class="overlay-panel overlay-right">
                  <h1>Hello, Friend!</h1>
                  <p>Enter your details and start your journey</p>
                  <button class="btn" id="signUp">Sign Up</button>
                </div>
              </div>
            </div>
        </div>

        <script>
            const signUpButton = document.getElementById('signUp');
            const signInButton = document.getElementById('signIn');
            const container = document.getElementById('container');
            signUpButton.addEventListener('click', () => container.classList.add("right-panel-active"));
            signInButton.addEventListener('click', () => container.classList.remove("right-panel-active"));
        </script>
        """,
        unsafe_allow_html=True,
    )

    # ----------------- SIGN IN FORM (inside white box) -----------------
    with st.container():
        with st.expander("🔐 Sign In", expanded=True):
            email = st.text_input("Email (Sign In)")
            password = st.text_input("Password (Sign In)", type="password")
            if st.button("Login"):
                if email and password:
                    st.session_state.logged_in = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Please enter email & password")

    # ----------------- SIGN UP FORM (inside white box) -----------------
    with st.container():
        with st.expander("🆕 Sign Up", expanded=False):
            new_email = st.text_input("Email (Sign Up)")
            new_password = st.text_input("Password (Sign Up)", type="password")
            if st.button("Register"):
                if new_email and new_password:
                    st.success("Account created (dummy for now)")
                else:
                    st.error("Please enter details")

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
        st.rerun()

# -------------------------
# MAIN APP
# -------------------------
if not st.session_state.logged_in:
    login_ui()
else:
    dashboard_ui()
