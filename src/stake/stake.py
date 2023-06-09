import streamlit as st
import requests


def main(username, url):
    with st.form("get_pool"):
        st.subheader("Stake")
        amount = st.number_input("Stake amount:", min_value=1, value=100, step=1)
        pwd = st.input("Password:", type="password")
        query_params = {"amount": amount, "password": pwd}
        response = requests.get(f"{url}/stake/{username}", params=query_params).json()
        if response["success"]:
            st.json(response)
        else:
            st.error(response)

        st.form_submit_button("Stake")


if __name__ == "__main__":
    main()
