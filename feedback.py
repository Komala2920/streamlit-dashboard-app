st.title("Feedback")
feedback = st.text_area("Share your thoughts")
if st.button("Submit"):
    st.success("Thanks for your feedback!")
