import streamlit as st
import pandas as pd
import requests


def main(url):
    with st.form("all_pools"):
        response = requests.get(f"{url}/all_pools").json()
        if response["success"]:
            df = pd.json_normalize(response["result"])
            df.index += 1
            st.subheader("All Pools")
            st.dataframe(df, height=1000)
        else:
            st.code(pd.json_normalize(response)["message"][0])
        st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
