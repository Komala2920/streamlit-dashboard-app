# app.py
import streamlit as st
import sqlite3
import hashlib
from sqlite3 import IntegrityError

DB_PATH = "users.db"

# ---------- DATABASE INIT ----------
def init_db():
    """Ensure DB + table exist every run (safe for Streamlit reruns)."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT
            )
        ''')
        conn.commit()

# ---------- UTILS ----------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ---------- DB FUNCTIONS (use fresh connection each call) ----------
def add_user(username: str, email: str, password: str):
    if not username or not email or not password:
        return False, "Please fill all fields."
    hashed = hash_password(password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                      (username, email, hashed))
            conn.commit()
        return True, "Account created successfully."
    except IntegrityError as ie:
        msg = str(ie).lower()
        if "users.email" in msg or "unique constraint failed: users.email" in msg:
            return False, "Email already registered."
        else:
            return False, "Username already taken."
    except Exception as e:
        return False, f"DB error: {e}"

def login_user(email: str, password: str):
    if not email or not password:
        return None
    hashed = hash_password(password)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT username, email FROM users WHERE email=? AND password=?", (email, hashed))
        return c.fetchone()  # returns tuple (username, email) or None

def get_user(username: str):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT username, email FROM users WHERE username=?", (username,))
        return c.fetchone()

# ---------- STREAMLIT CONFIG ----------
init_db()
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
        width: 850px; margin: auto;
        display: flex; background: #fff;
        border-radius: 12px; box-shadow: 0 15px 25px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    .left-panel {
        background: #20c997;
        flex: 1; color: #fff; text-align: center;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 30px; border-radius: 12px;
    }
    .left-panel h2 { font-size: 28px; margin-bottom: 10px; }
    .left-panel p { font-size: 14px; margin-bottom: 30px; }
    .left-btn {
        border: 2px solid #fff; background: transparent; color: #fff;
        padding: 12px 30px; border-radius: 30px; cursor: pointer;
    }
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
    </style>
""", unsafe_allow_html=True)

# ---------- LOGIN / SIGNUP PAGE (when not logged in) ----------
def login_signup_page():
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.markdown('<div class="left-panel">', unsafe_allow_html=True)
        st.markdown("<h2>Welcome Back!</h2>", unsafe_allow_html=True)
        st.markdown("<p>To keep connected with us please login with your personal info</p>", unsafe_allow_html=True)
        # the original JS onclick won't work inside Streamlit reliably; instead show a helpful note/button
        if st.button("Already have an account? Scroll to Login below"):
            st.experimental_scroll("login_anchor")  # helpful UX (may not work in all versions)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)
        st.markdown("<h2>Create Account</h2>", unsafe_allow_html=True)
        st.markdown('<div class="social-icons"><div>f</div><div>G+</div><div>in</div></div>', unsafe_allow_html=True)
        st.write("or use your email for registration:")

        with st.form("signup_form"):
            username = st.text_input("Username", key="su_username")
            email = st.text_input("Email", key="su_email")
            password = st.text_input("Password", type="password", key="su_password")
            submitted = st.form_submit_button("SIGN UP")
            if submitted:
                ok, msg = add_user(username.strip(), email.strip().lower(), password)
                if ok:
                    st.success(msg + " You can now login below.")
                else:
                    st.error(msg)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("Login")
    st.write('<a id="login_anchor"></a>', unsafe_allow_html=True)
    with st.form("login_form"):
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_pass")
        if st.form_submit_button("Login"):
            user = login_user(login_email.strip().lower(), login_password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = user[0]
                st.success("Login successful! Redirecting...")
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
    user = get_user(st.session_state.username)
    if user:
        st.write(f"Username: {user[0]}")
        st.write(f"Email: {user[1]}")
    else:
        st.write("User not found.")

def feedback_page():
    st.title("💬 Feedback")
    feedback = st.text_area("Your feedback:")
    if st.button("Submit"):
        # For simplicity we just acknowledge feedback. You can store it in DB or file if needed.
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
