import streamlit as st
import requests
from requests import JSONDecodeError
from time import sleep

DT_FMT = "dddd DD MMMM YYYY"
BST = ("balance", "stake_amount", "All-time mined DUCO")
STAKING_PERC = 1.5


def calc_by_period(username, url, period, periods, duco_price):
    response = get_user_balance(username, url)

    with st.spinner("Calculating..."):
        if response["success"]:
            balance = get_user_balance(username, url)["result"]["balance"]
            sleep(period)
            new_balance = get_user_balance(username, url)["result"]["balance"]

            minutes = periods[period]
            earned = new_balance - balance

            if not earned:
                calc_by_period(username, url, period, periods, duco_price)

            if earned:
                minutely = earned * (1 // minutes) if minutes < 1 else earned / minutes
                hourly = minutely * 60
                daily = hourly * 24
                weekly = daily * 7
                monthly = daily * 30
                yearly = daily * 365

                c1, c2 = st.columns(2)
                c1.write(f"Minutely: ≈{round(minutely, 2)}ᕲ")
                c1.write(f"Hourly: ≈{round(hourly, 2)}ᕲ {duco_to_usd(duco_price, hourly, 4)}")
                c1.write(f"Daily: ≈{round(daily, 2)}ᕲ {duco_to_usd(duco_price, daily, 4)}")
                c2.write(f"Weekly: ≈{round(weekly, 2)}ᕲ {duco_to_usd(duco_price, weekly)}")
                c2.write(f"Monthly: ≈{round(monthly, 2)}ᕲ {duco_to_usd(duco_price, monthly)}")
                c2.write(f"Yearly: ≈{round(yearly, 2)}ᕲ {duco_to_usd(duco_price, yearly)}")

        else:
            st.code(response["message"])

    return


def get_duco_price(url, username):
    response = requests.get(f"{url}/v3/users/{username}").json()
    if response["success"]:
        st.code(response["result"])
        return response["result"]["prices"]["max"]


def get_user_balance(username, url):
    response = requests.get(f"{url}/balances/{username}")
    try:
        response = response.json()
    except JSONDecodeError:
        response = get_user_balance(username, url)

    return response


def duco_to_usd(duco_price, val, nums=2):
    return f"≈{round(duco_price * val, nums)}$"


def calc_stake_reward(stake):
    return round(stake * (1 + (STAKING_PERC/100)) - stake)


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


def get_temp_hum(miners):
    st.subheader("Sensors Data") if any(m["it"] for m in miners) else ""
    for miner in miners:
        if miner["it"]:
            temp = miner["it"].split("@")[0]
            hum = miner["it"].split("@")[1]
            if temp not in "error":
                st.code(f"Identifier: {miner['identifier']}")
                st.code(f"Temperature: {temp}°C / {(float(temp) * 9 / 5) + 32}°F")
                st.code(f"Humidity: {hum}%")
                st.markdown("---")


def get_transactions_limit():
    col1, _, _ = st.columns(3)
    with col1:
        limit = st.number_input("Transactions Count:", min_value=1, value=10, step=1)
    return limit
