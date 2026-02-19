import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf


def price_history_figure(ticker: str, buy_date) -> plt.Figure:
    """Generate price chart with a red buy date marker."""
    stock = yf.Ticker(ticker)

    # Fetch history since buy date
    hist = stock.history(start=buy_date, interval="1d")

    fig, ax = plt.subplots()
    ax.plot(hist.index, hist["Close"], linewidth=1.5)

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