import streamlit as st
import pandas as pd
import requests

from src.utils.helpers import hide_df_indexes, get_transactions_limit


def main(username, url):
    type_tr = st.radio(
        "Select data type:", (
            "1. All Transactions",
            "2. Transaction By id/hash",
        )
    )

    if type_tr[:1] == "1":
        with st.form("transactions"):
            st.subheader(f"{username} Transactions")
            limit = get_transactions_limit()
            response = requests.get(f"{url}/user_transactions/{username}?limit={limit}").json()
            if response["success"]:
                df = pd.json_normalize(response["result"])
                if not df.empty:
                    df = df.sort_values(by="id", ascending=False).reset_index(drop=True)
                    df.index += 1
                    st.dataframe(df, height=500)
                else:
                    st.code("User did not have any transactions")
            else:
                st.code(response["message"])
            st.form_submit_button("Refresh")

    elif type_tr[:1] == "2":
        with st.form("transaction_by_id"):
            hide_df_indexes()
            st.subheader("Transaction By Id")
            tr_id = st.number_input("Input transaction id:", min_value=1, value=1, step=1)
            response = requests.get(f"{url}/id_transactions/{tr_id}").json()
            df = pd.json_normalize(response["result"])
            st.dataframe(df)
            st.form_submit_button("Refresh")
        with st.form("transaction_by_hash"):
            hide_df_indexes()
            st.subheader("Transaction By Hash")
            tr_h = st.text_input("Transaction Hash:", "84b2303d95bcd1dd921350803ae92157d667d627")
            response = requests.get(f"{url}/transactions/{tr_h}").json()
            df = pd.json_normalize(response["result"])
            st.dataframe(df)
            st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
