import streamlit as st
import pandas as pd
import requests


def header():
    # st.set_page_config(initial_sidebar_state="collapsed")
    st.sidebar.image('https://raw.githubusercontent.com/revoxhere/duino-coin/master/Resources/duco.png', width=300)
    st.sidebar.markdown("---")
    st.header("DUCO data")
    st.markdown("---")


def main():
    header()

    url = "https://server.duinocoin.com/"

    type_r = st.sidebar.radio(
        "Select data type:", (
            "1. User data",
            "2. Transactions",
            "3. Miners",
            "4. Balance",
            "5. Statistics",
            "6. All pools",
            "7. Get pool",
            "8. Ping",
            "9. IP",
        )
    )
    st.sidebar.markdown("---")

    if type_r[:1] == "1":
        type_u = st.radio(
            "Select data type:", (
                "1. Info by username",
                "2. All users",
            )
        )

        if type_u[:1] == "1":
            st.subheader("User info")
            username = st.text_input("Input username:", "revox")
            st.button("Find")
            response = requests.get(f"{url}/users/{username}").json()

            df_bal = pd.json_normalize(response['result']['balance'])
            df_min = pd.json_normalize(response['result']['miners'])
            df_min.index += 1
            df_tr = pd.json_normalize(response['result']['transactions'])
            df_tr = df_tr.sort_values(by='datetime', ascending=False).reset_index(drop=True)
            df_tr.index += 1

            st.subheader("Balance")
            st.table(df_bal)
            st.subheader("User miners")
            st.table(df_min)
            st.subheader("User transactions")
            st.table(df_tr)

        elif type_u[:1] == "2":
            st.write("Under construction ... 🚧")
            # response = requests.get(f"{url}/users/").json()
            st.subheader("All users")
            # st.json(response)

    elif type_r[:1] == "2":
        type_tr = st.radio(
            "Select data type:", (
                "1. User transactions",
                "2. Transaction by id",
                "3. Transaction by hash",
            )
        )
        st.markdown("---")

        if type_tr[:1] == "1":
            st.subheader("User transactions")
            c1, c2 = st.columns(2)
            username = c1.text_input("Input username:", "revox")
            limit = c2.number_input("Input count of transactions:", min_value=1, value=10, step=1)
            st.button("Find data")
            response = requests.get(f"{url}/user_transactions/{username}?limit={limit}").json()
            df = pd.json_normalize(response['result'])
            df = df.sort_values(by='datetime', ascending=False).reset_index(drop=True)
            df.index += 1
            st.table(df)

        elif type_tr[:1] == "2":
            st.subheader("Transaction by id")
            tr_id = st.number_input("Input transaction id:", min_value=1, value=1, step=1)
            st.button("Find data")
            response = requests.get(f"{url}/id_transactions/{tr_id}").json()
            df = pd.json_normalize(response['result'])
            st.table(df)

        elif type_tr[:1] == "3":
            st.subheader("Transaction by hash")
            tr_h = st.text_input("Input transaction hash:", "84b2303d95bcd1dd921350803ae92157d667d627")
            st.button("Find data")
            response = requests.get(f"{url}/transactions/{tr_h}").json()
            df = pd.json_normalize(response['result'])
            st.table(df)

    elif type_r[:1] == "3":
        st.subheader("Miners by username")
        username = st.text_input("Input username:", "revox")
        st.button("Find data")
        response = requests.get(f"{url}/miners/{username}").json()
        if response['success']:
            df = pd.json_normalize(response['result'])
            df.index += 1
            st.table(df)
        else:
            st.table(pd.json_normalize(response))

    elif type_r[:1] == "4":
        st.subheader("Balance by username")
        username = st.text_input("Input username:", "revox")
        st.button("Find data")
        response = requests.get(f"{url}/balances/{username}").json()
        df = pd.json_normalize(response['result'])
        st.table(df)

    elif type_r[:1] == "5":
        type_s = st.radio(
            "Select data type:", (
                "1. Server statistics",
                "2. Miners statistics",
                "3. Historic prices",
            )
        )
        st.markdown("---")

        if type_s[:1] == "1":
            response = requests.get(f"{url}/statistics").json()
            filter_ = ['Kolka', 'Miner distribution', 'Top 10 richest miners']
            filtered = {k: _ for k, _ in response.items() if k not in filter_}
            df = pd.json_normalize(filtered)
            st.subheader("Server statistics")
            st.table(df)

            df_k = pd.json_normalize(response['Kolka'])
            st.subheader("Kolka statistics")
            st.table(df_k)

            df_md = pd.json_normalize(response['Miner distribution'])
            st.subheader("Miner distribution")
            st.table(df_md)

            st.subheader("Top 10 richest miners")
            m_list = pd.json_normalize(response)['Top 10 richest miners'][0]
            data_miners = {
                "Miner": [m.split('- ')[1] for m in m_list],
                "DUCO": [d.split('DUCO - ')[0] for d in m_list],
            }
            df_miners = pd.DataFrame(data_miners)
            df_miners.index += 1
            st.table(df_miners)

        if type_s[:1] == "2":
            st.write("Under construction ... 🚧")
            # response = requests.get(f"{url}/statistics_miners").json()
            # df = pd.json_normalize(response.json()['result'])
            # st.subheader("Miners statistics")
            # st.write(response)
            # st.table(df)

        if type_s[:1] == "3":
            response = requests.get(f"{url}/historic_prices").json()
            if response['success']:
                st.subheader("Historic prices")
                st.table(pd.json_normalize(response['result']))
            else:
                st.table(pd.json_normalize(response))

    elif type_r[:1] == "6":
        response = requests.get(f"{url}/all_pools").json()
        df = pd.json_normalize(response['result'])
        df.index += 1
        st.subheader("All pools")
        st.table(df)

    elif type_r[:1] == "7":
        response = requests.get(f"{url}/getPool").json()
        df = pd.json_normalize(response)
        st.subheader("Pool")
        st.table(df)

    elif type_r[:1] == "8":
        response = requests.get(f"{url}/ping").json()
        df = pd.json_normalize(response)
        st.subheader("Ping")
        st.table(df)

    elif type_r[:1] == "9":
        response = requests.get(f"{url}/ip").json()
        df = pd.json_normalize(response)
        st.subheader("Ip")
        st.table(df)

    st.markdown("---")


if __name__ == "__main__":
    main()

