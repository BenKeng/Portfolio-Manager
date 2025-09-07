import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import datetime
from data_loader import stock_price
from analytics import prof_calc

def plot(positions: str):
    df = pd.read_csv(positions, parse_dates = ['datetime'])

    for _, r in df.iterrows():
        ticker = r["ticker"]      
        bdate  = (r["datetime"])      
        qty    = int(r["quantity"]) 
        c, b = stock_price(ticker, bdate, qty)
        p, per_p = prof_calc(c, b)
        days = (datetime.datetime.today().date() - bdate.date()).days

        stock = yf.Ticker(ticker)
        hist = stock.history(period = 'max', interval= '5d')
        

        hist['Close'].plot()
        plt.xlabel("Date"); plt.ylabel("Price")
        plt.tight_layout(); plt.show()

plot('config/positions.csv')