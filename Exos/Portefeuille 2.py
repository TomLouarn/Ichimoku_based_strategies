"""xxx"""

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

TICKERS = ["NVDA", "AAPL", "MSFT", "AMZN", "META", "AVGO", "TSLA"]

def get_prices (tickers, period:str = "1y", interval:str = "1d"):
    data = yf.download(tickers, period=period, interval=interval, auto_adjust=True, progress=False)

    if data["Close"].empty :
        data["Close"] = data["Adj Close"]

    close = data["Close"]

    if isinstance(close, pd.Series):
        name = tickers if isinstance(tickers, str) else tickers[0]
        close = close.to_frame(name=name)

    close = close.dropna(how="all")

    return close

def ask_shares (tickers):
    print("How many shares do you have ?")
    shares = {}
    for t in tickers:
        n = input(f"for {t}: ").strip()
        shares[t] = int(n) if n else 0

    return shares

def portfolio(prices: pd.DataFrame, shares: dict):
    s = pd.Series(shares).reindex(prices.columns).fillna(0)
    port = (s*prices).sum(axis=1)
    port.name = "Portfolio"
    return port

def last_day(prices: pd.DataFrame, shares: dict)-> pd.DataFrame:
    last = prices.iloc[-1]
    recap = pd.DataFrame({
        "Price": last,
        "Qty": pd.Series(shares),
        "Value": last*pd.Series(shares)
    }).fillna(0).sort_values("Value", ascending=False)
    return recap

def plot_portfolio(port: pd.Series):
    plt.figure(figsize=(10,5))
    plt.plot(port.index, port.values)
    plt.title("Portfolio")
    plt.xlabel("Date")
    plt.ylabel("USD")
    plt.grid(False)
    plt.tight_layout()
    plt.show()

def main():
    period = "1y"
    interval = "1d"
    tickers = TICKERS

    prices = get_prices(tickers, period, interval)
    print(prices.tail(3))

    shares = ask_shares(prices.columns.tolist())
    port = portfolio(prices, shares)
    valeur_totale = float(port.iloc[-1])
    print(f"La valeur du portfolio est de ${valeur_totale:,.2f}")

    recap = last_day(prices, shares)
    print(recap)

    plot_portfolio(port)

if __name__ == "__main__":
    main()