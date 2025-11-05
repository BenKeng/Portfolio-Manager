import pandas as pd
from datetime import datetime
from data_loader import stock_price

def prof_calc(c, b):
    profit = c - b
    percentage_profit = (c / b) * 100
    return profit, percentage_profit

print(prof_calc)