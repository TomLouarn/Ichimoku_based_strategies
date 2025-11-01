import pandas as pd
import numpy as np
import math
import xlsxwriter
import yfinance as yf
from scipy import stats

stocks = pd.read_csv("S&P500.csv", sep=None, engine='python', index_col=0)
stocks = stocks.dropna(how="all").dropna(axis = 1, how = "all")

tickers = stocks["Ticker"].astype(str).tolist()
tickers = tickers[:5]
print(tickers)

data = yf.download(tickers, period="1y", interval="1d", group_by="ticker", auto_adjust=True, progress= False)

my_columns = ["Ticker", "Close", "Volume", "Return", "Shares to buy"]

close_price = pd.concat({t: data[t]["Close"] for t in tickers}, axis=1)
volumes = pd.concat({t: data[t]["Volume"] for t in tickers}, axis=1)

"""historical_df = (pd.concat([
    close_price.stack().rename("Close"),
    volumes.stack().rename("Volume"),
    market_cap.stack().rename("Market Cap")],
    axis=1).reset_index().rename(columns={"level_0":"Date", "level_1":"Ticker"}))

print(historical_df)"""

rows = []

for ticker in tickers:
    last_close = close_price[ticker].iloc[-1]
    first_close = close_price[ticker].iloc[0]
    last_volumes = volumes[ticker].iloc[-1]
    rows.append({
        "Ticker" : ticker,
        "First Close" : first_close,
        "Close": last_close,
        "Volume" : last_volumes,
        "Shares to buy" : "N/A"
    })

final_df = pd.DataFrame(rows, columns = my_columns)

def one_year_return(series: pd.Series) -> float:
    s = series.dropna()
    if len(s) < 2:
        return np.nan
    return s.iloc[-1]/s.iloc[0]-1

returns_1y = close_price.apply(one_year_return, axis=0)

"""market_caps = {}
for t in tickers:
    try:
        market_caps[t] = yf.Ticker(t).fast_info.get("market_cap", np.nan)
    except Exception as e:
        market_caps[t] = np.nan"""

result = pd.DataFrame ({
    "Ticker" : returns_1y.index,
    #"Market Cap": [market_caps.get(t,np.nan) for t in returns_1y.index],
    "Return": (returns_1y.values * 100)
})

final_df["Return"] = result["Return"]

final_df = final_df[final_df["Return"] >30].sort_values("Return", ascending=False, inplace=True)

print(final_df)
print(len(final_df))
