"""
author: Kaushal Sharma
date: 2021-11-05
This file fetches data for the specified scrip from the exchange
"""
import yfinance
import streamlit as sl
from state import State
import datetime

from ta import add_all_ta_features
from ta.utils import dropna


@sl.cache_data
def fetch_and_store_yahoo_fin_data(st, ticker: str, period: str, interval: str):
    df = yfinance.download(
        tickers=f"{ticker}.NS", period=f"{period}", interval=f"{interval}"
    )
    df = df.round(2)
    df = df.dropna()
    # df = add_all_ta_features(
    #     df,
    #     open="Open",
    #     high="High",
    #     low="Low",
    #     close="Close",
    #     volume="Volume",
    #     fillna=True,
    # )
    df.reset_index(inplace=True)
    State.state_update(st, "ticker_data", df)
    return df


@sl.cache_data
def fetch_yahoo_fin_info(ticker):
    ticker = yfinance.Ticker(f"{ticker}.NS")
    ticker_info = ticker.info
    return ticker_info


@sl.cache_data
def fetch_yahoo_fin_income_statement(ticker: str):
    ticker = yfinance.Ticker(f"{ticker}.NS")
    ticker_stmt = ticker.income_stmt
    ticker_stmt.fillna(0, inplace=True)
    ticker_q_stmt = ticker.quarterly_income_stmt
    ticker_q_stmt.fillna(0, inplace=True)
    return ticker_stmt, ticker_q_stmt


@sl.cache_data
def fetch_yahoo_fin_balance_sheet(ticker: str):
    ticker = yfinance.Ticker(f"{ticker}.NS")
    ticker_bs = ticker.balance_sheet
    ticker_bs.fillna(0, inplace=True)
    ticker_q_bs = ticker.quarterly_balance_sheet
    ticker_q_bs.fillna(0, inplace=True)
    return ticker_bs, ticker_q_bs


@sl.cache_data
def fetch_yahoo_fin_news(ticker: str):
    ticker = yfinance.Ticker(f"{ticker}.NS")
    ticker_news = ticker.news
    return ticker_news


@sl.cache_data
def fetch_yahoo_option_chain(ticker: str):
    current_date = str(datetime.datetime.now().date())
    ticker = yfinance.Ticker(f"{ticker}.NS")
    # ticker_options_chain = ticker.option_chain(current_date)
    try:
        ticker_options_chain = ticker.option_chain("2023-07-27")
    except ValueError:
        return False, []
    else:
        return True, ticker_options_chain
