import streamlit as st
import sqlite3

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("app_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ---------- HELPER FUNCTIONS ----------
def add_user(username, email, password):
    try:
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        return True
    except:
        return False

def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()

def get_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

# ---------- STREAMLIT CONFIG ----------
st.set_page_config(page_title="Streamlit App", page_icon="✨", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    body {font-family: 'Segoe UI', sans-serif;}
    .container {
        width: 850px; height: 500px; margin: auto;
        display: flex; background: #fff;
        border-radius: 12px; box-shadow: 0 15px 25px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    .left-panel {
        background: #20c997;
        flex: 1; color: #fff; text-align: center;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 30px;
    }
    .left-panel h2 { font-size: 28px; margin-bottom: 10px; }
    .left-panel p { font-size: 14px; margin-bottom: 30px; }
    .left-btn {
        border: 2px solid #fff; background: transparent; color: #fff;
        padding: 12px 30px; border-radius: 30px; cursor: pointer;
    }
    .left-btn:hover { background: #fff; color: #20c997; }

    .right-panel {
        flex: 1.3; padding: 40px; display: flex; flex-direction: column; justify-content: center;
    }
    .right-panel h2 { color: #20c997; margin-bottom: 20px; }
    .social-icons { display: flex; gap: 15px; margin-bottom: 20px; }
    .social-icons div {
        width: 40px; height: 40px; border: 1px solid #ccc; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        color: #666; font-size: 18px;
    }
    input {
        width: 100%; padding: 12px; margin: 10px 0;
        border: 1px solid #ccc; border-radius: 6px;
    }
    .signup-btn {
        background: #20c997; color: #fff; border: none;
        padding: 12px 30px; border-radius: 30px; cursor: pointer;
    }
    .signup-btn:hover { background: #17a589; }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGIN / SIGNUP ----------
def login_signup_page():
    st.markdown("""
    <div class="container">
        <div class="left-panel">
            <h2>Welcome Back!</h2>
            <p>To keep connected with us please login with your personal info</p>
            <button class="left-btn" onclick="document.getElementById('login_form').style.display='block'">SIGN IN</button>
        </div>
        <div class="right-panel">
            <h2>Create Account</h2>
            <div class="social-icons">
                <div>f</div><div>G+</div><div>in</div>
            </div>
            <p>or use your email for registration:</p>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("SIGN UP"):
            if add_user(username, email, password):
                st.success("Account created! You can login now.")
            else:
                st.error("User already exists!")

    st.markdown("</div></div>", unsafe_allow_html=True)

    st.write("---")
    st.subheader("Login")
    with st.form("login_form"):
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pass")
        if st.form_submit_button("Login"):
            user = login_user(login_email, login_password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user[0]
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials!")

# ---------- APP PAGES ----------
def home_page():
    st.title(f"Welcome, {st.session_state.username} 👋")
    st.write("This is the *Home Page*")

def dashboard_page():
    st.title("📊 Dashboard")
    st.write("Your dashboard content goes here.")

def profile_page():
    st.title("👤 Profile")
    st.write(f"Username: {st.session_state.username}")

def feedback_page():
    st.title("💬 Feedback")
    feedback = st.text_area("Your feedback:")
    if st.button("Submit"):
        st.success("Thanks for your feedback!")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.experimental_rerun()

# ---------- NAVIGATION ----------
if not st.session_state.logged_in:
    login_signup_page()
else:
    menu = ["Home", "Dashboard", "Profile", "Feedback", "Logout"]
    choice = st.sidebar.radio("Navigation", menu)

    if choice == "Home":
        home_page()
    elif choice == "Dashboard":
        dashboard_page()
    elif choice == "Profile":
        profile_page()
    elif choice == "Feedback":
        feedback_page()
    elif choice == "Logout":
        logout()
