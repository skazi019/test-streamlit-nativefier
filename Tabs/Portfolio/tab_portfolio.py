import os
import numpy as np
import time
import pandas as pd
import pathlib

from state import State
from st_aggrid import (
    AgGrid,
    GridOptionsBuilder,
    GridUpdateMode,
    DataReturnMode,
    ColumnsAutoSizeMode,
)
from Tabs.Portfolio.portfolio_utils import get_portfolio, calculate_portfolio_pnl, get_current_price_portfolio, save_portfolio 
from Tabs.Portfolio.portfolio_triggers import trade_buy_trigger, trade_sell_trigger, trade_buy, trade_sell


def get_aggrid(data, type):
    data.reset_index(inplace=True, drop=True)
    gd = GridOptionsBuilder.from_dataframe(data)
    gd.configure_selection(use_checkbox=True, selection_mode="multiple")
    gd.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)

    gridOptions = gd.build()
    return AgGrid(
        data,
        height=500,
        theme="alpine",
        gridOptions=gridOptions,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
        header_checkbox_selection_filtered_only=True,
        use_checkbox=True,
    )


def tab_portfolio(st):
    portfolio = get_portfolio()

    if len(portfolio) < 1:
        st.info("Nothing added in portfolio. User the Add to Portfolio button in sidebar to start making trades.")
        st.stop()

    portfolio = get_current_price_portfolio(st, portfolio)
    portfolio = trade_buy_trigger(st, portfolio)
    portfolio = trade_sell_trigger(st, portfolio)
    portfolio = calculate_portfolio_pnl(st, portfolio)

    st.subheader("Open Trades")
    if len(portfolio[portfolio["Status"] == "OPEN"]) > 0:
        open_trades_df = get_aggrid(portfolio[portfolio["Status"] == "OPEN"], "open")

        if len(open_trades_df["selected_rows"]) > 0:
            close_col, delete_col, _, _, _ = st.columns(5)

            with close_col:
                if st.button("Close Trade"):
                    all_rows = []
                    for row in open_trades_df["selected_rows"]:
                        all_rows.append(row["ID"])

                    portfolio = trade_sell(st, portfolio, all_rows)
                    save_portfolio(portfolio)
                    st.success("Selected trade closed")
                    st.experimental_rerun()

            with delete_col:
                if st.button("Delete Trade"):
                    st.success("selected trades deleted")
                    all_rows = []
                    for row in open_trades_df["selected_rows"]:
                        all_rows.append(row["ID"])

                    portfolio.drop(all_rows, axis=0, inplace=True)
                    save_portfolio(portfolio)
                    st.experimental_rerun()
    else:
        st.info("No trades to show")


    st.subheader("Watchlist")
    if len(portfolio[portfolio["Status"] == "WATCHLIST"]) > 0:
        pending_trades_df = get_aggrid(portfolio[portfolio["Status"] == "WATCHLIST"], "watchlist")

        if len(pending_trades_df["selected_rows"]) > 0:
            wl_open_trade, wl_delete_col, _, _, _ = st.columns(5)

            with wl_open_trade:
                if st.button("Open Trade"):
                    all_rows = []
                    for row in pending_trades_df["selected_rows"]:
                        all_rows.append(row["ID"])

                    portfolio = trade_buy(st, portfolio, all_rows)
                    save_portfolio(portfolio)
                    st.success("Selected trade opened")
                    st.experimental_rerun()

            with wl_delete_col:
                if st.button("Delete Trade"):
                    st.success("selected trades deleted")
                    all_rows = []
                    for row in pending_trades_df["selected_rows"]:
                        all_rows.append(row["ID"])

                    portfolio.drop(all_rows, axis=0, inplace=True)
                    save_portfolio(portfolio)
                    st.experimental_rerun()
    else:
        st.info("No trades to show")

    st.subheader("Closed Trades")
    if len(portfolio[portfolio["Status"] == "CLOSED"]) > 0:
        closed_trades_df = get_aggrid(portfolio[portfolio["Status"] == "CLOSED"], "closed")

        if len(closed_trades_df  ["selected_rows"]) > 0:
            cl_delete_col, _, _, _, _ = st.columns(5)

            with cl_delete_col:
                if st.button("Delete Trade"):
                    st.success("selected trades deleted")
                    all_rows = []
                    for row in closed_trades_df["selected_rows"]:
                        all_rows.append(row["ID"])

                    portfolio.drop(all_rows, axis=0, inplace=True)
                    save_portfolio(portfolio)
                    st.experimental_rerun()
    else:
        st.info("No trades to show")
