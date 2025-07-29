import streamlit as st
import mysql.connector
import pandas as pd
import altair as alt

# --- Page config ---
st.set_page_config(
    page_title="Pro Tennis Analytics Dashboard",
    layout="wide",
    page_icon="🎾"
)

# --- Custom CSS for a clean modern theme ---
st.markdown("""
    <style>
    body, .reportview-container {
        background-color: #f4f4f4;
        color: #111;
    }
    .stApp {
        background-color: #f4f4f4;
    }
    .css-18e3th9, .css-1d391kg {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        color: #111;
    }
    .stDataFrame th, .stDataFrame td {
        background-color: #ffffff;
        color: #111;
    }
    .metric {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- Connect to MySQL ---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Veerendra@06",
    database="tennis_data"
)
cursor = conn.cursor(dictionary=True)

# --- Fetch data from tables ---
cursor.execute("""
    SELECT c.name, c.country, r.rank, r.points, r.movement
    FROM competitors c
    JOIN competitor_rankings r ON c.competitor_id = r.competitor_id
""")
rank_data = pd.DataFrame(cursor.fetchall())

cursor.execute("SELECT * FROM competitions")
comp_data = pd.DataFrame(cursor.fetchall())

cursor.execute("SELECT * FROM categories")
cat_data = pd.DataFrame(cursor.fetchall())

cursor.execute("SELECT * FROM venues")
venue_data = pd.DataFrame(cursor.fetchall())

cursor.execute("SELECT * FROM complexes")
complex_data = pd.DataFrame(cursor.fetchall())

# --- Header ---
st.markdown("""
    <h1 style='text-align: center; color: #2c3e50;'>Pro Tennis Analytics Dashboard</h1>
""", unsafe_allow_html=True)
st.markdown("---")

# --- Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Competitors", len(rank_data))
col2.metric("Top Rank", rank_data['rank'].min())
col3.metric("Highest Points", rank_data['points'].max())

st.markdown("---")

# --- Filters ---
st.subheader("Filter Competitors")
col_filter1, col_filter2 = st.columns(2)
countries = rank_data['country'].unique().tolist()
selected_country = col_filter1.selectbox("Select Country", ["All"] + countries)
rank_min, rank_max = int(rank_data['rank'].min()), int(rank_data['rank'].max())
selected_range = col_filter2.slider("Rank Range", rank_min, rank_max, (rank_min, min(rank_max, 10)))

# --- Apply Filters ---
filtered_df = rank_data.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
filtered_df = filtered_df[(filtered_df['rank'] >= selected_range[0]) & (filtered_df['rank'] <= selected_range[1])]

st.markdown("### Filtered Competitor Rankings")
st.dataframe(filtered_df, use_container_width=True)

# --- Search ---
st.subheader("Search Player by Name")
search_input = st.text_input("Enter player name:")
if search_input:
    result_df = rank_data[rank_data['name'].str.contains(search_input, case=False)]
    st.dataframe(result_df)

# --- Country-wise Points Chart ---
st.markdown("### Country-wise Total Points")
country_points = rank_data.groupby('country')['points'].sum().reset_index().sort_values(by='points', ascending=False).head(10)
country_chart = alt.Chart(country_points).mark_bar().encode(
    x=alt.X('points:Q', title='Total Points'),
    y=alt.Y('country:N', sort='-x'),
    color=alt.Color('country:N', scale=alt.Scale(scheme='set2')),
    tooltip=['country', 'points']
).properties(height=400, width=700, background='#ffffff')
st.altair_chart(country_chart, use_container_width=True)

# --- Top 5 Player Leaderboard ---
st.markdown("### Top 5 Players by Points")
top5 = rank_data.sort_values(by='points', ascending=False).head(5)
top5_chart = alt.Chart(top5).mark_bar().encode(
    x=alt.X('points:Q', title='Points'),
    y=alt.Y('name:N', sort='-x'),
    color=alt.Color('name:N', scale=alt.Scale(scheme='set3')),
    tooltip=['name', 'points', 'rank', 'country']
).properties(height=300, background='#ffffff')
st.altair_chart(top5_chart, use_container_width=True)

# --- Export to Excel ---
st.subheader("Export Filtered Data")
if st.button("Download as Excel"):
    filtered_df.to_excel("filtered_competitors.xlsx", index=False)
    st.success("Excel file saved as filtered_competitors.xlsx")

# --- Extra Tables ---
st.markdown("### Additional Tables")
with st.expander("View Competitions by Category"):
    st.dataframe(comp_data.merge(cat_data, on="category_id")[["competition_name", "type", "gender", "category_name"]])

with st.expander("View Venues"):
    st.dataframe(venue_data[["venue_name", "city_name", "country_name", "timezone"]])

with st.expander("View Complexes"):
    st.dataframe(complex_data)

st.markdown("---")
st.markdown("<center>Created by Veerendra Kashyap | Powered by Streamlit + MySQL + Python</center>", unsafe_allow_html=True)
