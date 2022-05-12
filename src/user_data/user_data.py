import streamlit as st
import pandas as pd
import requests
import pendulum

from src.utils.helpers import (
    BST,
    DT_FMT,
    duco_to_usd,
    get_temp_hum,
    get_duco_price,
    calc_stake_reward,
    hide_table_indexes,
    calc_by_period,
)


def main(username, url):
    type_u = st.radio(
        "Select data type:", (
            f"1. {username} info",
            "2. All users",
        )
    )

    if type_u[:1] == "1":
        with st.form("user_info"):
            hide_table_indexes()
            response = requests.get(f"{url}/v3/users/{username}").json()
            if response["success"]:
                st.subheader("User Data")
                duco_price = get_duco_price(url, username)
                for key, value in response["result"]["balance"].items():
                    if value:
                        if key not in "username":
                            if key in ("stake_date", "verified_date", "last_login"):
                                value = pendulum.from_timestamp(value).format(DT_FMT)
                            if key == "created" and "before" not in value:
                                value = pendulum.from_format(value, "DD/MM/YYYY HH:mm:ss").format(f"HH:mm:ss {DT_FMT}")
                            st.code(f"{key.title().replace('_', ' ')}: {value}{'ᕲ / ' + duco_to_usd(duco_price, value) if key in BST else ''}")

                stake = response["result"]["balance"]["stake_amount"]
                if stake:
                    reward = calc_stake_reward(stake)
                    st.code(f"Staking Reward: {round(reward)}ᕲ / {duco_to_usd(duco_price, reward)}")

                if response["result"]["miners"]:
                    miners = response["result"]["miners"]
                    df_min = pd.json_normalize(miners)
                    df_min = df_min.sort_values(by="identifier", ascending=True).reset_index(drop=True)
                    df_min.index += 1

                    st.subheader(f"Miners ({df_min.shape[0]})")
                    st.dataframe(df_min.drop(["username"], 1) if df_min.shape[0] > 0 else df_min)

                    get_temp_hum(miners)

                if response["result"]["transactions"]:
                    df_tr = pd.json_normalize(response["result"]["transactions"])
                    df_tr = df_tr.sort_values(by="id", ascending=False).reset_index(drop=True)
                    df_tr.index += 1

                    st.subheader("Transactions")
                    st.dataframe(df_tr)

            else:
                st.code(response["message"])
            st.form_submit_button("Refresh")

        with st.form("daily_reward"):
            st.subheader("Calculate Mined ᕲuco`s")

            _, col = st.columns(2)
            periods = {15: 0.25, 30: 0.5, 60: 1, 180: 3, 300: 5, 600: 10}
            period = col.selectbox("Select period (min):", options=periods.keys(), format_func=lambda x: periods[x])

            calc_by_period(username, url, period, periods, duco_price)

            st.form_submit_button("Calculate")

    elif type_u[:1] == "2":
        st.write("Under Construction ... 🚧")
        # response = requests.get(f"{url}/users/").json()
        st.subheader("All Users")
        # st.json(response)


if __name__ == "__main__":
    main()
