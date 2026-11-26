import streamlit as st
import pandas as pd
import plotly.express as px
from db import engine

st.set_page_config(
    page_title="OrderLens | Data Analytics",
    page_icon="📊",
    layout="wide"
)

# -------------------- THEME --------------------
px.defaults.template = "plotly_dark"

st.markdown("""
<style>
.stApp {
    background-color: #0e1117 !important;
    color: #f8fafc !important;
}

h1, h2, h3, h4, p, label {
    color: #f8fafc !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
}

/* Date inputs */
[data-testid="stSidebar"] [data-testid="stDateInput"] input {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    caret-color: #111827 !important;
    opacity: 1 !important;
}
[data-testid="stSidebar"] [data-testid="stDateInput"] button,
[data-testid="stSidebar"] [data-testid="stDateInput"] button svg {
    color: #111827 !important;
    fill: #111827 !important;
}



/* Metrics */
[data-testid="stMetric"] {
    background-color: #1f2937 !important;
    padding: 18px !important;
    border-radius: 12px !important;
    border: 1px solid #374151 !important;
}
[data-testid="stMetricLabel"] * {
    color: #cbd5e1 !important;
}
[data-testid="stMetricValue"] * {
    color: #ffffff !important;
}

/* Refresh and download buttons */
[data-testid="stSidebar"] .stButton button,
.stDownloadButton button {
    background-color: #2563eb !important;
    color: #ffffff !important;
    border: 1px solid #60a5fa !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stButton button * {
    color: #ffffff !important;
}

/* Chart headings and markdown */
[data-testid="stApp"] h1,
[data-testid="stApp"] h2,
[data-testid="stApp"] h3 {
    color: #f8fafc !important;
}

/* Dataframes */
[data-testid="stDataFrame"] {
    border: 1px solid #374151 !important;
}

/* Streamlit info boxes */
[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span {
    color: #111827 !important;
}

/* Consistent Plotly chart containers */
[data-testid="stPlotlyChart"] {
    background-color: #0e1117 !important;
}


/* Persistent sidebar collapse control */
[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarExpandButton"] {
    visibility: visible !important;
    opacity: 1 !important;
    display: flex !important;
    z-index: 999999 !important;
}

[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarExpandButton"] button {
    visibility: visible !important;
    opacity: 1 !important;
    display: flex !important;
    background: #2563eb !important;
    color: #ffffff !important;
    border: 2px solid #93c5fd !important;
    border-radius: 8px !important;
    min-width: 40px !important;
    width: 40px !important;
    min-height: 40px !important;
    height: 40px !important;
    box-shadow: 0 0 10px rgba(37, 99, 235, 0.6) !important;
}

[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarExpandButton"] svg {
    visibility: visible !important;
    opacity: 1 !important;
    color: #ffffff !important;
    fill: #ffffff !important;
    stroke: #ffffff !important;
}


</style>
""", unsafe_allow_html=True)



# -------------------- DATA LOADING --------------------
@st.cache_data(ttl=300)
def load_data():
    orders = pd.read_sql("SELECT * FROM fact_orders", engine)
    customers = pd.read_sql("SELECT * FROM dim_customers", engine)
    products = pd.read_sql("SELECT * FROM dim_products", engine)

    orders["order_date"] = pd.to_datetime(orders["order_date"])

    return orders, customers, products


try:
    orders, customers, products = load_data()
except Exception as e:
    st.error(f"Database connection or data loading failed: {e}")
    st.stop()

# -------------------- SIDEBAR --------------------
st.sidebar.title("📊 OrderLens")



page = st.sidebar.selectbox(
    "Navigation",
    ["Overview", "Sales Analytics", "Data Quality", "Data Explorer"]
)



if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    try:
        load_data.clear()
        orders, customers, products = load_data()
        st.sidebar.success("Data successfully refreshed!")
    except Exception as e:
        st.sidebar.error(f"Refresh failed: {e}")

# -------------------- FILTERS --------------------
min_date = orders["order_date"].min().date()
max_date = orders["order_date"].max().date()

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="start_date",
    format="DD/MM/YYYY"
)

end_date = st.sidebar.date_input(
    "End Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key="end_date",
    format="DD/MM/YYYY"
)

if start_date > end_date:
    st.sidebar.error("Start date must be before end date.")
    st.stop()

filtered = orders[
    (orders["order_date"].dt.date >= start_date)
    & (orders["order_date"].dt.date <= end_date)
].copy()

# -------------------- HEADER --------------------
st.title("📊 OrderLens")
st.caption("Retail Data Engineering & Business Analytics Platform")

