import pandas as pd
from datetime import datetime
from data_loader import stock_price

def data_fetch(positions: str) -> pd.DataFrame:
    df = pd.read_csv(positions, parse_dates = ['datetime'])

    for _, r in df.iterrows():
        ticker = r["ticker"]      
        bdate  = (r["datetime"])      
        qty    = int(r["quantity"]) 
        c, b = stock_price(ticker, bdate, qty)
        p, per_p = prof_calc(c, b)
        print(f"{ticker}: profit: {p:.2f}$      percentage profit: {per_p:.2f}%")
        days = (datetime.today().date() - bdate.date()).days
        pro_day = p / days
        print(f'    Held for {days} days    profit per day:  {pro_day:.2f}$')

def prof_calc(c: float, b: float):
    profit = c - b
    percentage_profit = (c / b) * 100
    return profit, percentage_profit


