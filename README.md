# 📊 Superstore Sales Analysis Pipeline

This project is a complete Data Engineering pipeline designed to analyze sales data from the Kaggle Superstore dataset. It covers the full lifecycle of data: from raw ingestion and transformation to storage in a cloud data warehouse (Snowflake) and final visualization.

## 🚀 Project Overview

The goal of this project is to provide insights into sales performance, customer segments, and regional trends. The pipeline automates the cleaning of raw CSV data, enriches it with time-based features, loads it into Snowflake for scalable querying, and presents the results through an interactive Streamlit dashboard.

## 🛠️ Tools & Technologies

*   **Data Source:** Kaggle Superstore Dataset (`train.csv`)
*   **Data Processing:** `Pandas` (Python)
*   **Data Warehouse:** `Snowflake`
*   **Visualization:** `Streamlit` & `Matplotlib`
*   **Language:** Python 3.x

## 📁 Project Structure

*   `train.csv`: The raw dataset containing ~9,800 rows of sales transactions.
*   `project.py`: The ETL (Extract, Transform, Load) script. It cleans the data and uploads it to Snowflake.
*   `dashboard.py`: The Streamlit application that builds the interactive dashboard.
*   `clean_data.csv`: (Generated) The processed and cleaned version of the data.

## ⚙️ Installation

1.  **Clone the repository** (or ensure all files are in the same directory).
2.  **Install the required Python libraries:**
    ```bash
    pip install pandas snowflake-connector-python streamlit matplotlib
    ```

## 🏃 How to Run

### Step 1: Data Processing & Loading
Run the `project.py` script to process the raw data and upload it to your Snowflake account.
```bash
python project.py
```
*Note: You will be prompted to enter your Snowflake credentials in the script.*

### Step 2: Launch the Dashboard
Once the data is processed, launch the visualization dashboard using Streamlit:
```bash
streamlit run dashboard.py
```

## 📊 Dashboard Features
*   **KPIs:** Total Sales, Order Count, Customer Count, and Average Shipping Days.
*   **Category Analysis:** Sales breakdown by product category (Furniture, Office Supplies, Technology).
*   **Regional Trends:** Pie chart showing sales distribution across regions.
*   **Monthly Performance:** Time-series chart showing sales trends over months/years.
*   **Segment Distribution:** Sales analysis based on customer segments (Consumer, Corporate, Home Office).
*   **Raw Data View:** A searchable table of the entire cleaned dataset.

---
*Created for Big Biological Data University Project.*
