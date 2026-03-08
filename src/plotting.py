import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
import pandas as pd


def price_history_figure(ticker: str, buy_date) -> plt.Figure:
    """Generate price chart with a red buy date marker."""
    stock = yf.Ticker(ticker)

    # Fetch history since buy date
    hist = stock.history(start=buy_date, interval="1d")

    sma20 = hist["Close"].rolling(window=20).mean()

    fig, ax = plt.subplots()
    ax.plot(hist.index, hist["Close"], linewidth=1.5)
    ax.plot(hist.index, sma20, linestyle="--", color="orange", linewidth=1.5, label="20-day SMA")

    # Red dashed line shows the purchase point
    ax.axvline(x=buy_date, color="red", linestyle="--", linewidth=1, label="Buy date")
    ax.legend()

    ax.set_title(f"{ticker} — Price History")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price ($)")
    
    # Format X-axis dates for better readability
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.tight_layout()

    return fig


def multi_stock_history_figure(table) -> plt.Figure:
    """
    Generate a comparative price chart for all assets in the portfolio.
    This demonstrates algorithmic looping and comparative data visualization.
    """
    fig, ax = plt.subplots()

    # Iterate through each unique asset to plot its individual history
    for _, row in table.iterrows():
        ticker = row["Stock Ticker"]
        buy_date = row["Purchase Date"]
        stock = yf.Ticker(ticker)
        # Fetch data and plot line
        hist = stock.history(start=buy_date, interval="1d")
        ax.plot(hist.index, hist["Close"], label=ticker)

    ax.set_title("Comparative Portfolio Asset Performance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Share Price ($)")
    ax.legend()

    # Format X-axis for better date visibility
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.tight_layout()

    return fig


def volatility_figure(ticker: str, buy_date) -> plt.Figure:
    """Rolling 20-day volatility (std dev of daily returns) for a single stock."""
    stock = yf.Ticker(ticker)
    hist = stock.history(start=buy_date, interval="1d")

    daily_returns = hist["Close"].pct_change() * 100
    rolling_vol = daily_returns.rolling(window=20).std()

    fig, ax = plt.subplots()
    ax.plot(rolling_vol.index, rolling_vol, linewidth=1.5, color="purple")
    ax.set_title(f"{ticker} — 20-Day Rolling Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Price Swing (%)")
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.tight_layout()

    return fig


def portfolio_value_figure(table) -> plt.Figure:
    """Total portfolio value over time, summing each stock from its purchase date."""
    all_values = []

    for _, row in table.iterrows():
        ticker = row["Stock Ticker"]
        qty = row["Quantity"]
        buy_date = row["Purchase Date"]
        stock = yf.Ticker(ticker)
        hist = stock.history(start=buy_date, interval="1d")
        if hist.empty:
            continue
        value_series = hist["Close"] * qty
        value_series.name = ticker
        all_values.append(value_series)

    fig, ax = plt.subplots()

    if all_values:
        # Sum across stocks per date; NaN (before purchase) treated as 0
        combined = pd.concat(all_values, axis=1)
        portfolio_total = combined.sum(axis=1)
        ax.plot(portfolio_total.index, portfolio_total, linewidth=1.5, color="green")
        ax.fill_between(portfolio_total.index, portfolio_total, alpha=0.15, color="green")

    ax.set_title("Portfolio Total Value Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Value ($)")
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.tight_layout()

    return fig


def profit_loss_figure(table) -> plt.Figure:
    """Horizontal bar chart of unrealised P&L per stock, green/red by sign."""
    tickers = table["Stock Ticker"]
    profits = table["Profit ($)"]
    colors = ["green" if p >= 0 else "red" for p in profits]

    fig, ax = plt.subplots()
    ax.barh(tickers, profits, color=colors)
    ax.axvline(x=0, color="black", linewidth=0.8)
    ax.set_title("Unrealised Profit / Loss by Stock")
    ax.set_xlabel("Profit / Loss ($)")
    fig.tight_layout()

    return fig