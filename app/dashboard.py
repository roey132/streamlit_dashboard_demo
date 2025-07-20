import streamlit as st
import pandas as pd
import altair as alt


def render_dashboard(df: pd.DataFrame):
    st.set_page_config(layout="wide")
    st.title("🌍 Earthquake Insights Dashboard")
    st.markdown("Analyze global earthquake trends by time, magnitude, severity, and tsunami impact.")

    df['time_utc'] = pd.to_datetime(df['time_utc'])

    # Sidebar filters
    with st.sidebar:
        st.header("⚖️ Filters")
        min_date = df['time_utc'].min().date()
        max_date = df['time_utc'].max().date()
        date_range = st.date_input("Date Range", (max_date - pd.Timedelta(days=7), max_date), min_value=min_date, max_value=max_date)
        mag_range = st.slider("Magnitude Range", float(df['magnitude'].min()), float(df['magnitude'].max()), (float(df['magnitude'].min()), float(df['magnitude'].max())), 0.1)
        show_tsunami_only = st.checkbox("Show Only Tsunami Events", value=False)

    # Filter data
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = df[
        (df['time_utc'] >= start_date) &
        (df['time_utc'] <= end_date) &
        (df['magnitude'] >= mag_range[0]) &
        (df['magnitude'] <= mag_range[1])
    ]
    if show_tsunami_only:
        filtered_df = filtered_df[filtered_df['tsunami'] == 1]

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Earthquakes", len(filtered_df))
    col2.metric("Average Magnitude", f"{filtered_df['magnitude'].mean():.2f}")
    if not filtered_df.empty:
        max_mag_row = filtered_df.loc[filtered_df['magnitude'].idxmax()]
        col3.metric("Strongest Magnitude", f"{max_mag_row['magnitude']:.1f}", label_visibility="visible")
        col4.metric("Tsunami Events", int(filtered_df['tsunami'].sum()))
    else:
        col3.metric("Strongest Magnitude", "N/A")
        col4.metric("Tsunami Events", "0")

    # Map
    st.subheader("🗺️ Earthquake Locations")
    if not filtered_df.empty:
        st.map(filtered_df[['latitude', 'longitude']])
    else:
        st.info("No data to display on map with current filters.")

    # Trend chart: number of quakes per day
    st.subheader("🕛 Daily Earthquake Count")
    daily_counts = filtered_df.copy()
    daily_counts['date'] = daily_counts['time_utc'].dt.date
    daily_counts['date'] = daily_counts['date'].astype(str)  # ✅ convert to string

    daily_chart = alt.Chart(daily_counts.groupby('date').size().reset_index(name='count')).mark_bar().encode(
        x=alt.X('date:O', title='Date', axis=alt.Axis(labelAngle=-45)),
        y='count:Q',
        tooltip=['date:O', 'count:Q']
    ).properties(width=700, height=300)
    st.altair_chart(daily_chart, use_container_width=True)

    # Severity breakdown
    st.subheader("🔹 Magnitude Severity Breakdown")
    def categorize_magnitude(mag):
        if mag < 3.0:
            return "Minor"
        elif mag < 5.0:
            return "Light"
        elif mag < 6.0:
            return "Moderate"
        else:
            return "Strong+"

    filtered_df['severity'] = filtered_df['magnitude'].apply(categorize_magnitude)
    severity_counts = filtered_df['severity'].value_counts().reset_index()
    severity_counts.columns = ['Severity', 'Count']

    bar = alt.Chart(severity_counts).mark_bar().encode(
        x='Severity:N',
        y='Count:Q',
        tooltip=['Severity', 'Count'],
        color='Severity:N'
    ).properties(width=600)
    st.altair_chart(bar, use_container_width=True)

    # Data preview & export
    st.subheader("📊 Filtered Earthquake Data")
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "filtered_earthquakes.csv", "text/csv")
