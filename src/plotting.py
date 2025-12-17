import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import datetime
from src.data_loader import stock_price



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

        plt.title(f"{ticker} Price History")
        plt.xlabel("Time(Years)"); plt.ylabel("Price($)")
        plt.tight_layout()
        return plt.gcf()
    
def price_history_figure(ticker: str):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max", interval="5d")

    fig, ax = plt.subplots()
    ax.plot(hist.index, hist["Close"])
    ax.set_title(f"{ticker} Price History")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price ($)")
    fig.tight_layout()

    return fig

if __name__ == "__main__":  
    plot('config/positions.csv')