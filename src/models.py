import pandas as pd
from datetime import datetime
from src.data_loader import fetch_stock_value

class StockPosition:
    """
    Represents an individual stock holding.
    Encapsulates position-specific data and calculation logic.
    """
    def __init__(self, ticker: str, purchase_date: datetime, quantity: int):
        self.ticker = ticker.upper()
        self.purchase_date = purchase_date
        self.quantity = quantity
        self.current_value = 0.0
        self.buy_value = 0.0
        self.profit = 0.0
        self.return_pct = 0.0
        self.cost_per_share = 0.0

    def update_metrics(self):
        """Fetches latest prices and recalculates profit/return metrics."""
        self.current_value, self.buy_value = fetch_stock_value(self.ticker, self.purchase_date, self.quantity)
        self.profit = self.current_value - self.buy_value
        self.return_pct = (self.profit / self.buy_value * 100) if self.buy_value != 0 else 0.0
        self.cost_per_share = self.buy_value / self.quantity if self.quantity > 0 else 0.0

    def to_dict(self):
        """Serializes position data for DataFrame/UI display."""
        return {
            "Stock Ticker": self.ticker,
            "Purchase Date": self.purchase_date,
            "Quantity": self.quantity,
            "Cost Per Share ($)": round(self.cost_per_share, 2),
            "Total Cost ($)": round(self.buy_value, 2),
            "Current Value ($)": round(self.current_value, 2),
            "Profit ($)": round(self.profit, 2),
            "Percentage Return (%)": round(self.return_pct, 2)
        }

class Portfolio:
    """
    Manages a collection of StockPosition objects.
    Demonstrates encapsulation and collection management.
    """
    def __init__(self):
        self.positions = []

    def add_position(self, ticker: str, purchase_date: datetime, quantity: int):
        """Adds a new StockPosition to the portfolio."""
        pos = StockPosition(ticker, purchase_date, quantity)
        self.positions.append(pos)

    def refresh_all(self):
        """Updates metrics for all positions in the portfolio."""
        for pos in self.positions:
            pos.update_metrics()

    def get_summary_df(self):
        """Returns a pandas DataFrame of all positions for display."""
        if not self.positions:
            return pd.DataFrame()
        return pd.DataFrame([pos.to_dict() for pos in self.positions])

    def get_totals(self):
        """Calculates aggregate portfolio metrics."""
        total_profit = sum(pos.profit for pos in self.positions)
        total_cost = sum(pos.buy_value for pos in self.positions)
        total_return = (total_profit / total_cost * 100) if total_cost != 0 else 0.0
        return total_profit, total_cost, total_return
