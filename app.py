import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Animated Login System", layout="wide")

# ---------------- BACKGROUND SETUP ----------------
def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data.read()).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# Set your background image here
# set_background("background.png")   # 👈 add your background image file

# ---------------- LOGIN / SIGNUP UI ----------------
def login_signup_ui():
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
          width: 900px;
          max-width: 100%;
          min-height: 500px;
          margin: auto;
          display: flex;
        }
        .form-container {
          position: absolute;
          top: 0;
          height: 100%;
          transition: all 0.6s ease-in-out;
          display: flex;
          justify-content: center;
          flex-direction: column;
          padding: 0 50px;
          text-align: left;
          width: 50%;
          background: #fff;
        }
        .form-container h1 {
          margin-bottom: 20px;
          font-size: 28px;
          color: #20c997;
          text-align: center;
        }
        .form-container input {
          background: #f3f3f3;
          border: none;
          padding: 12px 15px;
          margin: 10px auto;
          width: 80%;
          border-radius: 5px;
          display: block;
        }
        .sign-in-container {
          left: 0;
          z-index: 2;
          align-items: center;
          text-align: center;
        }
        .sign-up-container {
          left: 0;
          opacity: 0;
          z-index: 2;
          align-items: center;
          padding-left: 0;
          text-align: center;
        }
        .container.right-panel-active .sign-in-container {
          transform: translateX(100%);
        }
        .container.right-panel-active .sign-up-container {
          transform: translateX(100%);
          opacity: 1;
          z-index: 5;
          transition: all 0.6s ease-in-out;
        }
        .overlay-container{
          position:absolute;
          top:0;
          left:50%;
          width:50%;
          height:100%;
          overflow:hidden;
          transition:transform .6s ease-in-out;
          z-index:100;
        }
        .container.right-panel-active .overlay-container{ transform: translateX(-100%); }
        .overlay{
          background: linear-gradient(to right,#20c997,#17a2b8);
          color: #fff;
          position: relative;
          left:-100%;
          height:100%;
          width:200%;
          transform:translateX(0);
          transition:transform .6s ease-in-out;
        }
        .container.right-panel-active .overlay{ transform: translateX(50%); }
        .overlay-panel{
          position:absolute;
          display:flex;
          flex-direction:column;
          align-items:center;
          justify-content:center;
          padding:0 40px;
          text-align:center;
          top:0;
          height:100%;
          width:50%;
          transition:transform .6s ease-in-out;
        }
        .overlay-left{ transform: translateX(-20%); left:0; }
        .container.right-panel-active .overlay-left{ transform: translateX(0); }
        .overlay-right{ right:0; transform: translateX(0); }
        .container.right-panel-active .overlay-right{ transform: translateX(20%); }
        .btn {
          border-radius: 20px;
          border: 1px solid #20c997;
          background-color: #20c997;
          color: #fff;
          font-size: 14px;
          font-weight: bold;
          padding: 12px 45px;
          letter-spacing: 1px;
          text-transform: uppercase;
          transition: transform 80ms ease-in;
          margin-top: 15px;
          cursor: pointer;
        }
        .btn:active { transform: scale(0.95); }
        .btn:focus { outline: none; }
    </style>

    <div class="container" id="container">
        <!-- Sign In Form -->
        <div class="form-container sign-in-container">
          <h1>Sign In</h1>
          <input id="signin-email" placeholder="Email" />
          <input id="signin-password" type="password" placeholder="Password" />
          <button class="btn" id="signin-submit">Login</button>
        </div>

        <!-- Sign Up Form -->
        <div class="form-container sign-up-container">
          <h1>Create Account</h1>
          <input id="signup-name" placeholder="Name" />
          <input id="signup-email" placeholder="Email" />
          <input id="signup-password" type="password" placeholder="Password" />
          <button class="btn" id="signup-submit">Sign Up</button>
        </div>

        <!-- Overlay -->
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
    components.html(html_code, height=650, scrolling=False)

# ---------------- DASHBOARD PAGES ----------------
def home_page():
    st.title("🏠 Home")
    st.write("Welcome to the Home page!")

def dashboard_page():
    st.title("📊 Dashboard")
    st.write("This is the dashboard.")

def profile_page():
    st.title("👤 Profile")
    st.write("Your profile details go here.")

def feedback_page():
    st.title("💬 Feedback")
    st.text_area("Enter your feedback here:")

# ---------------- MAIN APP ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "Home"

if not st.session_state.logged_in:
    login_signup_ui()
else:
    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("🏠 Home"): st.session_state.page = "Home"
    if st.sidebar.button("📊 Dashboard"): st.session_state.page = "Dashboard"
    if st.sidebar.button("👤 Profile"): st.session_state.page = "Profile"
    if st.sidebar.button("💬 Feedback"): st.session_state.page = "Feedback"
    if st.sidebar.button("🚪 Logout"): st.session_state.logged_in = False

    # Render pages
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Dashboard":
        dashboard_page()
    elif st.session_state.page == "Profile":
        profile_page()
    elif st.session_state.page == "Feedback":
        feedback_page()                                          

