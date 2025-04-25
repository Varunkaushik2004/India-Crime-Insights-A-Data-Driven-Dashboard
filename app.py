# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import subprocess

if st.sidebar.button("🔄 Re-run Pipeline"):
    with st.spinner("Cleaning latest data..."):
        subprocess.run(["python", "pipeline.py"])
        st.success("Pipeline re-executed. Latest data is now loaded!")
        st.cache_data.clear()  # Clear cache to reload fresh data
        st.rerun()

# Load cleaned data
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/cleaned_crime_data_final.csv", parse_dates=["Date Reported", "Date of Occurrence", "Date Case Closed"])
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🧊 Filter Data")

all_years = sorted(df['Year'].unique())
all_states = sorted(df['City'].unique())
all_crimes = sorted(df['Crime Description'].unique())

years = st.sidebar.multiselect("Select Year(s)", options=["All"] + all_years, default=["All"])
states = st.sidebar.multiselect("Select State/UT(s)", options=["All"] + all_states, default=["All"])
crime_types = st.sidebar.multiselect("Select Crime Type(s)", options=["All"] + all_crimes, default=["All"])

# Apply filters with 'All' support
filtered_df = df.copy()
if "All" not in years:
    filtered_df = filtered_df[filtered_df['Year'].isin(years)]
if "All" not in states:
    filtered_df = filtered_df[filtered_df['City'].isin(states)]
if "All" not in crime_types:
    filtered_df = filtered_df[filtered_df['Crime Description'].isin(crime_types)]

# --- Title & Description ---
st.title("🔍 Crime in India Dashboard")
st.markdown("Analyze trends in crime across states, time, and types using this interactive dashboard.")

# --- Key Metrics Section ---
st.markdown("### 📊 Key Metrics")
total_crimes = filtered_df.shape[0]
most_common_crime = filtered_df['Crime Description'].mode()[0] if not filtered_df.empty else "N/A"
state_with_max_crimes = filtered_df['City'].value_counts().idxmax() if not filtered_df.empty else "N/A"
avg_closure_time = round(filtered_df['Closure Time (Days)'].mean(), 2) if 'Closure Time (Days)' in filtered_df.columns else "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Crimes", total_crimes)
col2.metric("Most Common Crime", most_common_crime)
col3.metric("Highest Crime City", state_with_max_crimes)
col4.metric("Avg Closure Time", avg_closure_time)

st.divider()

# --- Line Chart: Crimes Over Time ---
st.markdown("### 📈 Crimes Over Years")
line_data = filtered_df.groupby("Year").size().reset_index(name="Crime Count")
fig_line = px.line(line_data, x="Year", y="Crime Count", markers=True, title="Total Crimes per Year")
st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# --- Bar Chart: Crimes by State ---
st.markdown("### 🏙️ Crimes by City/State")
bar_data = filtered_df['City'].value_counts().reset_index()
bar_data.columns = ['City', 'Crime Count']
fig_bar = px.bar(bar_data, x='City', y='Crime Count', title='Crimes by City/State', color='Crime Count')
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# --- Pie Chart: Crime Type Distribution ---
st.markdown("### 🧩 Crime Type Distribution")
pie_data = filtered_df['Crime Description'].value_counts().reset_index()
pie_data.columns = ['Crime Type', 'Count']
fig_pie = px.pie(pie_data, names='Crime Type', values='Count', hole=0.4, title='Crime Type Share')
st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# --- Heatmap: Month vs Day ---
st.markdown("### 📅 Heatmap: Crimes by Month and Day of Week")
if not filtered_df.empty:
    heatmap_data = filtered_df.groupby(['Month', 'Day of Week']).size().reset_index(name='Crimes')
    pivot = heatmap_data.pivot(index='Day of Week', columns='Month', values='Crimes').fillna(0)
    fig_heatmap = px.imshow(pivot, labels=dict(x="Month", y="Day of Week", color="Number of Crimes"),
                            x=pivot.columns, y=pivot.index,
                            title="Heatmap of Crimes by Month and Day")
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    st.info("Not enough data to generate heatmap.")

st.divider()

# --- Map Chart: Crime by City (Fake coords for now) ---
st.markdown("### 🗺️ Crime Density by City")

city_coords = {
    "Delhi": [28.6139, 77.2090],
    "Mumbai": [19.0760, 72.8777],
    "Bangalore": [12.9716, 77.5946],
    "Chennai": [13.0827, 80.2707],
    "Kolkata": [22.5726, 88.3639],
    "Hyderabad": [17.3850, 78.4867],
    "Pune": [18.5204, 73.8567],
    "Ahmedabad": [23.0225, 72.5714],
    "Jaipur": [26.9124, 75.7873],
    "Lucknow": [26.8467, 80.9462],
}

