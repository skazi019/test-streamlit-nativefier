import streamlit as st
from streamlit_option_menu import option_menu
from render_sidebar import render_sidebar
from app_config import set_app_config
from state import State
from Core.fetch_ticker_data import fetch_and_store_yahoo_fin_data
from Core.fetch_ticker_data import (
    fetch_yahoo_fin_info,
    fetch_yahoo_fin_income_statement,
    fetch_yahoo_fin_balance_sheet,
)
from Tabs.CompanyDetails.details_tab import ticker_details_tab
from Tabs.CandlestickPatterns.tab_candlestick_patterns import tab_candlestick_pattern
from Tabs.TechnicalAnalysis.tab_technical_analysis import tab_technical_analysis
from Tabs.News.tab_news import tab_news
from Tabs.Financials.tab_financials import tab_financials
from Tabs.Options.tab_options import tab_options
from Tabs.Portfolio.tab_portfolio import tab_portfolio


set_app_config(st)
render_sidebar(st)

user_ticker = State.get(st, "ticker")

if (
    State.get(st, "ticker") is None
    or State.get(st, "ticker_period") is None
    or State.get(st, "ticker_interval") is None
):
    st.header("Portfolio")
    st.markdown("---")
    tab_portfolio(st)
    st.stop()

tab_menu_selected = option_menu(
    None,
    ["Company Details", "Financials", "Technical Analysis", "Portfolio"],
    orientation="horizontal",
    icons=["buildings-fill", "bank2", "graph-up-arrow", "basket"],
)

if tab_menu_selected == "Company Details":
    ticker_info = fetch_yahoo_fin_info(State.get(st, "ticker"))
    State.state_add(st, "ticker_info", ticker_info)
    ticker_details_tab(
        st, ticker=State.get(st, "ticker"), ticker_info=State.get(st, "ticker_info")
    )


if tab_menu_selected == "Financials":
    tab_financials(st)

if tab_menu_selected == "News":
    tab_news(st)

if tab_menu_selected == "Technical Analysis":
    tab_technical_analysis(st)

if tab_menu_selected == "CandleStick Patterns":
    tab_candlestick_pattern(st)

if tab_menu_selected == "Options":
    tab_options(st)

if tab_menu_selected == "Portfolio":
    tab_portfolio(st)
