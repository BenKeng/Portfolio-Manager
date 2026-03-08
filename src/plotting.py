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
    all_returns = []

    # Iterate through each unique asset to plot its individual history
    for _, row in table.iterrows():
        ticker = row["Stock Ticker"]
        buy_date = row["Purchase Date"]
        stock = yf.Ticker(ticker)
        # Fetch data, normalise to % return from first price, and plot
        hist = stock.history(start=buy_date, interval="1d")
        if hist.empty:
            continue
        pct_return = (hist["Close"] - hist["Close"].iloc[0]) / hist["Close"].iloc[0] * 100
        ax.plot(pct_return.index, pct_return, label=ticker)
        all_returns.append(pct_return)

    # Average performance line across all stocks
    if all_returns:
        avg = pd.concat(all_returns, axis=1).mean(axis=1)
        ax.plot(avg.index, avg, color="black", linewidth=2, linestyle="--", label="Portfolio Average")

    ax.set_title("Comparative Portfolio Asset Performance")
    ax.set_xlabel("Date")
    ax.set_ylabel("Return (%)")
    ax.legend()
    
    # Format X-axis for better date visibility
    fig.autofmt_xdate()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.tight_layout()
    
    return fig