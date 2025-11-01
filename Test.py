import yfinance as yf
import pandas as pd

tickers = "AAPL,GOOG"
tickers = tickers.split(",")
print(tickers)

data = []
for ticker in tickers:
    raw = yf.download(ticker, period="5y", interval="1d", progress=False, auto_adjust=True)
    raw["Ticker"] = ticker
    data.append(raw)

df = pd.concat(data, axis=1)

print(df.Close.iloc[-1])

