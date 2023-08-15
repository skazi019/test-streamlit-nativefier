import os
import time
import pandas as pd
from pandas.core.dtypes.common import validate_all_hashable
from state import State
from streamlit_pills import pills
import streamlit_toggle as tog

from Core.fetch_ticker_data import fetch_and_store_yahoo_fin_data, fetch_yahoo_fin_info
from Tabs.Portfolio.portfolio_utils import add_to_portfolio


def load_all_tickers():
    sector_path = os.path.join(os.getcwd(), "all_sector_ticker.csv")
    sectors_tickers = pd.read_csv(sector_path)
    sectors_tickers.reset_index(inplace=True, drop=True)
    sectors = sectors_tickers['Sector'].unique().tolist()
    sectors.insert(0, "All")
    return sectors, sectors_tickers


def render_sidebar(st):
    with st.spinner("Loading data..."):
        sectors, all_sector_data = load_all_tickers()
        sectors.insert(0, "")
        with st.sidebar:
            if st.button("Refresh"):
                st.cache_data.clear()
                State.state_clear(st)
                time.sleep(2)
                st.experimental_rerun()

            sector_user_selection = st.selectbox("Select Sector", options=sectors, index=0)

            if sector_user_selection and sector_user_selection is not None:
                State.state_remove_multiple(st, ["ticker", "ticker_period", "ticker_interval"])

                if sector_user_selection == "All":
                    tickers = all_sector_data["Symbol"].unique().tolist()
                else:
                    tickers = all_sector_data[all_sector_data['Sector']==sector_user_selection]["Symbol"].unique().tolist()

                tickers.insert(0, "")
                ticker_user_selection = st.selectbox("Select Ticker", options=tickers, index=0)
                State.state_update(st, "ticker", ticker_user_selection)

                valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
                valid_intervals = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]


                if ticker_user_selection and ticker_user_selection is not None:
                    period_user_selection = pills("Select Period", options=valid_periods, index=valid_periods.index("2y"))
                    State.state_update(st, "ticker_period", period_user_selection)

                    if period_user_selection and period_user_selection is not None:
                        interval_user_selection = pills("Select Interval", options=valid_intervals, index=valid_intervals.index("1d"))

                        if interval_user_selection and interval_user_selection is not None:
                            State.state_update(st, "ticker_interval", interval_user_selection)

                            fetch_and_store_yahoo_fin_data(
                                st,
                                ticker=State.get(st, "ticker"),
                                period=State.get(st, "ticker_period"),
                                interval=State.get(st, "ticker_interval"),
                            )
                            ticker_info = fetch_yahoo_fin_info(State.get(st, "ticker"))
                            State.state_update(st, "ticker_info", ticker_info)

                            st.divider()
                            st.write("**Add to Portfolio**")

                            ticker_data = State.get(st, "ticker_data")
                            ticker_data.rename(columns={"Date": "Datetime"}, inplace=True)
                            last_price = ticker_data["Close"][len(ticker_data)-1]

                            buy_trigger = st.number_input("Buy Trigger", value=last_price, key="portfolio_buy_trigger")
                            sell_sl = st.number_input("Sell Stop Loss", value=last_price, key="portfolio_stoploss")
                            quantity = st.number_input("Quantity", value=1, key="portfolio_quantity")
                            if st.button("Add", on_click=add_to_portfolio, args=(st, buy_trigger, sell_sl, quantity)):
                                success_msg = st.empty()
                                success_msg.success("Added to portfolio")
                                time.sleep(1)
                                success_msg.empty()
