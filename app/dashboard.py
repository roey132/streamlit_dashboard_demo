import streamlit as st
import pandas as pd

def render_dashboard(df: pd.DataFrame):
    st.title("🌍 Earthquake Dashboard")
    st.markdown("Live demo using S3 + Athena + Streamlit")

    # Filter
    df['time_utc'] = pd.to_datetime(df['time_utc'])
    max_date = df['time_utc'].max()
    min_date = df['time_utc'].min()

    date_range = st.slider("Select date range", min_value=min_date.date(), max_value=max_date.date(), value=(max_date.date() - pd.Timedelta(days=30), max_date.date()))
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = df[(df['time_utc'] >= start) & (df['time_utc'] <= end)]

    # Map
    st.map(filtered_df[['latitude', 'longitude']])

    # Chart
    st.bar_chart(filtered_df['magnitude'])

    # Table
    st.dataframe(filtered_df)