map_data = filtered_df['City'].value_counts().reset_index()
map_data.columns = ['City', 'Crime Count']
map_data['lat'] = map_data['City'].map(lambda x: city_coords.get(x, [0, 0])[0])
map_data['lon'] = map_data['City'].map(lambda x: city_coords.get(x, [0, 0])[1])

fig_map = px.scatter_mapbox(
    map_data,
    lat="lat",
    lon="lon",
    size="Crime Count",
    color="Crime Count",
    hover_name="City",
    zoom=4,
    mapbox_style="carto-positron",
    title="Crime Density by City (Bubble Map)"
)
st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# --- Solved vs Unsolved Cases ---
st.markdown("### 🔒 Solved vs Unsolved Cases")
if 'Case Closed' in filtered_df.columns:
    solved_unsolved_data = filtered_df['Case Closed'].value_counts().reset_index()
    solved_unsolved_data.columns = ['Case Status', 'Count']
    fig_status = px.pie(solved_unsolved_data, names='Case Status', values='Count', hole=0.4, title='Solved vs Unsolved Cases')
    st.plotly_chart(fig_status, use_container_width=True)
else:
    st.info("No case closure data available for Solved vs Unsolved chart.")

st.divider()

# --- Victim Gender Distribution ---
st.markdown("### 👩‍🦱 Victim Gender Distribution")
gender_data = filtered_df['Victim Gender'].value_counts().reset_index()
gender_data.columns = ['Gender', 'Count']
fig_gender = px.pie(gender_data, names='Gender', values='Count', hole=0.4, title='Victim Gender Distribution')
st.plotly_chart(fig_gender, use_container_width=True)

st.divider()

# --- Victim Age Distribution ---
st.markdown("### 📊 Victim Age Distribution")
if 'Victim Age' in filtered_df.columns:
    fig_age = px.histogram(filtered_df, x='Victim Age', nbins=30, title='Distribution of Victim Age')
    st.plotly_chart(fig_age, use_container_width=True)
else:
    st.info("Victim Age data is unavailable.")

st.divider()

# --- Weapon Used in Crime ---
st.markdown("### 🔪 Weapon Used in Crime")
if 'Weapon Used' in filtered_df.columns:
    weapon_data = filtered_df['Weapon Used'].value_counts().reset_index()
    weapon_data.columns = ['Weapon', 'Count']
    fig_weapon = px.pie(weapon_data, names='Weapon', values='Count', hole=0.4, title='Weapon Used in Crime')
    st.plotly_chart(fig_weapon, use_container_width=True)
else:
    st.info("Weapon data is unavailable.")

st.divider()

# --- Crime Type by Year ---
st.markdown("### 🕒 Crime Type by Year")
crime_by_year = filtered_df.groupby(['Year', 'Crime Description']).size().reset_index(name='Crime Count')
fig_crime_by_year = px.bar(crime_by_year, x='Year', y='Crime Count', color='Crime Description', title='Crime Type by Year')
st.plotly_chart(fig_crime_by_year, use_container_width=True)

st.divider()

# --- Crime Cases by Month ---
st.markdown("### 📅 Crimes by Month")
monthly_data = filtered_df.groupby("Month").size().reset_index(name="Crime Count")
fig_monthly = px.bar(monthly_data, x="Month", y="Crime Count", title="Crimes by Month")
st.plotly_chart(fig_monthly, use_container_width=True)

st.divider()

# --- Auto Insights ---
st.markdown("### 🧠 Auto Insights")
if not filtered_df.empty:
    insights = []

    max_city = filtered_df['City'].value_counts().idxmax()
    top_crime = filtered_df['Crime Description'].value_counts().idxmax()
    month_max = filtered_df['Month'].value_counts().idxmax()
    weekday_max = filtered_df['Day of Week'].value_counts().idxmax()

    insights.append(f"🔺 **{max_city}** has the highest number of reported crimes.")
    insights.append(f"📌 The most reported crime is **{top_crime}**.")
    insights.append(f"📅 **{month_max}** sees the most crime incidents.")
    insights.append(f"🕒 **{weekday_max}** is the most common day for crimes.")

    for i in insights:
        st.markdown(f"- {i}")
else:
    st.info("Not enough data to generate insights.")

st.divider()

# --- Data Table ---
st.markdown("### 🗃️ Filtered Data Table")
st.dataframe(filtered_df)

# --- CSV Download Button ---
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_crime_data.csv',
    mime='text/csv',
)

# --- Footer ---
st.markdown("""---""")
st.markdown("**Created by Varun Kaushik | BCA, DSEU Dwarka | 2025**")
