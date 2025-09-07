import yfinance as yf
import pandas as pd

from data_loader import load_data
from analytics import data_fetch

def run_all():

    current_position, buy_position = load_data('config/positions.csv')

    profit, percentage_profit = prof_calc(current_position, buy_position)


if __name__ == "__main__":
    run_all()