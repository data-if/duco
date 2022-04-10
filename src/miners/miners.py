import streamlit as st
import pandas as pd
import requests

from src.utils.helpers import hide_table_indexes


def main(username, url):
    with st.form("user_miners"):
        response = requests.get(f"{url}/miners/{username}").json()
        if response["success"]:
            df = pd.json_normalize(response["result"])
            st.subheader(f"{username} Miners ({df.shape[0]})")

            df = df.sort_values(by="identifier", ascending=True).reset_index(drop=True)
            df.index += 1
            hide_table_indexes()
            st.dataframe(df.drop(["username"], 1), height=1000)
        else:
            st.code(response["message"])
        st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
