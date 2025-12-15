#  TMDB Movie Data Orchestration Pipeline

## Project Overview
This project converts a Jupyter Notebook into a **data orchestration pipeline** that extracts movie data from the **TMDB API**, cleans and transforms the data, performs analysis and advanced queries, and generates visualisations.

The notebook acts as the **orchestrator**, while individual Python scripts handle each stage of the pipeline.

---

## Project Structure
tmdb_pipeline/
│
├── notebooks/
│ └── orchestrator.ipynb
│
├── scripts/
<<<<<<< HEAD
│ ├── extract.py # Fetches movie data from TMDB API
│ ├── clean.py # Cleans and transforms raw data
│ ├── analysis.py # KPI calculations and metrics
│ ├── queries.py # Advanced filtering and search logic
│ └── visualize.py # Data visualisation functions
=======
│   ├── extract.py        # Fetches movie data from TMDB API 
│   ├── clean.py          # Cleans and transforms raw data 
│   ├── analysis.py       # KPI calculations and metrics
│   ├── queries.py        # Advanced filtering and search logic
│   └── visualize.py     # Data visualisation functions
>>>>>>> dcab6cd849b838205c57842d7f0233c2fd65f3b4
│
├── config.py # API keys, constants, movie IDs
├── requirements.txt # Project dependencies
└── README.md

##  Orchestration Design
- **Scripts** perform individual tasks (extract, clean, analyze, visualize)
- **Notebook** controls execution order
- Each script is reusable and testable

This follows **industry-standard orchestration principles**.

---

##  Pipeline Stages

### 1️ Data Extraction (`extract.py`)
- Connects to the TMDB API
- Fetches movie details and credits
- Saves raw JSON data
- Returns a Pandas DataFrame

---

### 2️ Data Cleaning & Feature Engineering (`clean.py`)
- Drops irrelevant columns
- Extracts nested JSON fields
- Handles missing and invalid values
- Converts budget and revenue to USD millions
- Produces a clean DataFrame

---

### 3️ KPI & Metrics (`analysis.py`)
- Calculates:
  - Profit (Revenue − Budget)
  - ROI (Revenue / Budget)
- Provides reusable ranking functions

---

### 4️ Advanced Queries (`queries.py`)
- Actor-based searches
- Genre-based filtering
- Director-based queries
- Easily extendable

---

### 5️ Data Visualisation (`visualize.py`)
- Revenue vs Budget
- ROI by genre
- Popularity vs rating
- Franchise vs standalone comparison

---

##  Orchestrator Notebook Example
```python
from scripts.extract import run as extract
from scripts.clean import run as clean
from scripts.analysis import add_kpis
from scripts.visualize import revenue_vs_budget

df_raw = extract()
df_clean = clean(df_raw)
df_final = add_kpis(df_clean)

revenue_vs_budget(df_final)


Installation
1️ Clone the repository
git clone <your-repo-url>
cd tmdb_pipeline

2️ Install dependencies
pip install -r requirements.txt

 Configuration

Update your TMDB API key and constants in config.py:

API_KEY = "YOUR_TMDB_API_KEY"

 Why This Design

✔ Clean separation of concerns
✔ Easy debugging and testing
✔ Notebook can be replaced with Airflow or Prefect
✔ Scales well for real-world data pipelines

 Technologies Used

Python

Pandas

NumPy

Requests

Matplotlib

Seaborn

Jupyter Notebook