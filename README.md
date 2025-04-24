India Crime Insights: A Data-Driven Dashboard
Overview
India Crime Insights is an interactive dashboard that provides insights into crime data across India. The dashboard includes visualizations of crime trends, distributions, and key metrics. Users can filter data by year, state/UT, and crime type for in-depth analysis.

Features
Dynamic filters for year, state/UT, and crime type.

Visualizations like line charts, bar charts, pie charts, and maps.

Insights into crime trends, locations, and demographics.

Technologies Used
Python

Streamlit

Plotly

Pandas

Setup
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/india-crime-insights.git
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Run the app:

bash
Copy
Edit
streamlit run app.py
Data Pipeline
The data pipeline processes and cleans raw crime data, generating insights and preparing the data for visualizations.

Folder Structure
bash
Copy
Edit
/India Crime Insights
├── data/
│   ├── raw/                  # Raw data
│   ├── processed/            # Cleaned data
├── app.py                    # Streamlit app
├── pipeline.py               # Data pipeline
└── README.md                 # This file
