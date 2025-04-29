
🇮🇳 India Crime Insights: A Data-Driven Dashboard

📊 Overview
India Crime Insights is an interactive and user-friendly dashboard designed to explore and analyze crime data across India. With dynamic filters and visualizations, users can investigate crime trends, hotspots, and statistics by year, state/UT, and crime type.

🔍 Key Features
- ✅ Dynamic filters for Year, State/UT, and Crime Type
- 📈 Multiple visualizations: Line charts, Bar charts, Pie charts, and Geographic maps
- 📌 Interactive insights into crime trends, affected locations, and demographic patterns

🛠️ Technologies Used
- 🐍 Python
- 📊 Streamlit
- 📈 Plotly
- 🐼 Pandas

⚙️ Setup Instructions

1. Clone the repository
git clone https://github.com/Varunkaushik2004/India-Crime-Insights-A-Data-Driven-Dashboard.git

2. Install required packages
pip install -r requirements.txt

3. Run the Streamlit app
streamlit run app.py

🔄 Data Pipeline
The project includes a data pipeline that:
- Cleans and transforms raw crime data
- Handles missing values and parses dates
- Derives new insights (e.g., year, month, day of the week, closure time)
- Outputs processed data for visualization

📁 Project Structure
India-Crime-Insights-A-Data-Driven-Dashboard/
│
├── data/
│   ├── raw/                 # Contains raw crime datasets
│   └── processed/           # Cleaned and preprocessed data
│
├── app.py                   # Streamlit dashboard application
├── pipeline.py              # Data processing pipeline script
└── README.md                # Project documentation (this file)

🚀 Explore the Crime Landscape Across India – One Insight at a Time!
