import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Animated Login System", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_signup_ui():
    html_code = """
    <style>
        body { background: linear-gradient(to right, #20c997, #17a2b8); }
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
          cursor: pointer;   /* 👈 makes it a pointer */
        }
        .btn:active { transform: scale(0.95); }
        .btn:focus { outline: none; }
    </style>

    <div class="container" id="container">
        <div class="form-container sign-in-container">
          <h1>Sign In</h1>
          <input id="signin-email" placeholder="Email" />
          <input id="signin-password" type="password" placeholder="Password" />
          <button class="btn" id="signin-submit">Login</button>
        </div>

        <div class="form-container sign-up-container">
          <h1>Create Account</h1>
          <input id="signup-name" placeholder="Name" />
          <input id="signup-email" placeholder="Email" />
          <input id="signup-password" type="password" placeholder="Password" />
          <button class="btn" id="signup-submit">Sign Up</button>
        </div>

        <div class="overlay-container">
          <div class="overlay">
            <div class="overlay-panel overlay-left">
              <h1>Welcome Back!</h1>
              <button class="btn" id="signIn">Sign In</button>
            </div>
            <div class="overlay-panel overlay-right">
              <h1>Hello, Friend!</h1>
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

        // 🔗 Streamlit bridge: trigger login/signup
        document.getElementById('signin-submit').addEventListener('click', function() {
            window.parent.postMessage({type: 'login'}, '*');
        });
        document.getElementById('signup-submit').addEventListener('click', function() {
            window.parent.postMessage({type: 'signup'}, '*');
        });
    </script>
    """
    components.html(html_code, height=650, scrolling=False)

# -------- LISTEN TO JS EVENTS ----------
msg = st.experimental_get_query_params().get("msg", None)
if msg == ["login"]:
    st.session_state.logged_in = True
    st.success("✅ Logged in successfully!")

if not st.session_state.logged_in:
    login_signup_ui()
else:
    st.title("🏠 Home")
    st.write("You are logged in!")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
