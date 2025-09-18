import streamlit as st

# Page config
st.set_page_config(page_title="B-TECHNO Login", layout="wide")

# --- LEFT COLUMN: LOGIN FORM ---
with st.container():
    left, right = st.columns([1, 2])  # left (login) smaller, right (illustration) larger

    with left:
        st.markdown("## 🔑 Sign In")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Sign In")

        if submit:
            if username == "admin" and password == "12345":
                st.success(f"✅ Welcome, {username}!")
            else:
                st.error("❌ Invalid Credentials")

        st.markdown("[Forgot Password?](#)")
        st.write("---")
        st.markdown("Or sign in with:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Facebook")
        with col2:
            st.button("Twitter")
        with col3:
            st.button("Google")

        st.write("---")
        st.markdown("Don’t have an account? [Sign Up](#)")

    # --- RIGHT COLUMN: ILLUSTRATION ---
    with right:
        st.image("assets/illustration.png", width=400)  # replace with your animation/image
        st.markdown("### Technical Analysis of Software Requirements")
        st.caption(
            "Curabitur sed lectus in dui consectetur rhoncus sit amet nec sapien. "
            "Donec vel felis non tellus tristique condimentum."
        )
