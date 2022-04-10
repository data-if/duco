import streamlit as st
import pendulum
import requests

from src.utils.helpers import DT_FMT, BST, calc_stake_reward, duco_to_usd, get_duco_price


def main(username, url):
    with st.form("user_balance"):
        st.subheader(f"{username} Balance")
        response = requests.get(f"{url}/balances/{username}").json()

        if response["success"]:
            duco_price = get_duco_price(url, username)
            for key, value in response["result"].items():
                if key in ("balance", "stake_date", "stake_amount"):
                    if key in "stake_date":
                        value = pendulum.from_timestamp(value).format(DT_FMT)
                    st.code(f"{key.title().replace('_', ' ')}: {value}{'ᕲ / ' + duco_to_usd(duco_price, value) if key in BST else ''}")

            stake = response["result"]["stake_amount"]
            if stake:
                reward = calc_stake_reward(stake)
                st.code(f"Staking Reward: {reward}ᕲ / {duco_to_usd(duco_price, reward)}")

        else:
            st.code(response["message"])
        st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
