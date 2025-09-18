import requests

st.title("GitHub Dashboard")
username = st.text_input("Enter GitHub Username")
if username:
    response = requests.get(f"https://api.github.com/users/{username}")
    if response.status_code == 200:
        data = response.json()
        st.write(f"Name: {data['name']}")
        st.write(f"Public Repos: {data['public_repos']}")
        st.image(data['avatar_url'])
