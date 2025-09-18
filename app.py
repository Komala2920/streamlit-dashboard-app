import streamlit as st
import sqlite3
import hashlib
import pandas as pd
import altair as alt
from pathlib import Path

# ---------------------------
# Database setup
# ---------------------------
DB_PATH = "users.db"

def create_usertable():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

def add_userdata(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    conn.close()
    return data

# ---------------------------
# Utility: password hashing
# ---------------------------
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

# ---------------------------
# Background setup (CSS)
# ---------------------------
def add_bg_from_local(image_file):
    with open(image_file, "C:\Users\91995\Downloads\cbcb74d7c06b56b3249ef31f5aa9e6a2.jpg") as f:
        data = f.read()
    import base64
    b64 = base64.b64encode(data).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------------------------
# App Pages
# ---------------------------
def home():
    st.title("🌍 Home - Global Balance")
    st.write("Welcome to the interactive dashboard application!")

def show_dashboard():
    st.markdown("<div class='app-container'>", unsafe_allow_html=True)
    st.title("📊 Dashboard - Global Balance")
    st.write("Charts and analytics inspired by the illustration.")

    # --- Power BI Embed ---
    st.subheader("Power BI Dashboard")
    powerbi_url = "https://app.powerbi.com/view?r=YOUR_EMBED_URL"  # Replace with your link

    st.markdown(f"""
        <iframe title="PowerBI Dashboard"
            width="100%" height="600"
            src="{powerbi_url}"
            frameborder="0" allowFullScreen="true"></iframe>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- Local sample visualizations ---
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    df = pd.DataFrame({
        "date": dates,
        "sales": (pd.Series(range(30)) * 100 +
                  pd.Series(pd.array(pd.Series(range(30)).sample(frac=1).reset_index(drop=True)))).cumsum()
    })

    line = alt.Chart(df).mark_line(point=True).encode(
        x="date:T",
        y="sales:Q",
        tooltip=["date:T", "sales:Q"]
    ).properties(height=300)
    st.altair_chart(line, use_container_width=True)

    st.subheader("Category Share")
    cat_df = pd.DataFrame({"category": ["X", "Y", "Z"], "pct": [40, 35, 25]})
    pie = alt.Chart(cat_df).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="pct", type="quantitative"),
        color=alt.Color(field="category", type="nominal")
    ).properties(height=260)
    st.altair_chart(pie, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def profile(username):
    st.title("👤 Profile")
    st.write(f"Hello, {username}! This is your profile page.")

def feedback():
    st.title("📝 Feedback")
    feedback_text = st.text_area("Enter your feedback:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# ---------------------------
# Main app
# ---------------------------
def main():
    st.set_page_config(page_title="Global Balance", layout="wide")

    add_bg_from_local("C:\Users\91995\Downloads\cbcb74d7c06b56b3249ef31f5aa9e6a2.jpg")  # background image

    create_usertable()

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if "username" not in st.session_state:
        st.session_state.username = None

    if choice == "Login":
        st.subheader("Login Section")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            hashed_pswd = make_hashes(password)
            result = login_user(username, hashed_pswd)

            if result:
                st.session_state.username = username
                st.success(f"Logged In as {username}")

                nav = st.sidebar.radio("Navigation", ["Home", "Dashboard", "Profile", "Feedback", "Logout"])

                if nav == "Home":
                    home()
                elif nav == "Dashboard":
                    show_dashboard()
                elif nav == "Profile":
                    profile(username)
                elif nav == "Feedback":
                    feedback()
                elif nav == "Logout":
                    st.session_state.username = None
                    st.info("Logged out successfully.")

            else:
                st.error("Incorrect Username/Password")

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')

        if st.button("Sign Up"):
            add_userdata(new_user, make_hashes(new_password))
            st.success("You have successfully created a valid Account")
            st.info("Go to Login Menu to login")

if __name__ == '__main__':
    main()

