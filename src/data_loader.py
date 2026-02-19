import yfinance as yf
import pandas as pd
from datetime import datetime

def is_valid_ticker(ticker: str) -> bool:
    """Validator to check if ticker actually exists on Yahoo Finance."""
    stock = yf.Ticker(ticker)
    try:
        # If history comes back empty, the ticker is likely invalid
        hist = stock.history(period="1d")
        return not hist.empty
    except:
        return False

def fetch_stock_value(ticker: str, bdate: datetime, quant: int) -> tuple:
    """Retrieve position valuations using historical and current data."""
    stock = yf.Ticker(ticker)

    # Latest market closing price
    hist_current = stock.history(period='1d')
    if hist_current.empty: return 0.0, 0.0
    current_price = hist_current['Close'].iloc[-1]

    # Max history with timezone normalization for slicing
    hist = stock.history(period='max')
    hist.index = hist.index.tz_localize(None)

    # First available closing price at or after purchase date
    start_prices = hist.loc[bdate:, "Close"]
    if start_prices.empty: return current_price * quant, 0.0 # Handle dates out of range
    buy_price = start_prices.iloc[0]

    return current_price * quant, buy_price * quant


def load_data_table(positions_path: str) -> pd.DataFrame:
    """CSV deserializer to convert flat files into analytic dataframes."""
    df = pd.read_csv(positions_path, parse_dates=["datetime"])
    results = []

    for _, r in df.iterrows():
        ticker = r["ticker"]
        bdate = r["datetime"]
        qty = int(r["quantity"])
        c, b = fetch_stock_value(ticker, bdate, qty)

        results.append({
            "Stock Ticker": ticker.upper(),
            "Purchase Date": bdate,  
            "Quantity": qty,
            "Total Cost ($)": round(b, 2),
            "Current Value ($)": round(c, 2),
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    load_data_table("config/positions.csv")