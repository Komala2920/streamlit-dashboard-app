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
# LOGIN UI (HTML + Animation)
# -------------------------
def login_ui():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: "Poppins", sans-serif; }
        body {
          background: linear-gradient(to right, #20c997, #17a2b8);
          height: 100vh;
          width: 100vw;
          display: flex;
          justify-content: center;
          align-items: center;
          overflow: hidden;
        }
        .container {
          background: #fff;
          border-radius: 10px;
          box-shadow: 0 14px 28px rgba(0,0,0,0.25),
                      0 10px 10px rgba(0,0,0,0.22);
          position: relative;
          overflow: hidden;
          width: 800px;
          max-width: 100%;
          min-height: 480px;
          display: flex;
        }
        .form-container {
          position: absolute;
          top: 0;
          height: 100%;
          transition: all 0.6s ease-in-out;
        }
        .sign-in-container { left: 0; width: 50%; z-index: 2; }
        .sign-up-container { left: 0; width: 50%; opacity: 0; z-index: 1; }
        .container.right-panel-active .sign-in-container { transform: translateX(100%); }
        .container.right-panel-active .sign-up-container {
          transform: translateX(100%); opacity: 1; z-index: 5; animation: show 0.6s;
        }
        @keyframes show { 0%,49.99%{opacity:0} 50%,100%{opacity:1} }
        form {
          background: #fff; display: flex; flex-direction: column; padding: 0 50px;
          height: 100%; justify-content: center; align-items: center; text-align: center;
        }
        form h1 { font-weight: bold; margin-bottom: 20px; }
        form input {
          background: #eee; border: none; padding: 12px 15px; margin: 8px 0; width: 100%;
          max-width: 300px; border-radius: 4px;
        }
        .btn {
          border-radius: 20px; border: 1px solid #20c997; background: #20c997; color: #fff;
          font-size: 14px; font-weight: bold; padding: 12px 45px; letter-spacing: 1px;
          text-transform: uppercase; transition: transform 80ms ease-in; cursor: pointer; margin-top: 10px;
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
    </head>
    <body>
      <div class="container" id="container">
        <!-- Sign Up -->
        <div class="form-container sign-up-container">
          <form>
            <h1>Create Account</h1>
            <input type="text" placeholder="Name" />
            <input type="email" placeholder="Email" />
            <input type="password" placeholder="Password" />
            <button type="button" class="btn" onclick="parent.postMessage({isLoggedIn:true}, '*')">Sign Up</button>
          </form>
        </div>

        <!-- Sign In -->
        <div class="form-container sign-in-container">
          <form>
            <h1>Sign In</h1>
            <input type="email" placeholder="Email" />
            <input type="password" placeholder="Password" />
            <button type="button" class="btn" onclick="parent.postMessage({isLoggedIn:true}, '*')">Sign In</button>
          </form>
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
    </body>
    </html>
    """
    components.html(html_code, height=600, scrolling=False)

    # Catch messages from iframe
    msg = st.experimental_get_query_params()
    if "isLoggedIn" in st.session_state and st.session_state.isLoggedIn:
        st.session_state.logged_in = True
        st.experimental_rerun()

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
        st.experimental_rerun()

# -------------------------
# MAIN APP
# -------------------------
if not st.session_state.logged_in:
    if components.html:  # show login
        login_ui()
else:
    dashboard_ui()
