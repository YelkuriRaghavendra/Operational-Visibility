import streamlit as st
from db_init import fetch_data
import pandas as pd
from datetime import datetime, timedelta
import altair as alt

def get_daily_counts(event_type):
    query = f"""
    SELECT created_at::date as date, COUNT(*) as count
    FROM supply_summary
    WHERE last_source_update_event = '{event_type}'
    AND created_at IS NOT NULL
    AND created_at::timestamptz >= current_date - interval '30 days'
    GROUP BY date
    ORDER BY date
    """
    result = fetch_data(query)
    return result

def main():
    st.title("Dashboard")

    # Calculate the date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    date_range = pd.date_range(start=start_date, end=end_date)

    # Fetch daily counts
    fullsync_counts = get_daily_counts('FULL_SYNC')
    stock_update_counts = get_daily_counts('STOCK_UPDATE')

    # Create dataframes for the bar charts and reindex to include all dates
    fullsync_counts.set_index('date', inplace=True)
    fullsync_counts = fullsync_counts.reindex(date_range, fill_value=0).reset_index()
    fullsync_counts.columns = ['date', 'count']

    stock_update_counts.set_index('date', inplace=True)
    stock_update_counts = stock_update_counts.reindex(date_range, fill_value=0).reset_index()
    stock_update_counts.columns = ['date', 'count']

    # Display metrics
    total_fullsync_count = fullsync_counts['count'].sum()
    total_stock_update_count = stock_update_counts['count'].sum()
    total_sync_count = total_fullsync_count + total_stock_update_count

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Fullsync Count", value=total_fullsync_count)
    # Display the date range with increased font size
    col1.markdown(f"<div style='font-size: 25px;'>From {start_date} to {end_date}</div>", unsafe_allow_html=True)

    col2.metric(label="Stock Update Count", value=total_stock_update_count)

    col3.metric(label="Total Sync Count", value=total_sync_count)

    # Create two columns for the graphs
    graph_col1, graph_col2 = st.columns(2)

    # Display bar charts in the columns using Altair
    with graph_col1:
        st.subheader("Fullsync Counts Over the Last 30 Days")
        fullsync_chart = alt.Chart(fullsync_counts).mark_bar().encode(
            x=alt.X('date:T', axis=alt.Axis(format='%Y-%m-%d', title='Date', labelAngle=-45, labelOverlap=False, tickCount=30)),
            y=alt.Y('count:Q', title='Fullsync Count')
        ).properties(
            width=500,
            height=300
        )
        st.altair_chart(fullsync_chart)

    with graph_col2:
        st.subheader("Stock Update Counts Over the Last 30 Days")
        stock_update_chart = alt.Chart(stock_update_counts).mark_bar().encode(
            x=alt.X('date:T', axis=alt.Axis(format='%Y-%m-%d', title='Date', labelAngle=-45, labelOverlap=False, tickCount=30)),
            y=alt.Y('count:Q', title='Stock Update Count')
        ).properties(
            width=500,
            height=300
        )
        st.altair_chart(stock_update_chart)

if __name__ == "__main__":
    main()
