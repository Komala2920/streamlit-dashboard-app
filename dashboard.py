import requests

st.title("GitHub Dashboard")
username = st.text_input("Enter GitHub Username")
if username:
    response = requests.get(f"https://app.powerbi.com/groups/me/reports/4d41c1bc-17bb-491e-8da8-861aaede731f/24434bd2ed4071702132?redirectedFromSignup=1&experience=power-bi")
    if response.status_code == 200:
        data = response.json()
        st.write(f"Name: {data['name']}")
        st.write(f"Public Repos: {data['public_repos']}")
        st.image(data['avatar_url'])
