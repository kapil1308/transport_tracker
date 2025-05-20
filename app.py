import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from wordcloud import WordCloud
import numpy as np
import time
import os
from scipy.stats import ttest_ind

# Set page config
st.set_page_config(page_title="Germany Transport Efficiency Tracker", layout="wide")

# Initialize session state for A/B testing
if "ab_group" not in st.session_state:
    st.session_state.ab_group = np.random.choice(["A", "B"])
if "interactions" not in st.session_state:
    st.session_state.interactions = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# Title and description
st.title("Germany Public Transport Efficiency Tracker")
st.markdown("Analyze train delays and public sentiment for Deutsche Bahn services.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("train_delays.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

# Log A/B test results
def log_results():
    time_spent = time.time() - st.session_state.start_time
    log_data = {
        "group": st.session_state.ab_group,
        "interactions": st.session_state.interactions,
        "time_spent_seconds": round(time_spent, 2)
    }
    log_df = pd.DataFrame([log_data])
    log_file = "ab_test_results.csv"
    if os.path.exists(log_file):
        log_df.to_csv(log_file, mode="a", header=False, index=False)
    else:
        log_df.to_csv(log_file, mode="w", header=True, index=False)

if st.button("Log Session (Simulates Exit)"):
    log_results()
    st.success("Session logged!")

# Mock station coordinates
station_coords = {
    "Hauptbahnhof_Berlin": [52.5256, 13.3694],
    "Hauptbahnhof_Munich": [48.1404, 11.5583],
    "Hauptbahnhof_Hamburg": [53.5529, 10.0064],
    "Zoo Station_Berlin": [52.5071, 13.3324],
    "Südbahnhof_Munich": [48.1278, 11.5517],
    "Südbahnhof_Hamburg": [53.5488, 10.0263]
}

# Delay map
st.subheader("Delay Map by Station")
avg_delays = df.groupby(["station", "city"])["delay_minutes"].mean().reset_index()
m = folium.Map(location=[51.1657, 10.4515], zoom_start=6)
for _, row in avg_delays.iterrows():
    station, city, delay = row["station"], row["city"], row["delay_minutes"]
    key = f"{station}_{city}"
    if key in station_coords:
        lat, lon = station_coords[key]
        folium.CircleMarker(
            location=[lat, lon],
            radius=max(5, delay * 2),
            popup=f"{station}, {city}: {delay:.1f} min",
            color="red" if delay > 10 else "orange" if delay > 5 else "green",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
st_folium(m, width=700, height=400)

# Delay distribution with A/B testing
st.subheader("Delay Distribution")
city = st.selectbox("Select City", options=["All"] + sorted(df["city"].unique()), key="city_select")
st.session_state.interactions += 1
filtered_df = df if city == "All" else df[df["city"] == city]
if st.session_state.ab_group == "A":
    fig = px.histogram(filtered_df, x="delay_minutes", nbins=20, title="Delay Distribution (Minutes) - Histogram",
                       labels={"delay_minutes": "Delay (Minutes)", "count": "Frequency"})
    fig.update_layout(bargap=0.1)
else:
    fig = px.box(filtered_df, y="delay_minutes", title="Delay Distribution (Minutes) - Box Plot",
                 labels={"delay_minutes": "Delay (Minutes)"})
st.plotly_chart(fig, use_container_width=True)
st.markdown(f"*Viewing Variant {'A (Histogram)' if st.session_state.ab_group == 'A' else 'B (Box Plot)'}*")

# Sentiment word cloud
st.subheader("Public Sentiment (Mock X Posts)")
mock_posts = [
    "Deutsche Bahn delayed again, terrible service",
    "ICE train was on time, great experience",
    "DB needs better punctuality, frustrating",
    "Love the new trains, but delays ruin it"
]
text = " ".join(mock_posts)
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
st.image(wordcloud.to_array(), use_container_width=True)
st.caption("Word cloud based on simulated X posts about Deutsche Bahn.")
st.markdown("*Note*: Real-time sentiment requires X API access.")

# Reliability score
st.subheader("Route Reliability")
reliability = df.groupby("route").agg(
    total_trips=("delay_minutes", "count"),
    on_time=("delay_minutes", lambda x: (x < 5).sum())
).reset_index()
reliability["reliability_score"] = (reliability["on_time"] / reliability["total_trips"] * 100).round(1)
st.table(reliability[["route", "reliability_score"]].sort_values("reliability_score", ascending=False))

# A/B test results analysis
st.subheader("A/B Test Results (Admin View)")
if st.checkbox("Show A/B Test Analysis"):
    if os.path.exists("ab_test_results.csv"):
        results_df = pd.read_csv("ab_test_results.csv")
        summary = results_df.groupby("group").agg(
            avg_interactions=("interactions", "mean"),
            avg_time_spent=("time_spent_seconds", "mean"),
            count=("group", "count")
        ).round(2).reset_index()
        st.table(summary)
        group_a = results_df[results_df["group"] == "A"]["interactions"]
        group_b = results_df[results_df["group"] == "B"]["interactions"]
        if len(group_a) > 1 and len(group_b) > 1:
            t_stat, p_value = ttest_ind(group_a, group_b, equal_var=False)
            st.write(f"T-test for Interactions: p-value = {p_value:.4f}")
            st.write("Significant difference between groups (p < 0.05)." if p_value < 0.05 else
                     "No significant difference between groups (p >= 0.05).")
    else:
        st.write("No A/B test data available yet.")