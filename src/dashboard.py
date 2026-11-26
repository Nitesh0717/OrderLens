import streamlit as st
import pandas as pd
import plotly.express as px
from db import engine

st.set_page_config(page_title="OrderLens", layout="wide")
st.title("OrderLens | Retail Analytics Dashboard")
st.caption("Data Warehouse Analytics")

@st.cache_data
def load_data():
    orders = pd.read_sql("SELECT * FROM fact_orders", engine)
    products = pd.read_sql("SELECT * FROM dim_products", engine)
    customers = pd.read_sql("SELECT * FROM dim_customers", engine)
    return orders, products, customers

orders, products, customers = load_data()

orders["order_date"] = pd.to_datetime(orders["order_date"])

total_revenue = orders["total_amount"].sum()
total_orders = len(orders)
avg_order = orders["total_amount"].mean()
total_customers = orders["customer_id"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"{total_revenue:,.2f}")
c2.metric("Total Orders", f"{total_orders:,}")
c3.metric("Average Order Value", f"{avg_order:,.2f}")
c4.metric("Customers", f"{total_customers:,}")

st.divider()

monthly = orders.groupby(orders["order_date"].dt.to_period("M"))["total_amount"].sum().reset_index()
monthly["Month"] = monthly["order_date"].astype(str)

fig1 = px.line(monthly, x="Month", y="total_amount", markers=True, title="Monthly Revenue Trend")
st.plotly_chart(fig1, use_container_width=True)

category = orders.merge(products, on="product_id")
category_revenue = category.groupby("category")["total_amount"].sum().reset_index()

col1, col2 = st.columns(2)

with col1:
    fig2 = px.bar(category_revenue, x="category", y="total_amount", title="Revenue by Category")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    city_data = orders.merge(customers, on="customer_id")
    city_revenue = city_data.groupby("city")["total_amount"].sum().reset_index()
    fig3 = px.bar(city_revenue, x="city", y="total_amount", title="Revenue by City")
    st.plotly_chart(fig3, use_container_width=True)

st.subheader("Top 10 Customers")
top_customers = (
    orders.merge(customers, on="customer_id")
    .groupby("customer_name")["total_amount"]
    .sum()
    .nlargest(10)
    .reset_index()
)
st.dataframe(top_customers, use_container_width=True)

st.subheader("Data Preview")
st.dataframe(orders.head(100), use_container_width=True)
