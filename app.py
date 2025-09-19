# ========= Pages =========
elif choice == "Home":
    set_page_theme("#FFB6C1", "#FFE4E1")  # Light pink gradient
    st.subheader("🏠 Home")
    st.markdown("""
    Welcome to **Global Balance** 🌍  
    This platform provides an **interactive dashboard** built using Power BI, 
    where you can monitor, analyze, and visualize global balance data effectively.  

    ### 🔹 Features:
    - 📊 Real-time analytics  
    - 🌐 Global insights  
    - 📈 Interactive reports  
    - 💡 Data-driven decision making  
    """)

elif choice == "Dashboard":
    set_page_theme("#D2B48C", "#E6D3B3")  # Light taupe gradient
    st.subheader("📊 Dashboard")
    if "user" in st.session_state:
        st.write("Here is your embedded Power BI dashboard:")
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.iframe(powerbi_url, width=1000, height=600, scrolling=True)
    else:
        st.warning("⚠ Please log in to view the dashboard.")

elif choice == "Profile":
    set_page_theme("#F0F8FF", "#E6F2FA")  # Alice blue gradient
    st.subheader("👤 Profile")
    if "user" in st.session_state:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image("profile.png", width=150)  
        with col2:
            st.markdown(f"""
            **Full Name:** {st.session_state.get('fullname', 'Komala Rani Talisetti')}  
            **Username:** {st.session_state['user']}  
            **Email:** {st.session_state.get('email', 'talisettikomali@gmail.com')}  
            """)
    else:
        st.warning("⚠ Please log in to view your profile.")

elif choice == "Feedback":
    set_page_theme("#98FF98", "#CCFFCC")  # Mint green gradient
    st.subheader("💬 Feedback")
    feedback = st.text_area("Share your feedback:", key="feedback_text")
    if st.button("Submit Feedback", key="feedback_btn"):
        st.success("🙌 Thank you for your feedback!")
