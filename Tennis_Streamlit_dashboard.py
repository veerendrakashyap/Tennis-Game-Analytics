import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(page_title="Tennis Game Analytics Dashboard", layout="wide")

# Custom Styling
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #fdfdfd;
    color: #222;
    font-size: 18px;
}
.stApp {
    background-color: #fdfdfd;
}
.block-container {
    padding: 2rem;
}
.stMetric {
    background-color: #ffffff;
    border: 2px solid #8e44ad;
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    font-size: 22px;
    color: #000;
    font-weight: bold;
}
.stDataFrame, .dataframe {
    background-color: #ffffff;
    color: #1a1a1a;
    font-size: 18px;
}
.stTabs [role="tab"] {
    font-size: 18px;
    padding: 12px;
    font-weight: bold;
}
h1, h2, h3, .stSubheader, .stMarkdown h2 {
    color: #2c3e50;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Sidebar - Filters and branding
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/3e/Tennis_Racket_and_Balls.jpg", use_container_width=True)
st.sidebar.title("Filter Competitors")

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Veerendra@06",
    database="tennis_data"
)
cursor = conn.cursor(dictionary=True)

# Fetch data
cursor.execute("""
    SELECT c.name, c.country, r.rank, r.points, r.movement, r.competitions_played
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

# Sidebar Filters
countries = ["All"] + sorted(rank_data['country'].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", countries)
rank_min, rank_max = int(rank_data['rank'].min()), int(rank_data['rank'].max())
selected_range = st.sidebar.slider("Rank Range", rank_min, rank_max, (rank_min, rank_min + 10))
search_name = st.sidebar.text_input("Search by Player Name")

# Apply filters
filtered_df = rank_data.copy()
if selected_country != "All":
    filtered_df = filtered_df[filtered_df['country'] == selected_country]
filtered_df = filtered_df[(filtered_df['rank'] >= selected_range[0]) & (filtered_df['rank'] <= selected_range[1])]
if search_name:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False)]

# Title and KPIs
st.title("Tennis Game Analytics Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Competitors", len(rank_data))
col2.metric("Top Rank", rank_data['rank'].min())
col3.metric("Highest Points", rank_data['points'].max())
col4.metric("Countries Represented", rank_data['country'].nunique())

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Leaderboard", "Competitor Insights", "Competitions & Venues",
    "Country View", "Charts & Trends"
])

# Tab 1: Leaderboard
with tab1:
    st.subheader("Top 10 Players by Points")
    top10 = rank_data.sort_values(by='points', ascending=False).head(10)
    fig = px.bar(top10, x='points', y='name', color='country', orientation='h',
                 title="Top 10 Competitors", color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Top 5 Most Active Players")
    active_players = rank_data.sort_values(by='competitions_played', ascending=False).head(5)
    st.dataframe(active_players)

# Tab 2: Competitor Insights
with tab2:
    st.subheader("Filtered Competitors")
    st.dataframe(filtered_df)

# Tab 3: Competitions & Venues
with tab3:
    st.subheader("Competitions by Category")
    merged_comp = comp_data.merge(cat_data, on="category_id")
    st.dataframe(merged_comp[["competition_name", "type", "gender", "category_name"]])

    st.subheader("Venues")
    st.dataframe(venue_data[["venue_name", "city_name", "country_name", "timezone"]])

    st.subheader("Complexes")
    st.dataframe(complex_data)

# Tab 4: Country View
with tab4:
    st.subheader("Total Points by Country")
    country_points = rank_data.groupby('country')['points'].sum().reset_index().sort_values(by='points', ascending=False).head(15)
    fig1 = px.bar(country_points, x='points', y='country', orientation='h',
                  title="Top Countries by Points", color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Competitor Count by Country")
    country_count = rank_data['country'].value_counts().reset_index()
    country_count.columns = ['country', 'competitor_count']
    fig2 = px.bar(country_count.head(15), x='competitor_count', y='country', orientation='h',
                  title="Competitors per Country", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig2, use_container_width=True)

# Tab 5: Charts & Trends
with tab5:
    st.subheader("Competition Type Distribution")
    type_dist = comp_data['type'].value_counts().reset_index()
    type_dist.columns = ['type', 'count']
    fig3 = px.pie(type_dist, values='count', names='type', title="Competition Types",
                  color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Gender Distribution in Competitions")
    gender_dist = comp_data['gender'].value_counts().reset_index()
    gender_dist.columns = ['gender', 'count']
    fig4 = px.pie(gender_dist, values='count', names='gender', title="Gender Breakdown",
                  color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Rank Movement Summary")
    rank_move = rank_data['movement'].value_counts().reset_index()
    rank_move.columns = ['movement', 'count']
    fig5 = px.bar(rank_move, x='movement', y='count', title="Rank Movement Overview",
                  color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(fig5, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<center><b>Created by Veerendra Kashyap | Powered by Streamlit + MySQL + Python</b></center>", unsafe_allow_html=True)
