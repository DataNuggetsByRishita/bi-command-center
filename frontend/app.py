import streamlit as st
import requests
import pandas as pd
import plotly.express as px

from styles import set_video_background, card_open, card_close

BASE_URL = "http://127.0.0.1:8000"

# ✅ MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="BI Command Center", page_icon="📊", layout="wide")


@st.cache_data(ttl=30, show_spinner=False)
def api_get(endpoint: str, params: dict | None = None):
    url = f"{BASE_URL}{endpoint}"
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")
region_choice = st.sidebar.selectbox("Region", ["ALL", "NSW", "QLD", "VIC"])
date_range = st.sidebar.selectbox("Date Range", ["ALL", "Last 7 days", "Last 30 days"])

days_map = {"ALL": 0, "Last 7 days": 7, "Last 30 days": 30}
days = days_map[date_range]


# -----------------------------
# Title + navigation
# -----------------------------
st.title("BI Command Center")

page = st.radio(
    "Navigate",
    ["Overview", "Region", "Trends"],
    horizontal=True,
    label_visibility="collapsed",
)

# ✅ Background video by page
if page == "Overview":
    set_video_background("overview.mp4", overlay_opacity=0.65)
else:
    set_video_background("other_tabs.mp4", overlay_opacity=0.65)


# -----------------------------
# Health check
# -----------------------------
card_open()
try:
    st.write("Checking backend status...")
    health = api_get("/health")
    st.success(f"Backend status: {health['status']}")
except Exception:
    st.error("Backend not reachable. Start it with:\nuvicorn backend.main:app --reload")
    st.stop()
finally:
    card_close()


# -----------------------------
# PAGE 1: Overview
# -----------------------------
if page == "Overview":
    card_open()
    try:
        st.subheader("Business KPIs")

        kpis = api_get("/kpis", params={"region": region_choice, "days": days})

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"${kpis['total_sales']:.2f}")
        col2.metric("Total Profit", f"${kpis['total_profit']:.2f}")
        col3.metric("Total Orders", kpis["total_orders"])
    finally:
        card_close()


# -----------------------------
# PAGE 2: Region
# -----------------------------
elif page == "Region":

    # ✅ Sales by Region (NOW FILTERS WORK)
    card_open()
    try:
        st.subheader("Sales by Region")

        region_data = api_get(
            "/sales_by_region",
            params={"days": days, "region": region_choice}  # ✅ region filter applied
        )

        df_region = pd.DataFrame(region_data)

        if df_region.empty:
            st.warning("No data for selected filters.")
        else:
            fig = px.bar(df_region, x="region", y="sales", text="sales")
            fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
            fig.update_layout(
                height=420,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
            )
            st.plotly_chart(fig, use_container_width=True)
    finally:
        card_close()

    # ✅ Sales by Product (uses region + days)
    card_open()
    try:
        st.subheader("Sales by Product (Filter by Region)")

        prod_data = api_get(
            "/sales_by_product",
            params={"region": region_choice, "days": days}
        )
        df_prod = pd.DataFrame(prod_data)

        if df_prod.empty:
            st.warning("No product data for selected filters.")
        else:
            fig = px.bar(df_prod, x="product", y="sales", text="sales")
            fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
            fig.update_layout(
                height=420,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
            )
            st.plotly_chart(fig, use_container_width=True)
    finally:
        card_close()


# -----------------------------
# PAGE 3: Trends
# -----------------------------
else:
    card_open()
    try:
        st.subheader("Sales Over Time")

        time_data = api_get(
            "/sales_over_time",
            params={"days": days, "region": region_choice}
        )
        df_time = pd.DataFrame(time_data)

        if df_time.empty:
            st.warning("No trend data for selected filters.")
        else:
            df_time["date"] = pd.to_datetime(df_time["date"])
            fig = px.line(df_time, x="date", y="sales")
            fig.update_layout(
                height=420,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
            )
            st.plotly_chart(fig, use_container_width=True)
    finally:
        card_close()
