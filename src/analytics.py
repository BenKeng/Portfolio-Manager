import pandas as pd
from src.data_loader import stock_price
import math
import streamlit as st

def load_data2(positions: str):
    try:
        df = pd.read_csv(positions, parse_dates=["datetime"])
    except ValueError:
        st.error("csv file is not compatible.")
        return None
    #the table from the CSV file gets turned into a dataframe 
    current_position = {}
    buy_position = {}
    results = []
    #creates 2 dictionaries and 1 list to store values in
    for _, r in df.iterrows():

        ticker = r["ticker"]      
        bdate  = (r["datetime"])     
        q = r.get("quantity")

        if q is None or (isinstance(q, float) and math.isnan(q)):
            raise ValueError("Data is missing or invalid.")
        qty = int(q)
        c, b = stock_price(ticker, bdate, qty)  
        current_position[ticker] = c
        buy_position[ticker] = b
        profit = c - b
        percentage_profit = (profit / b) * 100
        print(float(round(profit, 2)), float(round(percentage_profit, 2)))

        qty = float(q) if q is not None else 0.0
        cost_per_stock = round(b / qty, 2) if qty > 0 else None

        results.append({
            "ticker": ticker,
            "datetime": bdate, 
            "quantity": qty,
            "profit($)": round(profit, 2),
            "percentage profit(%)": round(percentage_profit, 2),
            "cost per stock($)": round(cost_per_stock, 2),
            "cost($)": round(b, 2),
        })

    return pd.DataFrame(results)
