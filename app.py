# ========= Pages =========
elif choice == "Home":
    set_page_theme("#FFFFFF", "#1F3A93")  # White + Navy Blue
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
    set_page_theme("#FFFFFF", "#2C3E50")  # White + Charcoal Gray
    st.subheader("📊 Dashboard")
    if "user" in st.session_state:
        st.write("Here is your embedded Power BI dashboard:")
        powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNGVmZDc0YzYtYWUwOS00OWFiLWI2NDgtNzllZDViY2NlMjZhIiwidCI6IjA3NjQ5ZjlhLTA3ZGMtNGZkOS05MjQ5LTZmMmVmZWFjNTI3MyJ9"
        components.iframe(powerbi_url, width=1000, height=600, scrolling=True)
    else:
        st.warning("⚠ Please log in to view the dashboard.")

elif choice == "Profile":
    set_page_theme("#FFFFFF", "#2ECC71")  # White + Emerald Green
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
    set_page_theme("#FFFFFF", "#F8D7DA")  # White + Blush Pink
    st.subheader("💬 Feedback")
    feedback = st.text_area("Share your feedback:", key="feedback_text")
    if st.button("Submit Feedback", key="feedback_btn"):
        st.success("🙌 Thank you for your feedback!")
