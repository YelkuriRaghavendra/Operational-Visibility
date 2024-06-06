import streamlit as st
from db_init import fetch_data
import pandas as pd

def get_fullsync_count():
    query = """
    SELECT COUNT(*) 
    FROM supply_summary 
    WHERE last_source_update_event = 'FULL_SYNC' 
    AND created_at IS NOT NULL
    AND created_at::timestamptz >= current_date - interval '7 days'
    """
    result = fetch_data(query)
    return result.iloc[0, 0] if not result.empty else 0

def get_stock_update_count():
    query = """
    SELECT COUNT(*) 
    FROM supply_summary 
    WHERE last_source_update_event = 'STOCK_UPDATE' 
    AND created_at IS NOT NULL
    AND created_at::timestamptz >= current_date - interval '7 days'
    """
    result = fetch_data(query)
    return result.iloc[0, 0] if not result.empty else 0

def main():
    st.title("Dashboard")

    # Display metrics
    fullsync_count = get_fullsync_count()
    stock_update_count = get_stock_update_count()

    col1, col2 = st.columns(2)
    col1.metric(label="Fullsync Count", value=fullsync_count)
    col2.metric(label="Deltasync Count", value=stock_update_count)

if __name__ == "__main__":
    main()
