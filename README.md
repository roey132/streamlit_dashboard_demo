# 🌍 Earthquake Data Dashboard (AWS Athena + Streamlit)

This project demonstrates a modern, low-cost, serverless data pipeline and dashboard for global earthquake monitoring. It fetches live earthquake data daily via API, stores it in AWS S3, and visualizes it using Streamlit powered by Athena queries.

> ✅ Ideal for showcasing cloud data workflows, Athena querying, and Streamlit dashboards with live filters and insights.

---

## 🧰 Tech Stack

- **AWS S3** – stores daily ingested earthquake data as raw files
- **AWS Athena** – serverless SQL engine to query data directly from S3
- **Python + Pandas** – handles data transformation and analysis
- **Streamlit** – builds the interactive dashboard interface
- **GitHub** – version control and deployment source

---

## 🎯 Key Features

- ⚡ **Live interactive dashboard**
- 📅 Filter by date and magnitude range
- 🌊 Highlight tsunami-related events
- 📊 Visual insights: daily trends, severity breakdown, map view
- 📥 Download filtered dataset as CSV
- ✅ Smart Athena query reuse (no redundant executions within 2 hours)
- 💸 Minimal cost (serverless, cache-aware)

---

## 📸 Preview

![dashboard-preview](assets/dashboard-screenshot.png)

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/earthquake-dashboard.git
cd earthquake-dashboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set AWS credentials (one-time)

Make sure these are available as environment variables or via aws configure.

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=eu-central-1
```

### 5. Run the app
```bash
streamlit run streamlit_app.py
```

### 🧠 Insights Engine

The dashboard answers questions like:

    Where and when did earthquakes occur?

    Which areas had significant magnitudes recently?

    How often do tsunami threats occur?

    What’s the day-by-day trend in seismic activity?

All without re-querying AWS unless needed.

📁 Folder Structure
```bash
.
├── app/
│   ├── data_loader.py        # Athena/S3 logic
│   ├── dashboard.py          # Streamlit UI and filters
│   ├── athena_query.sql      # Reusable SQL for Athena
├── streamlit_app.py          # Main app entry point
├── requirements.txt
├── .streamlit/config.toml    # Theme customization
├── README.md
```

📬 Contact

Created by Roey Aharonov.
