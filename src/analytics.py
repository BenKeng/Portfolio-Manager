import pandas as pd
from src.data_loader import stock_price

def load_data2(positions: str) -> pd.DataFrame:
    df = pd.read_csv(positions, parse_dates = ['datetime'])
    current_position = {}
    buy_position = {}
    results = []
    for _, r in df.iterrows():
        
        ticker = r["ticker"]      
        bdate  = (r["datetime"])      
        qty    = int(r["quantity"]) 
        c, b = stock_price(ticker, bdate, qty)  
        current_position[ticker] = c
        buy_position[ticker] = b
        profit = c - b
        percentage_profit = (profit / b) * 100
        print(float(round(profit, 2)), float(round(percentage_profit, 2)))

        results.append({
            "ticker": ticker,
            "profit($)": round(profit, 2),
            "percentage profit(%)": round(percentage_profit, 2),
        })
    return pd.DataFrame(results)
    
if __name__ == "__main__":    
    load_data2("config/positions.csv")

