import streamlit as st

from src.user_data import user_data
from src.transactions import transactions
from src.miners import miners
from src.balance import balance
from src.statistics import statistics
from src.all_pools import all_pools
from src.pool import pool
from src.utils.helpers import get_duco_price


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


def main():
    username = header("revox")

    url = "https://server.duinocoin.com/"

    type_r = st.sidebar.radio(
        "Select Data Type:", (
            "1. User Data",
            "2. Transactions",
            "3. Miners & Sensors",
            "4. Balance",
            "5. Statistics",
            "6. All Pools",
            "7. Get Pool",
            # "8. Donate",
        )
    )

    duco_price = get_duco_price(url, username)
    if duco_price:
        st.sidebar.code(f"ᕲuco Price: ≈{duco_price:.6f}$")

    st.sidebar.markdown("[project repo](https://github.com/data-if/duco)")

    if type_r[:1] == "1":
        user_data.main(username, url)

    elif type_r[:1] == "2":
        transactions.main(username, url)

    elif type_r[:1] == "3":
        miners.main(username, url)

    elif type_r[:1] == "4":
        balance.main(username, url)

    elif type_r[:1] == "5":
        statistics.main(url)

    elif type_r[:1] == "6":
        all_pools.main(url)

    elif type_r[:1] == "7":
        pool.main(url)

    # elif type_r[:1] == "8":
    #     st.subheader("Donate")
    #     js = """
    #     <iframe
    #         id='kofiframe'
    #         src='https://ko-fi.com/kosarevsky/?hidefeed=true&widget=true&embed=true&preview=true'
    #         style='border:none;width:100%;padding:4px;background:#a9a9a9;'
    #         height='712'
    #         title='kosarevsky'
    #     >
    #     </iframe>
    #     """
    #
    #     st.markdown(js, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

