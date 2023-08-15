import os
import time
import pathlib
import pandas as pd
import datetime
import numpy as np
import streamlit as sl

from state import State
from Core.fetch_ticker_data import fetch_and_store_yahoo_fin_data


def portfolio_file_path():
    file_path = os.path.join(pathlib.Path(__file__).parent.resolve(), "portolio.csv")
    return file_path


def check_portfolio_exists():
    file_path = portfolio_file_path()

    # check if the portolio exists or not
    try:
        df = pd.read_csv(file_path)
    except:
        df = pd.DataFrame(
            columns=[
                "ID",
                "Name",
                "Ticker",
                "Status",
                "Addition Date",
                "Buy Price",
                "Quantity",
                "LTP",
                "Sell SL",
                "Sell Price",
                "Sell Date",
                "Profit/Loss",
            ]
        )
        df.to_csv(file_path, index=False)


def get_portfolio():
    file_path = portfolio_file_path()
    check_portfolio_exists()
    df = pd.read_csv(file_path)
    return df


def save_portfolio(df):
    file_path = portfolio_file_path()
    df.to_csv(file_path, index=False)


def add_to_portfolio(st, buy_price, sell_sl, quantity):
    """
    Status: WATCHLIST or OPEN or CLOSED
    """
    ticker_data = State.get(st, "ticker_data")
    ticker_info = State.get(st, "ticker_info")
    ticker_data.rename(columns={"Date": "Datetime"}, inplace=True)
    name = ticker_info["longName"]
    ticker = State.get(st, "ticker")
    status = "WATCHLIST"
    addition_date = datetime.datetime.now().strftime("%d %B %Y")
    ltp = np.nan
    sell_price = np.nan
    sell_date = pd.NaT
    pnl = np.nan

    portfolio = get_portfolio()
    if len(portfolio) == 0:
        id = len(portfolio)
    else:
        id = sorted(portfolio["ID"].tolist())[-1] + 1

    new_data = pd.DataFrame(
        [
            [
                id,
                name,
                ticker,
                status,
                addition_date,
                buy_price,
                quantity,
                ltp,
                sell_sl,
                sell_price,
                sell_date,
                pnl,
            ]
        ],
        columns=portfolio.columns,
    )

    portfolio = pd.concat([portfolio, new_data])
    save_portfolio(portfolio)


@sl.cache_data
def calculate_portfolio_pnl(st, portfolio):
    watchlist_data = portfolio["Status"] == "WATCHLIST"
    open_trades = portfolio["Status"] == "OPEN"
    closed_trades = portfolio["Status"] == "CLOSED"

    portfolio.loc[open_trades, "Profit/Loss"] = (
        portfolio.loc[open_trades, "LTP"]
        - portfolio.loc[open_trades, "Buy Price"]
    ) * portfolio.loc[open_trades, "Quantity"]

    portfolio.loc[closed_trades , "Profit/Loss"] = (
        portfolio.loc[closed_trades , "Sell Price"]
        - portfolio.loc[closed_trades , "Buy Price"]
    ) * portfolio.loc[closed_trades , "Quantity"]

    return portfolio

@sl.cache_data
def get_current_price_portfolio(st, portfolio):

    with st.spinner("Fetching LTPs..."):
        for ticker in portfolio["Ticker"].unique().tolist():
            # getting the latest price of the ticker
            last_traded_price = fetch_and_store_yahoo_fin_data(st, ticker=ticker, period="1d", interval="1m")
            last_traded_price = last_traded_price["Close"][len(last_traded_price)-1]

            portfolio.loc[portfolio["Ticker"]==ticker, "LTP"] = last_traded_price
            time.sleep(2)

    return portfolio


