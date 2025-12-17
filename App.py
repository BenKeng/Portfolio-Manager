import streamlit as st
import pandas as pd
import tempfile
from src.analytics import load_data2 as load_data_table  
from src.plotting import price_history_figure  

st.title("Portfolio Manager")

uploaded = st.file_uploader("Upload positions.csv", type=["csv"])

if uploaded is None:
    st.info("Upload your positions.csv to begin.")
    st.stop()

with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
    tmp.write(uploaded.getvalue())
    positions_path = tmp.name

table = load_data_table(positions_path)
st.subheader("Overview")
st.dataframe(table, use_container_width=True)

if "profit($)" in table.columns:
    st.subheader("Summary")
    st.write(f"Total profit: {table['profit($)'].sum():,.2f}$")

st.subheader("Performance Graph")

ticker = st.selectbox(
    "Select stock",
    sorted(table["ticker"].unique())
)

row = table[table["ticker"] == ticker].iloc[0]
buy_date = row["datetime"]

fig = price_history_figure(ticker, buy_date)
st.pyplot(fig)

#streamlit run App.py