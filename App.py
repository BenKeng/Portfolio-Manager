import streamlit as st
import pandas as pd
import tempfile
from src.analytics import load_data2 as load_data_table  
from src.plotting import price_history_figure 
#https://portfolio-program.streamlit.app/


# Login
def login():
    st.title("Login")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if pwd == st.secrets["PASSWORD"]:
            st.session_state["logged_in"] = True
        else:
            st.error("Wrong password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False 
#if the App were run again the session state would be saved as true
#resulting in an automatic login without the user needing to type in the password

if not st.session_state["logged_in"]:
    login()
    st.stop()
#if user doesn't login UI after login will never appear

# UI after login
st.title("Dashboard")
st.write("You are logged in!")
st.title("Portfolio Manager")

# Choose input method
use_editor = st.toggle("Create a csv file instead of uploading", value=True)
# true = table editor | false = upload file

table = None
if "table" not in st.session_state:
    st.session_state.table = None

# internal csv table
if use_editor:
    st.subheader("Enter stocks here")
    editor_df = st.data_editor(
        pd.DataFrame({
            "ticker": pd.Series(dtype="string"), 
            "date:   (yyyy-mm-dd)": pd.Series(dtype="string"), 
            "quantity": pd.Series(dtype="int"),
        }),
        num_rows="dynamic",
        use_container_width=True,
        key="positions_editor_v4",
    )
    update_clicked = st.button("Update portfolio")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(editor_df.to_csv(index=False).encode("utf-8"))
        positions_path = tmp.name

    if update_clicked:
        try:
            st.session_state.table = load_data_table(positions_path)
        except ValueError as e:
            st.error(str(e))
            st.stop()
        except Exception:
            st.error("Invalid input. Check ticker, date, and quantity.")
            st.stop()
# upload csv file
else:
    uploaded = st.file_uploader("Upload csv file", type=["csv"], key="csv_upload")

    if uploaded is None:
        st.info("Upload your csv file to begin.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded.getvalue())
        positions_path = tmp.name

    st.session_state.table = load_data_table(positions_path)
    table = st.session_state.table
    
table = st.session_state.table if use_editor else table

if table is None or table.empty:
    st.info("Click 'Update portfolio' to generate results." if use_editor else "Upload a CSV to generate results.")
    st.stop()

st.subheader("Overview")
st.dataframe(table.drop(columns=["datetime"]))

if "profit($)" in table.columns:
    st.subheader("Summary")
    total_profit = table['profit($)'].sum()
    total_cost = table['cost($)'].sum()

if total_cost != 0:
    total_return_pct = (total_profit / total_cost) * 100
else:
    total_return_pct = 0.0

st.write(f"Total profit: {total_profit:,.2f}$")
st.write(f"Total percentage profit: {total_return_pct:,.2f}%")
st.write(f"Total cost: {total_cost:,.2f}$")

st.subheader("Performance Graph")

ticker = st.selectbox(
    "Select stock",
    sorted(table["ticker"].unique())
)

row = table[table["ticker"] == ticker].iloc[0]
buy_date = row["datetime"]

fig = price_history_figure(ticker, buy_date)
st.pyplot(fig)

# Your existing upload (still supported)
st.subheader("Upload csv file")

uploaded = st.file_uploader("Upload csv file", type=["csv"], key="csv_uploader2")

positions_df = None

if uploaded is not None:
    positions_df = pd.read_csv(uploaded)
else:
    try:
        positions_df = pd.read_csv("config/positions.csv")
    except FileNotFoundError:
        st.info("Upload a csv file or create one above and save it to config/positions.csv")

if positions_df is not None:
    st.write("Loaded positions:")
    st.dataframe(positions_df, use_container_width=True)
