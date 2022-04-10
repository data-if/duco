import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
import requests

from src.utils.helpers import hide_table_indexes, BST


def main(url):
    type_s = st.radio(
        "Select data type:", (
            "1. Server Statistics",
            "2. Miners Statistics",
            "3. Historic Prices",
        )
    )

    if type_s[:1] == "1":
        response = requests.get(f"{url}/statistics").json()

        with st.form("richest_miners"):
            st.subheader("Top 10 Richest Miners")
            m_list = pd.json_normalize(response)["Top 10 richest miners"][0]
            data_miners = {
                "Miner": [m.split("- ")[1] for m in m_list],
                "DUCO": [d.split("DUCO - ")[0] for d in m_list],
            }
            df_miners = pd.DataFrame(data_miners)
            df_miners.index += 1
            st.dataframe(df_miners, height=330)
            st.form_submit_button("Refresh")

        hide_table_indexes()
        # hide_df_indexes()

        with st.form("miner_distribution"):
            df_md = pd.json_normalize(response["Miner distribution"])
            st.subheader("Miner Distribution")
            st.table(df_md)
            st.form_submit_button("Refresh")

        with st.form("kolka_statistics"):
            df_k = pd.json_normalize(response["Kolka"])
            st.subheader("Kolka Statistics")
            fig = px.bar(df_k, y=["Banned", "Jailed"], barmode="group")
            st.plotly_chart(fig, use_container_width=True)
            st.form_submit_button("Refresh")

        with st.form("server_statistics"):
            filter_ = ["Kolka", "Miner distribution", "Top 10 richest miners"]
            filtered = {k: _ for k, _ in response.items() if k not in filter_}
            st.subheader("Server Statistics")
            for key, value in filtered.items():
                st.code(f"{key}: {value} {'ᕲ' if key in BST else ''}")
            st.form_submit_button("Refresh")

    if type_s[:1] == "2":
        st.write("Under Construction ... 🚧")
        # response = requests.get(f"{url}/statistics_miners").json()
        # df = pd.json_normalize(response.json()['result'])
        # st.subheader("Miners Statistics")
        # st.write(response)
        # st.table(df)

    if type_s[:1] == "3":
        with st.form("hist_stat"):
            response = requests.get(f"{url}/historic_prices").json()
            if response["success"]:
                st.subheader("Historic Prices")
                st.table(pd.json_normalize(response["result"]))
            else:
                st.code(pd.json_normalize(response)["message"][0])
            st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