# -------------------- OVERVIEW --------------------
if page == "Overview":

    st.subheader("Business Overview")

    total_revenue = filtered["total_amount"].sum()
    total_orders = len(filtered)
    avg_order_value = (
        total_revenue / total_orders if total_orders else 0
    )

    total_customers = filtered["customer_id"].nunique()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
    c2.metric("Total Orders", f"{total_orders:,}")
    c3.metric("Average Order Value", f"₹{avg_order_value:,.2f}")
    c4.metric("Customers", f"{total_customers:,}")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        revenue_by_category = filtered.merge(
            products[["product_id", "category"]],
            on="product_id",
            how="left"
        )

        category_sales = (
            revenue_by_category.groupby("category")["total_amount"]
            .sum()
            .reset_index()
            .sort_values("total_amount", ascending=False)
        )

        fig = px.bar(
            category_sales,
            x="category",
            y="total_amount",
            title="Revenue by Product Category",
            text_auto=".2s"
        )

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        daily_sales = (
            filtered.groupby(filtered["order_date"].dt.date)
            ["total_amount"]
            .sum()
            .reset_index()
        )

        daily_sales.columns = ["Date", "Revenue"]

        fig = px.line(
            daily_sales,
            x="Date",
            y="Revenue",
            markers=True,
            title="Revenue Trend"
        )

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    city_data = filtered.merge(
        customers[["customer_id", "city"]],
        on="customer_id",
        how="left"
    )

    city_sales = (
        city_data.groupby("city")["total_amount"]
        .sum()
        .reset_index()
        .sort_values("total_amount", ascending=False)
        .head(10)
    )

    fig = px.bar(
        city_sales,
        x="city",
        y="total_amount",
        title="Top 10 Cities by Revenue",
        text_auto=".2s"
    )

    fig.update_layout(template="plotly_dark", height=400)

    st.plotly_chart(fig, use_container_width=True)

# -------------------- SALES ANALYTICS --------------------
elif page == "Sales Analytics":

    st.subheader("Sales Analytics")

    total_revenue = filtered["total_amount"].sum()
    total_orders = len(filtered)

    c1, c2 = st.columns(2)

    c1.metric("Revenue", f"₹{total_revenue:,.0f}")
    c2.metric("Orders", f"{total_orders:,}")

    st.markdown("---")

    category_data = filtered.merge(
        products[["product_id", "category"]],
        on="product_id",
        how="left"
    )

    category_sales = (
        category_data.groupby("category")["total_amount"]
        .sum()
        .reset_index()
        .sort_values("total_amount", ascending=False)
    )

    fig = px.bar(
        category_sales,
        x="category",
        y="total_amount",
        title="Category Revenue Analysis",
        text_auto=".2s"
    )

    fig.update_layout(template="plotly_dark", height=400)

    st.plotly_chart(fig, use_container_width=True)

    monthly_sales = filtered.copy()
    monthly_sales["Month"] = monthly_sales["order_date"].dt.strftime("%Y-%m")
    monthly_sales = (
        monthly_sales.groupby("Month", as_index=False)["total_amount"]
        .sum()
        .sort_values("Month")
    )

    if not monthly_sales.empty:
        fig = px.line(
            monthly_sales,
            x="Month",
            y="total_amount",
            markers=True,
            title="Monthly Sales Analysis"
        )
        fig.update_layout(
            template="plotly_dark",
            height=450,
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            font_color="#f1f5f9",
            title_font_color="#f8fafc"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No sales data available for the selected date range.")

    city_data = filtered.merge(
        customers[["customer_id", "city"]],
        on="customer_id",
        how="left"
    )

    city_sales = (
        city_data.groupby("city")["total_amount"]
        .sum()
        .reset_index()
        .sort_values("total_amount", ascending=False)
    )

    fig = px.bar(
        city_sales.head(10),
        x="city",
        y="total_amount",
        title="Top Performing Cities"
    )

    fig.update_layout(template="plotly_dark", height=400)

    st.plotly_chart(fig, use_container_width=True)

# -------------------- DATA QUALITY --------------------
elif page == "Data Quality":

    st.subheader("Data Quality & Warehouse Health")

    total_source_rows = len(orders)
    total_product_rows = len(products)
    total_customer_rows = len(customers)

    c1, c2, c3 = st.columns(3)

    c1.metric("Fact Records", f"{total_source_rows:,}")
    c2.metric("Customer Records", f"{total_customer_rows:,}")
    c3.metric("Product Records", f"{total_product_rows:,}")

    st.markdown("---")

    quality_checks = []

    for table_name, df in [
        ("Fact Orders", orders),
        ("Customer Dimension", customers),
        ("Product Dimension", products)
    ]:

        missing = int(df.isnull().sum().sum())
        duplicates = int(df.duplicated().sum())

        quality_checks.append({
            "Dataset": table_name,
            "Rows": len(df),
            "Duplicate Rows": duplicates,
            "Missing Values": missing,
            "Status": "PASS" if missing == 0 and duplicates == 0 else "CHECK"
        })

    quality_df = pd.DataFrame(quality_checks)

    st.markdown("### Dataset Validation Summary")

    st.dataframe(
        quality_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Warehouse Architecture")
    st.markdown("**Data Pipeline**")
    st.write("Raw CSV Data → Python ETL → PostgreSQL Source Tables → Dimensional Warehouse → SQL Analytics → Dashboard")
    st.markdown("- **Fact table:** fact_orders")
    st.markdown("- **Dimension table:** dim_customers")
    st.markdown("- **Dimension table:** dim_products")
    st.markdown("- **ETL:** Python + Pandas")
    st.markdown("- **Warehouse:** PostgreSQL")
    st.markdown("- **Validation:** Automated tests + dataset checks")
    st.info("These are dashboard-level validation checks on the currently loaded warehouse datasets.")

# -------------------- DATA EXPLORER --------------------
elif page == "Data Explorer":

    st.subheader("Data Explorer")

    dataset_choice = st.selectbox(
        "Select Dataset",
        ["Orders", "Customers", "Products"]
    )

    if dataset_choice == "Orders":
        display_df = filtered

    elif dataset_choice == "Customers":
        display_df = customers

    else:
        display_df = products

    st.write(f"Records: {len(display_df):,}")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download CSV",
        data=csv_data,
        file_name=f"{dataset_choice.lower()}_data.csv",
        mime="text/csv"
    )

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("OrderLens | Data Engineering Project")
