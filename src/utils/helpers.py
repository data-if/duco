import streamlit as st


DT_FMT = "dddd DD MMMM YYYY"
BST = ("balance", "stake_amount", "All-time mined DUCO")


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

