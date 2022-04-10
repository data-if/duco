import streamlit as st
import requests


def main(url):
    with st.form("get_pool"):
        st.subheader("Get Pool")
        response = requests.get(f"{url}/getPool").json()
        if response["success"]:
            for key, value in response.items():
                if key not in "success":
                    st.code(f"{key.title().replace('_', ' ')}: {value}")

        st.form_submit_button("Refresh")


if __name__ == "__main__":
    main()
