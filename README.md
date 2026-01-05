# BI Command Center

BI Command Center is an end-to-end Business Intelligence dashboard built to demonstrate real-world data analytics workflows, from backend data processing to frontend dashboard visualization.

The project focuses on transforming raw sales data into meaningful business insights using clean APIs, interactive filters, and a modern dashboard interface.

---

## What This Project Does

The BI Command Center allows users to:
- View key business KPIs such as total sales, total profit, and total orders
- Filter data by region and date range
- Analyze sales performance by region
- Drill down into product-level sales
- Track sales trends over time using interactive charts

The goal of this project was to simulate how business intelligence dashboards are designed and used in real business environments.

---

## Tech Stack

Backend  
- FastAPI  
- Pandas  
- REST APIs  

Frontend  
- Streamlit  
- Plotly  

Data  
- CSV-based sales dataset  

---

## How the Project Works

The backend is built using FastAPI and is responsible for reading and processing sales data from a CSV file. It exposes multiple API endpoints that return aggregated business metrics such as KPIs, region-wise sales, product-wise sales, and time-based trends.

The frontend is built using Streamlit and consumes these APIs to display interactive charts and metrics. Filters selected on the frontend, such as region and date range, dynamically control how data is processed on the backend.

The dashboard interface is enhanced using custom CSS, glass-style UI components, and background visuals to improve readability and user experience.

---

## How to Run the Project Locally

Start the backend:

```bashh
cd backend
uvicorn main:app --reload


The backend will run at:

http://127.0.0.1:8000


Start the frontend:

cd frontend
streamlit run app.py


The frontend will run at:

http://localhost:8501

API Endpoints

GET /health

GET /kpis

GET /sales_by_region

GET /sales_by_product

GET /sales_over_time

Each endpoint supports filters such as region and date range.

What I Learned

Designing and building REST APIs using FastAPI

Performing real-world data filtering and aggregation using Pandas

Connecting frontend dashboards to backend APIs

Handling dynamic filters across frontend and backend

Building interactive visualizations using Plotly

Structuring a full-stack data analytics project

Improving UI using custom styling in Streamlit

Why I Built This Project

I built this project to strengthen my practical skills in data analytics and dashboard development. It reflects how data is processed, analyzed, and presented to support business decision-making.

This project is part of my ongoing effort to build one project every week and continuously improve my technical and analytical skills.

Author

Rishita
Data Nuggets