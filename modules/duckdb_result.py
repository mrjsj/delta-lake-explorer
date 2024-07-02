import re
import streamlit as st
import duckdb
from datetime import datetime, timezone

def _parse_query(query: str) -> str:
    
    query = query.strip(";")
    patterns = [re.compile(r'(?<!\S)(FROM|JOIN)\s+([\w\-\"]+)\.([\w\-\"]+)\.([\w\-\"]+)', re.IGNORECASE)]
    root_path = st.secrets["DELTA_LAKE_ROOT_PATH"].strip("/")
    root_path = root_path + "/" if root_path != "" else ""

    def replacement(match):
        keyword = match.group(1)
        catalog = match.group(2).strip('"')
        schema = match.group(3).strip('"')
        table = match.group(4).strip('"')
        return f"{keyword} delta_scan('abfss://{root_path}{catalog}/{schema}/{table}')"
    
    new_query = query
    for pattern in patterns:
        new_query = re.sub(pattern, replacement, new_query)

    return new_query

def _setup_database() -> duckdb.DuckDBPyConnection:
    if "db" not in st.session_state:

        db = duckdb.connect(database=':memory:')

        if not ("AZURE_TENANT_ID" in st.secrets and "AZURE_CLIENT_ID" in st.secrets and "AZURE_CLIENT_SECRET" in st.secrets):           
            db.sql(f"""
                INSTALL delta; LOAD delta;
                INSTALL azure; LOAD azure;
                CREATE SECRET azure_secret (
                    TYPE AZURE,
                    PROVIDER CREDENTIAL_CHAIN,
                    CHAIN 'cli',
                    ACCOUNT_NAME {st.secrets["STORAGE_ACCOUNT_NAME"]}
                );
            """)
            

        else:
            db.sql(
                f"""
                    INSTALL delta; LOAD delta;
                    INSTALL azure; LOAD azure;
                    CREATE SECRET azure_secret (
                        TYPE AZURE,
                        PROVIDER SERVICE_PRINCIPAL,
                        ACCOUNT_NAME '{st.secrets["STORAGE_ACCOUNT_NAME"]}',
                        TENANT_ID '{st.secrets["AZURE_TENANT_ID"]}',
                        CLIENT_ID '{st.secrets["AZURE_CLIENT_ID"]}',
                        CLIENT_SECRET '{st.secrets["AZURE_CLIENT_SECRET"]}'
                    );
                """)
        
        st.session_state["db"] = db

    return st.session_state["db"]

def get_duckdb_result(query: str):

    if st.session_state["enable_query_parsing"]:
        query = _parse_query(query)

    if st.session_state["show_parsed_query"]:
        st.write("Parsed Query:")
        st.code(query, language="sql")

    db = _setup_database()

    return db.sql(query).df()


def show_duckdb_result():
    if "query" in st.session_state and st.session_state["query"] is not None:

        if st.session_state["query"]["text"] == "":
            return

        query = st.session_state["query"]["text"]
        with st.spinner("Loading..."):
            start_time = datetime.now(timezone.utc)
            result = get_duckdb_result(query)
            end_time = datetime.now(timezone.utc)

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=False
            )
            if st.session_state["show_query_time"]:
                st.status(f"Query completed in {end_time - start_time}", state="complete", expanded=False)