if st.button("Logout"):
    st.session_state['logged_in'] = False
    st.experimental_rerun()
