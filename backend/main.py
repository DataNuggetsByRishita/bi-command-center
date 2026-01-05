from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from pydantic import BaseModel
from typing import List


app = FastAPI(title="BI Command Center API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class KPIResponse(BaseModel):
    total_sales: float
    total_profit: float
    total_orders: int


class RegionSales(BaseModel):
    region: str
    sales: float


class ProductSales(BaseModel):
    product: str
    sales: float


class TimeSales(BaseModel):
    date: str
    sales: float


def load_sales_csv() -> pd.DataFrame:
    try:
        return pd.read_csv("data/sales.csv")
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="❌ data/sales.csv not found.")


def load_and_prepare_data(region: str = "ALL", days: int = 0) -> pd.DataFrame:
    df = load_sales_csv()

    required_cols = {"date", "region", "quantity", "price", "cost", "order_id", "product"}
    missing = required_cols - set(df.columns)
    if missing:
        raise HTTPException(status_code=500, detail=f"❌ Missing columns: {list(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])

    df["region"] = df["region"].astype(str).str.upper().str.strip()

    df["sales"] = df["quantity"] * df["price"]
    df["cost_total"] = df["quantity"] * df["cost"]

    region = str(region).upper().strip()

    if region != "ALL":
        df = df[df["region"] == region]

    if days and days > 0 and not df.empty:
        cutoff = df["date"].max() - pd.Timedelta(days=days)
        df = df[df["date"] >= cutoff]

    return df


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/kpis", response_model=KPIResponse)
def get_kpis(region: str = "ALL", days: int = 0):
    df = load_and_prepare_data(region=region, days=days)

    if df.empty:
        return KPIResponse(total_sales=0.0, total_profit=0.0, total_orders=0)

    total_sales = float(df["sales"].sum())
    total_profit = float((df["sales"] - df["cost_total"]).sum())
    total_orders = int(df["order_id"].nunique())

    return KPIResponse(total_sales=total_sales, total_profit=total_profit, total_orders=total_orders)


@app.get("/sales_by_region", response_model=List[RegionSales])
def sales_by_region(days: int = 0, region: str = "ALL"):
    # ✅ NOW region filter works (if VIC selected, only VIC will show)
    df = load_and_prepare_data(region=region, days=days)

    if df.empty:
        return []

    result = (
        df.groupby("region", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    return result.to_dict(orient="records")


@app.get("/sales_by_product", response_model=List[ProductSales])
def sales_by_product(region: str = "ALL", days: int = 0):
    df = load_and_prepare_data(region=region, days=days)

    if df.empty:
        return []

    result = (
        df.groupby("product", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )
    return result.to_dict(orient="records")


@app.get("/sales_over_time", response_model=List[TimeSales])
def sales_over_time(days: int = 0, region: str = "ALL"):
    df = load_and_prepare_data(region=region, days=days)

    if df.empty:
        return []

    result = (
        df.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    result["date"] = result["date"].dt.strftime("%Y-%m-%d")
    return result.to_dict(orient="records")
