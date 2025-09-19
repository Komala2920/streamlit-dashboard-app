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
# LOGIN UI (with animation + real inputs)
# -------------------------
def login_ui():
    # Animation container (overlay, panels)
    html_code = """
    <style>
        body { background: linear-gradient(to right, #20c997, #17a2b8); }
        .container {
          background: #fff;
          border-radius: 10px;
          box-shadow: 0 14px 28px rgba(0,0,0,0.25),
                      0 10px 10px rgba(0,0,0,0.22);
          position: relative;
          overflow: hidden;
          width: 100%;
          min-height: 80vh;
          display: flex;
        }
        .overlay-container{ position:absolute; top:0; left:50%; width:50%; height:100%; overflow:hidden; transition:transform .6s ease-in-out; z-index:100; }
        .container.right-panel-active .overlay-container{ transform: translateX(-100%); }
        .overlay{ background: linear-gradient(to right,#20c997,#17a2b8); position: relative; left:-100%; height:100%; width:200%; transform:translateX(0); transition:transform .6s ease-in-out; color:#fff; }
        .container.right-panel-active .overlay{ transform: translateX(50%); }
        .overlay-panel{ position:absolute; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:0 40px; text-align:center; top:0; height:100%; width:50%; transition:transform .6s ease-in-out; }
        .overlay-left{ transform: translateX(-20%); left:0; }
        .container.right-panel-active .overlay-left{ transform: translateX(0); }
        .overlay-right{ right:0; transform: translateX(0); }
        .container.right-panel-active .overlay-right{ transform: translateX(20%); }
    </style>

    <div class="container" id="container">
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
    """
    components.html(html_code, height=600, scrolling=False)

    # Actual Streamlit login box (replacing fake HTML form)
    st.markdown(
        """
        <style>
        .login-box {
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            max-width: 400px;
            margin: 2rem auto;
            text-align: center;
        }
        .login-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 1rem;
            color: #20c997;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Sign In</div>', unsafe_allow_html=True)

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login", use_container_width=True):
        if email and password:   # simple check (replace with DB validation later)
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Please enter email and password")

    st.markdown('</div>', unsafe_allow_html=True)

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
        st.rerun()

# -------------------------
# MAIN APP
# -------------------------
if not st.session_state.logged_in:
    login_ui()
else:
    dashboard_ui()
