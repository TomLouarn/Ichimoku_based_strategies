"""
The objective of this code is to build and analize an equity portfolio.

To achieve this, the code has two main goals:

    - Provide detailed information on the buying opportunity of a stock
        Charts, Ichimoku, RSI, Bollinger Bands

    Allow the user to create a portfolio and analyze it
        Calculation of Sharpe Ratio, Value at Risk (VaR),
        Expected Shortfall (ES) using historical data and Monte Carlo simulation,
        Maximum Drawdown, and estimated average return
        """

import pandas as pd
import yfinance as yf
import mplfinance as mpf
import plotly.graph_objects as go
import streamlit as st
from typing import List

from numpy.ma.core import empty

xlsx = pd.read_excel("tickers_indices.xlsx", index_col=0, engine="openpyxl")

def download_data(ticker: str, period="6y", interval="1d") -> pd.DataFrame:
    """
    Download historical data for the different tickers from Yahoo Finance,
    before testing the process with the Alpha Vantage API

    Parameters:
        ticker (str): The ticker symbol
        """

    data = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        progress=False,
        auto_adjust=True)
    return data

def final_df(tickers: List[str], period="6y", interval="1d") -> pd.DataFrame:
    """
    Create final dataframe from the tickers list

    Parameters:
        tickers: the tickers list
        period: the period of the data
        interval: the interval of the data
    """
    frame=[]
    for ticker in tickers:
        raw = download_data(ticker, period, interval).sort_index()
        raw["Ticker"] = ticker
        frame.append(raw)

    df = pd.concat(frame)
    df = df.groupby("Ticker", group_keys=False).apply(lambda x : x.ffill().dropna(how="all"))
    return df

def close_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """ Transform a long dataframe into a short dataframe

    Parameters:
        df (pd.DataFrame): The dataframe to be transformed"""
    close = (df
             .reset_index()
             .pivot(index="Date", columns="Ticker", values="Close")
             .sort_index()
             .ffill()
             .dropna(how="all")
             )
    return close


def save_csv(dataframe, filename):
    """
    Save the dataframe as a csv file

    Parameters:
        dataframe (pandas.DataFrame): The dataframe to save
        filename (str): The filename to save the data in
    """
    dataframe.to_csv(filename)

def load_csv(filename):
    """
    Load the csv file

    Parameters:
        filename (str): The filename of the csv file to read
    """
    dataframe = pd.read_csv(filename, index_col=0, parse_dates=True)
    return dataframe


def plot_single_stock(dataframe, tickers):
    """
    Plot the dataframe for each ticker

    Parameters:
        dataframe (pandas.DataFrame): The dataframe to plot
        tickers : list of ticker
    """

    for t in tickers:
        dft = (dataframe[dataframe["Ticker"] == t].loc[:, ["Open", "High", "Low", "Close"]].dropna(how="all").copy())
        if dft.empty:
            print(f"No data found for {t}")
            continue
        dft.index.name = "Date"
        dft = dft.sort.index()

        mpf.plot(
            dataframe,
            type = "candle",
            style = "yahoo",
            volume = True,
            mav = (20,50,200),
            figsize= (13,7),
            tight_layout = True,
            title = f"{t} Stock Price",
        )

""" Version Graphique pour Streamlit avec Plotly

def plot_stock_price(df, ticker, title_suffix="Stock Price (Plotly)"):

    if "Close" not in df.columns:
        raise ValueError("Le DataFrame doit contenir une colonne 'Close'.")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            mode="lines",
            name=f"{ticker}",
            line=dict(width=2, color="#1f77b4")
        )
    )

    fig.update_layout(
        title=f"{ticker} — {title_suffix}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white",
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
        width=1100,
        height=600
    )

    fig.show()"""

def plot_portfolio(dataframe):
    """
    Plot the dataframe of the portfolio

    Parameters:
        dataframe: The dataframe containing all the portfolio data
    """

def number_of_shares(tickers):
    """
    Ask the number of shares of each stock

    Parameters:
        tickers: the tickers list
    """
    shares = {}
    for ticker in tickers:
        while True :
            raw = input(f"Number of shares for {ticker} : ").strip().replace(",", ".")
            try:
                shares[ticker] = float(raw)
                break
            except ValueError:
                print("Please enter a valid number.")
    return pd.Series(shares, name = "shares")

def last_price (close, shares):
    """
    print the last price of a stock and the value of the stock in the portfolio

    Parameters:
        close (pd.Series): The close price of the stock
        shares (int): The number of shares
    """
    shares = shares.reindex(close.columns).fillna(0.0)
    price = close.iloc[-1].reindex(shares.index)
    position_value = (price*shares).round(2)
    total_value = float(position_value.sum().round(2))
    return price, position_value, total_value

def main():
    """
    Call others functions to make the code work

    Parameters:
        tickers (str): The tickers symbol to use
    """

def main():
    raw = input("Enter tickers (e.g., AAPL, TSLA, AMZN): ").upper().strip()
    tickers = [t.strip() for t in raw.split(",") if t.strip()]
    if not tickers:
        print("No tickers entered. Exiting...");
        return

    df_long = final_df(tickers)
    close = close_matrix(df_long)

    shares = number_of_shares(tickers)

    last_prices, pos_value, total_val = last_price(close, shares)
    print("\n Last Prices:");
    print(last_prices.round(2).rename("Price").to_frame().to_string())
    print("\n Position Value:");
    print(pos_value.rename("Value").to_frame().to_string())
    print("\n Total Value:");
    print(f" {total_val:,.2f}")

    plot_single_stock(df_long, tickers)

if __name__ == "__main__":
    main()
