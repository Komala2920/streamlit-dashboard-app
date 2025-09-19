import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Login | Signup", layout="centered")

USER_FILE = "users.csv"

if not os.path.exists(USER_FILE):
    df = pd.DataFrame(columns=["name", "email", "password"])
    df.to_csv(USER_FILE, index=False)

def load_users():
    return pd.read_csv(USER_FILE)

def save_user(name, email, password):
    df = load_users()
    if email in df["email"].values:
        return False
    new_user = pd.DataFrame([[name, email, password]], columns=["name", "email", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

def authenticate(email, password):
    df = load_users()
    user = df[(df["email"] == email) & (df["password"] == password)]
    if not user.empty:
        return user.iloc[0]["name"]
    return None

# CSS for sliding panels
st.markdown("""
<style>
* {font-family: 'Poppins', sans-serif;}
.container {
    position: relative;
    width: 850px;
    max-width: 100%;
    min-height: 500px;
    background: #fff;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    overflow: hidden;
}
.form-container {
    position: absolute;
    top: 0;
    height: 100%;
    transition: all 0.6s ease-in-out;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding: 0 50px;
    text-align: center;
    width: 50%;
}
.sign-in-container {left: 0; width: 50%; z-index: 2;}
.sign-up-container {left: 0; width: 50%; opacity: 0; z-index: 1;}

.container.right-panel-active .sign-in-container {
    transform: translateX(100%);
}
.container.right-panel-active .sign-up-container {
    transform: translateX(100%);
    opacity: 1;
    z-index: 5;
    transition: all 0.6s ease-in-out;
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
    background: linear-gradient(to right, #20c997, #17a2b8);
    color: #fff;
    position: relative;
    left: -100%;
    height: 100%;
    width: 200%;
    transform: translateX(0);
    transition: transform 0.6s ease-in-out;
    display: flex;
}
.container.right-panel-active .overlay {
    transform: translateX(50%);
}
.overlay-panel {
    position: absolute;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    top: 0;
    height: 100%;
    width: 50%;
    padding: 0 40px;
}
.overlay-left {transform: translateX(-20%); left: 0;}
.overlay-right {right: 0; transform: translateX(0);}
.container.right-panel-active .overlay-left {transform: translateX(0);}
.container.right-panel-active .overlay-right {transform: translateX(20%);}

input {
    background: #eee;
    border: none;
    padding: 12px 15px;
    margin: 8px 0;
    width: 100%;
    border-radius: 8px;
}
button {
    border-radius: 20px;
    border: none;
    background: #20c997;
    color: #fff;
    font-size: 14px;
    font-weight: bold;
    padding: 12px 45px;
    margin-top: 15px;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# Session state
if "right_panel" not in st.session_state:
    st.session_state.right_panel = False
if "user" not in st.session_state:
    st.session_state.user = None

# Container div
st.markdown(f"""
<div class="container {'right-panel-active' if st.session_state.right_panel else ''}" id="main-container">
    <div class="form-container sign-up-container">
        <form>
            <h1>Create Account</h1>
            <input type="text" placeholder="Name" id="signup_name"/>
            <input type="email" placeholder="Email" id="signup_email"/>
            <input type="password" placeholder="Password" id="signup_pass"/>
        </form>
    </div>
    <div class="form-container sign-in-container">
        <form>
            <h1>Sign In</h1>
            <input type="email" placeholder="Email" id="login_email"/>
            <input type="password" placeholder="Password" id="login_pass"/>
        </form>
    </div>
    <div class="overlay-container">
        <div class="overlay">
            <div class="overlay-panel overlay-left">
                <h1>Welcome Back!</h1>
                <p>To keep connected with us please login</p>
                <button onclick="switchToSignIn()">Sign In</button>
            </div>
            <div class="overlay-panel overlay-right">
                <h1>Hello, Friend!</h1>
                <p>Enter details and start your journey</p>
                <button onclick="switchToSignUp()">Sign Up</button>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
