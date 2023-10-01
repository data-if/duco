import streamlit as st
import requests


def main(username, url):
    with st.form("transaction"):
        st.subheader("Transaction")
        pwd = st.text_input("Password:", type="password")
        recipient = st.text_input("Recipient:")
        amount = st.number_input("Amount:", min_value=1., value=100., step=1.)
        memo = st.text_input("Memo:")

        if st.form_submit_button("Make Transaction"):
            query_params = {
                "username": username,
                "password": pwd,
                "recipient": recipient,
                "amount": amount,
                "memo": memo,
            }
            response = requests.get(f"{url}/transaction/", params=query_params).json()
            if response["success"]:
                st.json(response)
            else:
                st.error(response)
