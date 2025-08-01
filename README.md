# Tennis Game Analytics – SportRadar API Integration

An end-to-end data analytics project that extracts, stores, and visualizes tennis data using the SportRadar API. This project is built using Python, SQL, and Streamlit, and enables users to explore competition hierarchies, venue details, and player rankings in doubles tennis.

## Project Overview

This project focuses on:

* Collecting real-time tennis data from SportRadar API
* Structuring it into a relational SQL database
* Performing SQL analysis
* Presenting interactive visualizations via a Streamlit web app

It supports analysis of:

* Tournaments and competitions
* Sports complexes and venues
* Player rankings in doubles events

## Objectives

* Build a pipeline to extract tennis data via API
* Design and normalize a SQL database schema
* Execute complex SQL queries to derive insights
* Build an interactive Streamlit dashboard for exploration and filtering
* Enhance skills in API integration, data wrangling, SQL, and app development

## Features

* View all tournaments grouped by categories
* Filter competitions by type (e.g., singles/doubles), gender, or category
* Explore venues by country and timezone
* Analyze player rankings and performance in doubles events
* Visual dashboards and KPI summaries in Streamlit

## Datasets and APIs Used

| Source         | Endpoint                     | Data Collected              |
| -------------- | ---------------------------- | --------------------------- |
| SportRadar API | /competitions                | Categories and Competitions |
| SportRadar API | /complexes                   | Complexes and Venues        |
| SportRadar API | /doubles-competitor-rankings | Competitors and Rankings    |

## Tech Stack

* Languages: Python, SQL
* Libraries: requests, pandas, mysql.connector, streamlit, plotly, matplotlib
* Database: MySQL
* App: Streamlit
* Tools: Jupyter Notebook, Git, GitHub

## Project Structure

```
tennis-game-analytics/
|
├── app.py                        # Streamlit application
├── Tennis_Game_Analytics.ipynb  # Notebook for API extraction and preprocessing
├── tennis_SQL.sql               # SQL schema and queries
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
├── assets/                      # Screenshots or visuals (optional)
└── data/                        # API sample data or exports (optional)
```

## SQL Database Schema

Tables created and normalized:

1. Categories – Stores tournament categories
2. Competitions – Tournament-level details
3. Complexes – Sporting complexes
4. Venues – Linked to complexes
5. Competitors – Players
6. Competitor\_Rankings – Weekly rankings for doubles

All foreign keys and primary keys implemented

## SQL Insights Extracted

Sample queries implemented:

* List all competitions with their category
* Find all “doubles” competitions
* Count venues per complex
* Filter competitors with rank movement = 0
* Country-wise competitor stats and leaderboards

See `tennis_SQL.sql` for the full query list.

## Streamlit Dashboard

Key dashboard features:

* Homepage KPIs: Total competitors, highest-ranked player, total venues
* Filters: Rank range, country, competition type
* Player Viewer: Detailed view by selected player
* Country-wise summaries: Total competitors, average points
* Leaderboards: Top ranked and top scoring players


## How to Run the Project

1. Clone the repository

   ```
   git clone https://github.com/YOUR_USERNAME/tennis-game-analytics.git
   cd tennis-game-analytics
   ```

2. Install dependencies

   ```
   pip install -r requirements.txt
   ```

3. Set up your MySQL database using `tennis_SQL.sql`

4. Run the Streamlit app

   ```
   streamlit run Tennis_Streamlit_dashboard.py
   ```

## Future Enhancements

* Add more APIs (e.g., match-level stats)
* Add time-based trend analysis (e.g., ranking movement over time)
* Implement caching or pagination for performance
* Enhance UI with more visuals (bar, pie, map)

## License

This project is for educational and portfolio purposes. Data is fetched using public API keys from SportRadar.

## Acknowledgments

* SportRadar API
* Streamlit Docs
* Guided project inspiration from internship capstone requirements

