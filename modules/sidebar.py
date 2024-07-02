import streamlit as st

def load_sidebar():
    with st.sidebar:
        st.write("Settings")

        st.checkbox(
            "Enable query parsing",
            value=True,
            key="enable_query_parsing",
            help="""Enables parsing `"catalog"."schema"."table"` to `delta_scan('abfss://{root_path}/{catalog}/{schema}/{table}')` for all `FROM` and `JOIN` statements."""
        )
        st.checkbox("Show parsed query", value=False if not st.session_state["enable_query_parsing"] else True, key="show_parsed_query", help="Shows the parsed query when running a query.", disabled=not st.session_state["enable_query_parsing"])

        st.checkbox(
            label="Show query time",
            key="show_query_time",
            value=True,
        )