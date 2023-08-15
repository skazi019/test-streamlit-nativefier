import datetime
import numpy as np

def trade_buy_trigger(st, portfolio):
    if len(portfolio[portfolio["Status"] == "WATCHLIST"]) > 0:
        for index, row in portfolio[portfolio["Status"] == "WATCHLIST"].iterrows():
            if row["LTP"] >= row["Buy Price"]:
                portfolio.loc[index, "Status"] = "OPEN"

    return portfolio

def trade_sell_trigger(st, portfolio):
    if len(portfolio[portfolio["Status"] == "OPEN"]) > 0:
        for index, row in portfolio[portfolio["Status"] == "OPEN"].iterrows():
            if row["LTP"] >= row["Sell SL"]:
                portfolio.loc[index, "Status"] = "CLOSED"
                portfolio.loc[index, "Sell Price"] = row["LTP"]
                portfolio.loc[index, "Sell Date"] = datetime.datetime.now().strftime("%d %B %Y")

    return portfolio

def trade_buy(st, portfolio, all_rows):
    portfolio.loc[portfolio["ID"].isin(all_rows), "Status"] = "OPEN"
    for id in all_rows:
        portfolio.loc[portfolio["ID"]==id, "Buy Price"] = portfolio.loc[portfolio["ID"]==id, "LTP"]

    return portfolio

def trade_sell(st, portfolio, all_rows):
    portfolio.loc[portfolio["ID"].isin(all_rows), "Status"] = "CLOSED"
    for id in all_rows:
        portfolio.loc[portfolio["ID"]==id, "Sell Price"] = portfolio.loc[portfolio["ID"]==id, "LTP"]
        portfolio.loc[portfolio["ID"]==id, "Sell Date"] = datetime.datetime.now().strftime("%d %B %Y")

    return portfolio
