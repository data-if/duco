import streamlit as st
import requests


def main(username, url):
    with st.form("auth"):
        st.subheader("Auth")
        pwd = st.text_input("Password:", type="password")

        if st.form_submit_button("Auth"):
            query_params = {"password": pwd}
            response = requests.get(f"{url}/auth/{username}", params=query_params).json()
            if response["success"]:
                st.json(response)
            else:
                st.error(response)


if __name__ == "__main__":
    main()
