import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Wireless Zone Sales Dashboard", layout="wide")

st.title("📊 Wireless Zone Sales Dashboard")
st.markdown("Upload your sales export from **RQ4 or Verizon** to get started.")

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload Sales Data (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Data loaded successfully!")

    # Preprocess data (example column names, adjust as needed)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Sales Rep"] = df["Sales Rep"].astype(str)

    # KPI Cards
    total_activations = df["Activations"].sum()
    total_upgrades = df["Upgrades"].sum()
    total_accessories = df["Accessories"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("📱 Activations", total_activations)
    col2.metric("🔄 Upgrades", total_upgrades)
    col3.metric("🎧 Accessories", total_accessories)

    # Leaderboard
    st.subheader("🏆 Sales Leaderboard")
    leaderboard = df.groupby("Sales Rep")[["Activations", "Upgrades", "Accessories"]].sum().reset_index()
    leaderboard["Total"] = leaderboard[["Activations", "Upgrades", "Accessories"]].sum(axis=1)
    leaderboard = leaderboard.sort_values("Total", ascending=False)

    st.dataframe(leaderboard, use_container_width=True)

    # Trend Chart
    st.subheader("📈 Sales Trend Over Time")
    trend_data = df.groupby("Date")[["Activations", "Upgrades", "Accessories"]].sum().reset_index()
    chart = alt.Chart(trend_data).mark_line().encode(
        x="Date:T",
        y=alt.Y("Activations", title="Sales Count"),
        tooltip=["Date", "Activations", "Upgrades", "Accessories"]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("⬅️ Upload a file to get started.")

