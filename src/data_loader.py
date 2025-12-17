import yfinance as yf
import pandas as pd
from datetime import datetime

def load_data(positions: str) -> pd.DataFrame:
    df = pd.read_csv(positions, parse_dates = ['datetime'])
    current_position = {}
    buy_position = {}


    for _, r in df.iterrows():
        
        ticker = r["ticker"]      
        bdate  = (r["datetime"])      
        qty    = int(r["quantity"]) 
        c, b = stock_price(ticker, bdate, qty)  
        current_position[ticker] = c
        buy_position[ticker] = b
        print(f"{ticker}: current {c:.2f} | buy {b:.2f}")
    
    return b, c
   
    
def stock_price(ticker: str, bdate: datetime, quant: int):
    stock = yf.Ticker(ticker)

    cprice = stock.history(period='1d')['Close'].iloc[-1]
    
    hist = stock.history(period = 'max')
    hist.index = hist.index.tz_localize(None)
    StartPrice = hist.loc[bdate:, "Close"]
    bprice = StartPrice.iloc[0]

    cprice = cprice * quant
    bprice = bprice * quant
    
    return cprice, bprice


def load_data_table(positions: str) -> pd.DataFrame:
    df = pd.read_csv(positions, parse_dates=["datetime"])
    results = []

    for _, r in df.iterrows():
        ticker = r["ticker"]
        bdate = r["datetime"]
        qty = int(r["quantity"])
        c, b = stock_price(ticker, bdate, qty)

        results.append({
            "ticker": ticker,
            "datetime": bdate,  
            "quantity": qty,
            "buy": round(b, 2),
            "current": round(c, 2),
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    load_data("config/positions.csv")