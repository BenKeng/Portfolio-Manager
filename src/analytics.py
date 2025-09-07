import pandas as pd
from datetime import datetime
from data_loader import stock_price

def prof_calc(current_position, buy_position):
    profit = c - b
    percentage_profit = (c / b) * 100
    return profit, percentage_profit