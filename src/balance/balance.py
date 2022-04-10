import streamlit as st
import pendulum
import requests

from src.utils.helpers import DT_FMT, BST


def main(username, url):
    with st.form("user_balance"):
        st.subheader(f"{username} Balance")
        response = requests.get(f"{url}/balances/{username}").json()

        if response["success"]:
            for key, value in response["result"].items():
                if key in ("balance", "stake_date", "stake_amount"):
                    if key in "stake_date":
                        value = pendulum.from_timestamp(value).format(DT_FMT)
                    st.code(f"{key.title().replace('_', ' ')}: {value} {'ᕲ' if key in BST else ''}")
        else:
            st.code(response["message"])
        st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
