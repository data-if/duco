import streamlit as st
import pandas as pd
import requests


def header(usr):
    st.set_page_config(
        page_title="ᕲUCO ᕲATA",
        page_icon="https://raw.githubusercontent.com/revoxhere/duino-coin/master/Resources/duco.png",
        layout="wide",
    )
    st.sidebar.image("https://raw.githubusercontent.com/revoxhere/duino-coin/master/Resources/duco.png", width=300)
    # st.header("ᕲUCO ᕲATA")
    username = st.sidebar.text_input("Username:", usr)
    st.sidebar.button("Go")
    return username


def hide_table_indexes():
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)


def hide_df_indexes():
    # CSS to inject contained in a string
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)


def main():
    username = header("ifdeduco")

    url = "https://server.duinocoin.com/"

    type_r = st.sidebar.radio(
        "Select Data Type:", (
            "1. User Data",
            "2. Transactions",
            "3. Miners",
            "4. Balance",
            "5. Statistics",
            "6. All Pools",
            "7. Get Pool",
            "8. Donate",
        )
    )

    if type_r[:1] == "1":
        type_u = st.radio(
            "Select data type:", (
                "1. Info by username",
                "2. All users",
            )
        )

        if type_u[:1] == "1":
            with st.form("user_info"):
                hide_table_indexes()
                response = requests.get(f"{url}/users/{username}").json()
                if response['success']:
                    df_bal = pd.json_normalize(response['result']['balance'])
                    df_min = pd.json_normalize(response['result']['miners'])
                    df_min.index += 1
                    df_tr = pd.json_normalize(response['result']['transactions'])
                    if response['result']['transactions']:
                        df_tr = df_tr.sort_values(by='datetime', ascending=False).reset_index(drop=True)
                        df_tr.index += 1
                    st.subheader("Balance")
                    st.table(df_bal.drop(["username"], 1))
                    st.subheader(f"Miners ({df_min.shape[0]})")
                    st.dataframe(df_min.drop(["username"], 1) if df_min.shape[0] > 0 else df_min)
                    st.subheader("Transactions")
                    st.dataframe(df_tr)
                else:
                    st.code(pd.json_normalize(response)['message'][0])
                st.form_submit_button("Refresh")

        elif type_u[:1] == "2":
            st.write("Under Construction ... 🚧")
            # response = requests.get(f"{url}/users/").json()
            st.subheader("All Users")
            # st.json(response)

    elif type_r[:1] == "2":
        type_tr = st.radio(
            "Select data type:", (
                "1. User Transactions",
                "2. Transaction By id/hash",
            )
        )

        if type_tr[:1] == "1":
            with st.form("transactions"):
                st.subheader("User Transactions")
                limit = st.number_input("Transactions Count:", min_value=1, value=10, step=1)
                response = requests.get(f"{url}/user_transactions/{username}?limit={limit}").json()
                if response['success']:
                    df = pd.json_normalize(response['result'])
                    if not df.empty:
                        df = df.sort_values(by='datetime', ascending=False).reset_index(drop=True)
                        df.index += 1
                        st.dataframe(df, height=500)
                    else:
                        st.code("User did not have any transactions")
                else:
                    st.code(pd.json_normalize(response)['message'][0])
                st.form_submit_button("Refresh")

        elif type_tr[:1] == "2":
            with st.form("transaction_by_id"):
                hide_df_indexes()
                st.subheader("Transaction By Id")
                tr_id = st.number_input("Input transaction id:", min_value=1, value=1, step=1)
                response = requests.get(f"{url}/id_transactions/{tr_id}").json()
                df = pd.json_normalize(response['result'])
                st.dataframe(df)
                st.form_submit_button("Refresh")
            with st.form("transaction_by_hash"):
                hide_df_indexes()
                st.subheader("Transaction By Hash")
                tr_h = st.text_input("Transaction Hash:", "84b2303d95bcd1dd921350803ae92157d667d627")
                response = requests.get(f"{url}/transactions/{tr_h}").json()
                df = pd.json_normalize(response['result'])
                st.dataframe(df)
                st.form_submit_button("Refresh")

    elif type_r[:1] == "3":
        with st.form("user_miners"):
            st.subheader("Usern Miners")
            response = requests.get(f"{url}/miners/{username}").json()
            hide_table_indexes()
            if response['success']:
                df = pd.json_normalize(response['result'])
                df.index += 1
                st.dataframe(df.drop(["username"], 1), height=1000)
            else:
                st.code(pd.json_normalize(response)['message'][0])
            st.form_submit_button("Refresh")

    elif type_r[:1] == "4":
        with st.form("user_balance"):
            st.subheader("Usern Balance")
            response = requests.get(f"{url}/balances/{username}").json()
            hide_table_indexes()
            df = pd.json_normalize(response['result'])
            st.table(df.drop(["username"], 1))
            st.form_submit_button("Refresh")

    elif type_r[:1] == "5":
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
                m_list = pd.json_normalize(response)['Top 10 richest miners'][0]
                data_miners = {
                    "Miner": [m.split('- ')[1] for m in m_list],
                    "DUCO": [d.split('DUCO - ')[0] for d in m_list],
                }
                df_miners = pd.DataFrame(data_miners)
                df_miners.index += 1
                st.dataframe(df_miners, height=330)
                st.form_submit_button("Refresh")

            hide_table_indexes()
            # hide_df_indexes()

            with st.form("miner_distribution"):
                df_md = pd.json_normalize(response['Miner distribution'])
                st.subheader("Miner Distribution")
                st.table(df_md)
                st.form_submit_button("Refresh")

            with st.form("kolka_statistics"):
                df_k = pd.json_normalize(response['Kolka'])
                st.subheader("Kolka Statistics")
                st.table(df_k)
                st.form_submit_button("Refresh")

            with st.form("server_statistics"):
                filter_ = ['Kolka', 'Miner distribution', 'Top 10 richest miners']
                filtered = {k: _ for k, _ in response.items() if k not in filter_}
                df = pd.json_normalize(filtered)
                st.subheader("Server Statistics")
                st.dataframe(df)
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
                if response['success']:
                    st.subheader("Historic Prices")
                    st.table(pd.json_normalize(response['result']))
                else:
                    st.code(pd.json_normalize(response)['message'][0])
                st.form_submit_button("Refresh")

    elif type_r[:1] == "6":
        with st.form("all_pools"):
            response = requests.get(f"{url}/all_pools").json()
            if response['success']:
                df = pd.json_normalize(response['result'])
                df.index += 1
                st.subheader("All Pools")
                st.dataframe(df, height=1000)
            else:
                st.code(pd.json_normalize(response)['message'][0])
            st.form_submit_button("Refresh")

    elif type_r[:1] == "7":
        with st.form("get_pool"):
            st.subheader("Get Pool")
            response = requests.get(f"{url}/getPool").json()
            df = pd.json_normalize(response)
            hide_table_indexes()
            st.table(df)
            st.form_submit_button("Refresh")

    elif type_r[:1] == "8":
        st.subheader("Donate")
        js = """
        <iframe 
            id='kofiframe' 
            src='https://ko-fi.com/kosarevsky/?hidefeed=true&widget=true&embed=true&preview=true' 
            style='border:none;width:100%;padding:4px;background:#a9a9a9;' 
            height='712' 
            title='kosarevsky'
        >
        </iframe>
        """

        st.markdown(js, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

