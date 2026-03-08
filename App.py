import streamlit as st
import pandas as pd
import tempfile
import os
import matplotlib.pyplot as plt
from datetime import datetime
from src.analytics import load_data2 as load_data_table
from src.plotting import price_history_figure, multi_stock_history_figure, volatility_figure, portfolio_value_figure, profit_loss_figure
from src.data_loader import is_valid_ticker
#https://portfolio-program.streamlit.app/


# --- AUTHENTICATION ---
def login():
    st.title("Login")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        # FALLBACK: Allow "admin" password even if secrets.toml is missing
        if pwd == st.secrets.get("PASSWORD", "admin"):
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Access Denied: Invalid Password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False 

if not st.session_state["logged_in"]:
    login()
    st.stop()

# --- MAIN DASHBOARD ---
st.title("Investment Portfolio Analytics")
st.write("Welcome to the Portfolio Manager. Track your equity holdings with live market data.")

# --- DATA INPUT SECTION ---
use_editor = st.toggle("Enable Manual Table Entry", value=False)

if "table" not in st.session_state:
    st.session_state.table = None

if use_editor:
    st.subheader("Inventory Management")
    # Initialize empty dataframe for the data editor
    initial_data = pd.DataFrame({
        "ticker": pd.Series(dtype="string"), 
        "datetime": pd.Series(dtype="datetime64[ns]"), 
        "quantity": pd.Series(dtype="int"),
    })
    
    editor_df = st.data_editor(
        initial_data,
        column_config={
            "ticker": st.column_config.TextColumn("Ticker Symbol", help="e.g. AAPL, TSLA"),
            "datetime": st.column_config.DateColumn("Acquisition Date"),
            "quantity": st.column_config.NumberColumn("Shares Owned", min_value=1),
        },
        num_rows="dynamic",
        use_container_width=True,
        key="positions_editor_v6",
    )
    
    col_update, col_save = st.columns(2)
    
    if col_update.button("Update Portfolio View"):
        if editor_df.empty or editor_df.dropna().empty:
            st.warning("Please enter at least one valid stock position.")
        else:
            invalid_tickers = [t for t in editor_df["ticker"].dropna() if not is_valid_ticker(t)]
            if invalid_tickers:
                st.error(f"Invalid Tickers Detected: {', '.join(invalid_tickers)}. Please check symbols.")
            else:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                        tmp.write(editor_df.to_csv(index=False).encode("utf-8"))
                        path = tmp.name
                    st.session_state.table = load_data_table(path)
                    st.rerun()
                except Exception as e:
                    st.error(f"Computation Error: {str(e)}")

    if col_save.button("Save Entry to Local Disk"):
         os.makedirs("config", exist_ok=True)
         editor_df.to_csv("config/positions.csv", index=False)
         st.success("Successfully saved to config/positions.csv")

else:
    st.subheader("Batch File Upload")
    uploaded = st.file_uploader("Select CSV Portfolio File", type=["csv"], key="csv_loader_main")

    if uploaded is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded.getvalue())
            path = tmp.name
        
        # Load and check for changes to prevent recursive loop
        new_table = load_data_table(path)
        if st.session_state.table is None or not new_table.equals(st.session_state.table):
            st.session_state.table = new_table
            st.rerun()

# --- ANALYTICS DISPLAY SECTION ---
table = st.session_state.table

if table is None or table.empty:
    st.info("Awaiting data input... Populate the table or upload a CSV to begin analysis.")
    st.stop()

st.subheader("Performance Inventory")
# Display the processed data excluding the raw date for a cleaner look
st.dataframe(table.drop(columns=["Purchase Date"]), use_container_width=True)

# Portfolio Aggregates calculation
prof = table['Profit ($)'].sum()
cost = table['Total Cost ($)'].sum()
ret = (prof / cost * 100) if cost != 0 else 0.0

portfolio_age = (datetime.now() - pd.to_datetime(table["Purchase Date"]).min()).days

st.subheader("Executive Summary")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Unrealized P/L", f"${prof:,.2f}", delta=f"{ret:.2f}%")
m2.metric("Total Invested Capital", f"${cost:,.2f}")
m3.metric("Portfolio Growth", f"{ret:.2f}%")
m4.metric("Portfolio Age", f"{portfolio_age} days")

st.download_button(
    label="Export Portfolio Report (CSV)",
    data=table.to_csv(index=False).encode("utf-8"),
    file_name=f"portfolio_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)

# --- VISUALIZATION SECTION ---
st.subheader("Market Visualization")
ticker_choice = st.selectbox("Analyze Individual Asset", sorted(table["Stock Ticker"].unique()))

# Locate selection data for charting
sel_row = table[table["Stock Ticker"] == ticker_choice].iloc[0]
sel_date = sel_row["Purchase Date"]

tab_single, tab_vol, tab_pv, tab_pl, tab_multi, tab_alloc = st.tabs([
    "Asset History", "Volatility", "Portfolio Value", "P&L", "Comparison View", "Capital Allocation"
])

with tab_single:
    st.pyplot(price_history_figure(ticker_choice, sel_date))
    with st.popover("ℹ️ 20-day SMA"):
        st.markdown("**20-day Simple Moving Average**\n\nThe 20-day SMA plots the average closing price of the preceding 20 trading days at each point. It begins after the first 20 trading days and smooths out short-term price fluctuations to reveal the underlying trend.")

with tab_vol:
    st.pyplot(volatility_figure(ticker_choice, sel_date))
    with st.popover("ℹ️ Volatility"):
        st.markdown("**20-Day Rolling Volatility**\n\nShows how much the stock's daily price moves have varied over the last 20 trading days. A higher value means bigger swings and more risk. Spikes indicate periods of uncertainty or major news events.")

with tab_pv:
    st.pyplot(portfolio_value_figure(table))
    with st.popover("ℹ️ Portfolio Value"):
        st.markdown("**Portfolio Total Value Over Time**\n\n**Green line** — combined market value of all holdings each day.\n\n**Grey dashed line** — total amount you invested (cost basis). It only steps up when a new stock is purchased, and stays flat otherwise.\n\nThe gap between the two lines shows how much of the growth comes from price changes, not new purchases.")

with tab_pl:
    st.pyplot(profit_loss_figure(table))
    with st.popover("ℹ️ P&L"):
        st.markdown("**Unrealised Profit / Loss**\n\nShows how much each stock has gained (green) or lost (red) since purchase, in dollars. Values are unrealised — they only become real when you sell.")

with tab_multi:
    st.pyplot(multi_stock_history_figure(table))

with tab_alloc:
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(table["Total Cost ($)"], labels=table["Stock Ticker"], autopct="%1.1f%%", startangle=140)
    st.pyplot(fig_pie)