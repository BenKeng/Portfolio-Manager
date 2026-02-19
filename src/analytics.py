import pandas as pd
from src.models import Portfolio

def build_portfolio_from_csv(positions_path: str) -> Portfolio:
    """Factory function to generate a Portfolio object from a CSV source."""
    df = pd.read_csv(positions_path)
    # Flexible column detection
    date_col = "datetime" if "datetime" in df.columns else "date" if "date" in df.columns else None

    if not date_col or "ticker" not in df.columns:
        raise ValueError("Invalid CSV format.")

    df[date_col] = pd.to_datetime(df[date_col])
    
    portfolio = Portfolio()
    for _, r in df.iterrows():
        portfolio.add_position(r["ticker"], r[date_col], int(r["quantity"]))
    
    portfolio.refresh_all()
    return portfolio

# Legacy compatibility wrapper
def load_data2(positions: str) -> pd.DataFrame:
    """Wrapper to maintain compatibility with view layer during refactor."""
    pf = build_portfolio_from_csv(positions)
    return pf.get_summary_df()
