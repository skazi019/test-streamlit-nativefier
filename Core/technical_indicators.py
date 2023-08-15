"""
author: Kaushal Sharma
date: 2021-11-05
This file fetches data for the specified scrip from the exchange
"""
import numpy as np


def calculate_all_emas(ticker_df):
    emas = [9, 21, 50, 90, 200]
    for ma in emas:
        ticker_df[f"EMA_{ma}"] = (
            ticker_df.loc[:, "Close"].ewm(span=ma, min_periods=ma, adjust=False).mean()
        )
        ticker_df[f"EMA_{ma}"] = ticker_df[f"EMA_{ma}"].round(2)
    return ticker_df


def calculate_all_vwma(ticker_df):
    emas = [9, 21, 50, 90, 200]
    for ma in emas:
        rolling_close = ticker_df["Close"].rolling(ma)
        rolling_volumne = ticker_df["Volume"].rolling(ma)
        ticker_df[f"{ma}_VWMA"] = ticker_df.rolling(ma).apply(
            lambda x: np.sum(x["Volume"] * x["Close"])
        )
    return ticker_df
