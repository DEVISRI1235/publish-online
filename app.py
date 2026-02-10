import streamlit as st
import snowflake.connector
import pandas as pd

from snowflake.snowpark.context import get_active_session

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Enterprise Analytics Dashboard",
    layout="wide"
)

st.title("📊 Enterprise Analytics Dashboard")
st.caption("Bronze → Silver → Gold Architecture | Snowflake Native Streamlit")

# -------------------------------------------------
# Snowflake Session
# -------------------------------------------------
session = get_active_session()

# ---------------------------a----------------------
# Executive Summary (KPIs)
# -------------------------------------------------
st.header("📌 Executive Summary")

exec_df = session.sql(
    "SELECT * FROM GOLD.VW_EXEC_SUMMARY"
).to_pandas()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Orders", int(exec_df["TOTAL_ORDERS"][0]))
col2.metric("Total Revenue", f"${exec_df['TOTAL_REVENUE'][0]:,.2f}")
col3.metric("Avg Order Value", f"${exec_df['AVG_ORDER_VALUE'][0]:,.2f}")
col4.metric("Total Customers", int(exec_df["TOTAL_CUSTOMERS"][0]))
col5.metric("Total Products", int(exec_df["TOTAL_PRODUCTS"][0]))

st.divider()

# -------------------------------------------------
# Revenue by Region
# -------------------------------------------------
st.header("🌍 Revenue by Region")

region_df = session.sql(
    "SELECT * FROM GOLD.VW_REVENUE_BY_REGION"
).to_pandas()

st.bar_chart(
    region_df,
    x="REGION",
    y="TOTAL_REVENUE"
)

st.dataframe(region_df, use_container_width=True)

st.divider()

# -------------------------------------------------
# Revenue by Product Category
# -------------------------------------------------
st.header("🛒 Revenue by Product Category")

category_df = session.sql(
    "SELECT * FROM GOLD.VW_REVENUE_BY_CATEGORY"
).to_pandas()

st.bar_chart(
    category_df,
    x="CATEGORY",
    y="TOTAL_REVENUE"
)

st.dataframe(category_df, use_container_width=True)

st.divider()

# -------------------------------------------------
# Top 5 Customers
# -------------------------------------------------
st.header("🏆 Top 5 Customers by Revenue")

customer_df = session.sql(
    "SELECT * FROM GOLD.VW_TOP_CUSTOMERS"
).to_pandas()

st.bar_chart(
    customer_df,
    x="NAME",
    y="TOTAL_REVENUE"
)

st.dataframe(customer_df, use_container_width=True)

st.divider()

# -------------------------------------------------
# Monthly Revenue Trend
# -------------------------------------------------
st.header("📈 Monthly Revenue Trend")

monthly_df = session.sql(
    "SELECT * FROM GOLD.VW_MONTHLY_TREND"
).to_pandas()

st.line_chart(
    monthly_df,
    x="MONTH",
    y="TOTAL_REVENUE"
)

st.dataframe(monthly_df, use_container_width=True)

st.divider()

# -------------------------------------------------
# Revenue Growth %
# -------------------------------------------------
st.header("📊 Month-over-Month Revenue Growth")

growth_df = session.sql(
    "SELECT * FROM GOLD.VW_MONTHLY_REVENUE_GROWTH"
).to_pandas()

st.line_chart(
    growth_df,
    x="MONTH",
    y="GROWTH_PERCENT"
)

st.dataframe(growth_df, use_container_width=True)
