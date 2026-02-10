import streamlit as st
import snowflake.connector
import pandas as pd

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Enterprise Analytics Dashboard",
    layout="wide"
)

st.title("📊 Enterprise Analytics Dashboard")
st.caption("Bronze → Silver → Gold Architecture | Streamlit Cloud")

# -------------------------------------------------
# Snowflake Connection (Streamlit Cloud)
# -------------------------------------------------
conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database="ENTERPRISE_DB",
    schema="GOLD"
)

def load_df(query):
    return pd.read_sql(query, conn)

# -------------------------------------------------
# Executive Summary
# -------------------------------------------------
st.header("📌 Executive Summary")

exec_df = load_df("SELECT * FROM VW_EXEC_SUMMARY")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Orders", int(exec_df["TOTAL_ORDERS"][0]))
c2.metric("Total Revenue", f"${exec_df['TOTAL_REVENUE'][0]:,.2f}")
c3.metric("Avg Order Value", f"${exec_df['AVG_ORDER_VALUE'][0]:,.2f}")
c4.metric("Total Customers", int(exec_df["TOTAL_CUSTOMERS"][0]))
c5.metric("Total Products", int(exec_df["TOTAL_PRODUCTS"][0]))

# -------------------------------------------------
# Revenue by Region
# -------------------------------------------------
st.header("🌍 Revenue by Region")
region_df = load_df("SELECT * FROM VW_REVENUE_BY_REGION")
st.bar_chart(region_df, x="REGION", y="TOTAL_REVENUE")

# -------------------------------------------------
# Revenue by Category
# -------------------------------------------------
st.header("🛒 Revenue by Category")
cat_df = load_df("SELECT * FROM VW_REVENUE_BY_CATEGORY")
st.bar_chart(cat_df, x="CATEGORY", y="TOTAL_REVENUE")

# -------------------------------------------------
# Top Customers
# -------------------------------------------------
st.header("🏆 Top 5 Customers")
cust_df = load_df("SELECT * FROM VW_TOP_CUSTOMERS")
st.bar_chart(cust_df, x="NAME", y="TOTAL_REVENUE")

# -------------------------------------------------
# Monthly Trend
# -------------------------------------------------
st.header("📈 Monthly Revenue Trend")
month_df = load_df("SELECT * FROM VW_MONTHLY_TREND")
st.line_chart(month_df, x="MONTH", y="TOTAL_REVENUE")

# -------------------------------------------------
# Growth
# -------------------------------------------------
st.header("📊 Revenue Growth %")
growth_df = load_df("SELECT * FROM VW_MONTHLY_REVENUE_GROWTH")
st.line_chart(growth_df, x="MONTH", y="GROWTH_PERCENT")
