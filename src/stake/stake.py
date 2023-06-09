import streamlit as st
import requests


def main(username, url):
    with st.form("stake"):
        st.subheader("Stake")
        amount = st.number_input("Stake amount:", min_value=1, value=100, step=1)
        pwd = st.input("Password:", type="password")

        if st.form_submit_button("Stake"):
            query_params = {"amount": amount, "password": pwd}
            response = requests.get(f"{url}/stake/{username}", params=query_params).json()
            if response["success"]:
                st.json(response)
            else:
                st.error(response)


if __name__ == "__main__":
    main()
