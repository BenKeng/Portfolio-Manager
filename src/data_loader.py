import yfinance as yf
import pandas as pd
from datetime import datetime

def load_data(positions: str) -> pd.DataFrame:
    df = pd.read_csv(positions, parse_dates = ['datetime'])
    current_position = {}
    buy_position = {}

    # Add dictonary here instead of lists. Current and buy position sollen columns in dem dictonary


    for _, r in df.iterrows():


        
        ticker = r["ticker"]      
        bdate  = (r["datetime"])      
        qty    = int(r["quantity"]) 
        c, b = stock_price(ticker, bdate, qty)  
        current_position = current_position.append(c)
        buy_position = buy_position.append(b)
        print(f"{ticker}: current {c:.2f} | buy {b:.2f}")
    
    return current_position, buy_position
   
    
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

