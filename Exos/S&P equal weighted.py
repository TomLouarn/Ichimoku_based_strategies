

import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
import time

API_KEY = "DHDGV6F2D97W4ICZ"

stocks = pd.read_csv("S&P500.csv", sep=None, engine = "python", index_col = 0)
stocks = stocks.dropna(how="all")
stocks = stocks.dropna(axis = 1, how="all")
tickers = stocks.Ticker.tolist()

print(stocks)
print(tickers)



my_columns = ["Ticker", "Stock Price", "Market Cap", "Shares to buy"]
final_df = pd.DataFrame (columns=my_columns, ignore_index=True)

for ticker in tickers:
    params = {
        "function" : "TIME_SERIES_DAILY",
        "symbol" : ticker,
        "apikey" : API_KEY,
    }
    api_url = "https://www.alphavantage.co/query"
    r = requests.get(api_url, params, timeout=15)
    data = r.json()
    price = data["Adj Close"]
    market_cap = data["Market Cap"]
    final_df = final_df.append(
        pd.Series([
            ticker,
            price,
            market_cap,
            "N/A"
        ], index=my_columns),
        ignore_index=True
    )


portfolio_size = input("Enter the portfolio size: ")

try:
    val = float(portfolio_size)
except ValueError:
    portfolio_size = input("Please enter a number\n Enter the portfolio size: ")
    val = float(portfolio_size)

position_size = portfolio_size/len(final_df.index)

for i in range(0, len(final_df.index)):
    final_df.iloc[i,3] = math.floor(position_size/final_df.iloc[i,1])


writer = pd.ExcelWriter ("S&P500EW.xlsx", engine = "xlsxwriter")
final_df.to_excel(writer, "S&P500EW.xlsx", index = False)

writer.sheets["S&PEW.xlsx"].set_columns("A:A", 18, string_format)
writer.sheets["S&PEW.xlsx"].set_columns("B:B", 18, string_format)
writer.sheets["S&PEW.xlsx"].set_columns("C:C", 18, string_format)
writer.sheets["S&PEW.xlsx"].set_columns("D:D", 18, string_format)


writer.sheets("S&PEW.xlsx").write("A1", "Ticker", string_format)
writer.sheets("S&PEW.xlsx").write("B1", "Stock Price", other_format)

#best way to do this :

column_format = {
    "A": ["Ticker", string_format]
    "B": ["Stock Price", other_format]
    "C":["Market Cap", other_format]
    "D": ["Shares to buy", other_format]
}

for column in column_format.keys():
    writer.sheets["S&PEW.xlsx"].set_column(f'{column}:{column}', 18, column_format.column[1])
    writer.sheets("S&PEW.xlsx").write(f"{column}1", column_format.column[0], column_format.column[1])

writer.save()




