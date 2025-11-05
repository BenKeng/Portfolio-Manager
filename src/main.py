import yfinance as yf
import pandas as pd

from data_loader import load_data
from analytics import data_fetch

load_data('config/positions.csv')

data_fetch('config/positions.csv')
