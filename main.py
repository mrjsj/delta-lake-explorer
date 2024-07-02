import streamlit as st
from modules.code_editor import load_code_editor
from modules.sidebar import load_sidebar
from modules.duckdb_result import show_duckdb_result


def main():
    st.set_page_config(page_title="Delta Lake Explorer", page_icon="📊", layout="wide")
    st.title("Delta Lake Explorer")
    load_sidebar()
    load_code_editor()
    show_duckdb_result()
    
if __name__ == "__main__":
    main()