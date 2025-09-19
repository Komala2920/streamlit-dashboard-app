import streamlit as st

# Page config
st.set_page_config(page_title="Login & Signup UI", layout="centered")

# CSS styling for custom layout
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .box {
        display: flex;
        width: 800px;
        height: 450px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        overflow: hidden;
        background-color: white;
    }
    .left {
        width: 40%;
        background: #1abc9c;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 30px;
    }
    .left h1 {
        font-size: 28px;
        margin-bottom: 10px;
    }
    .left p {
        font-size: 14px;
        margin-bottom: 20px;
    }
    .left button {
        background: transparent;
        border: 2px solid white;
        border-radius: 25px;
        padding: 10px 30px;
        color: white;
        cursor: pointer;
        font-size: 14px;
    }
    .right {
        width: 60%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 30px;
    }
    .right h2 {
        color: #1abc9c;
        margin-bottom: 20px;
    }
    .input-box {
        width: 100%;
        margin-bottom: 15px;
    }
    input {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .signup-btn {
        background: #1abc9c;
        border: none;
        color: white;
        padding: 10px 30px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# HTML layout
st.markdown("""
<div class="container">
    <div class="box">
        <!-- Left Panel -->
        <div class="left">
            <h1>Welcome Back!</h1>
            <p>To keep connected with us please login with your personal info</p>
            <button>Sign In</button>
        </div>
        
        <!-- Right Panel -->
        <div class="right">
            <h2>Create Account</h2>
            <div class="input-box">
                <input type="text" placeholder="Name">
            </div>
            <div class="input-box">
                <input type="email" placeholder="Email">
            </div>
            <div class="input-box">
                <input type="password" placeholder="Password">
            </div>
            <button class="signup-btn">Sign Up</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
