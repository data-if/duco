import streamlit as st
import pendulum

from src.utils.helpers import DT_FMT, BST, calc_stake_reward, duco_to_usd, get_duco_price, get_user_balance


def main(username, url):
    with st.form("user_balance"):
        st.subheader(f"{username} Balance")
        response = get_user_balance(username, url)

        if response["success"]:
            duco_price = get_duco_price(url, username)
            for key, value in response["result"].items():
                if value:
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

    with st.form("stake_stats"):
        st.subheader(f"{username} Stakes Statistics")
        import requests
        limit = -1
        response = requests.get(f"{url}/user_transactions/{username}?limit={limit}").json()
        if response["success"]:

            deposit = 0
            last_deposit = 0
            reward = 0

            for tr in response["result"]:
                if tr["memo"]:
                    if tr["memo"] == "Staking deposit":
                        st.write("---")
                        deposit += tr["amount"]
                        st.write(f"Staking deposit: {deposit} on {tr['datetime']}")
                        last_deposit = tr["amount"]
                    elif tr["memo"] == "Staking rewards":
                        reward += tr["amount"]
                        st.write(f"Staking rewards: {reward} on {tr['datetime']}")

            all_time_reward = reward - deposit

            if all_time_reward < 0:
                all_time_reward += last_deposit
            st.code(f"All Time Staking Rewards: {all_time_reward}ᕲ / {duco_to_usd(duco_price, all_time_reward)}")
        st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
