import numpy as np
import talib
import time
from streamlit_echarts import st_echarts
from state import State
from config import (
    candlestick_down_color,
    candlestick_down_border_color,
    candlestick_up_color,
    candlestick_up_border_color,
)
from Tabs.CandlestickPatterns.talib_available_patterns import (
    get_all_candlestick_patterns,
)
from Tabs.CandlestickPatterns.plot_cdl_pattern import plot_candlestick_pattern


def tab_candlestick_pattern(st):
    all_candlestick_patterns = get_all_candlestick_patterns()
    ticker_data = State.get(st, "ticker_data")
    ticker_data.rename(columns={"Date": "Datetime"}, inplace=True)
    ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
    ticker_data = ticker_data[["Datetime", "Open", "High", "Low", "Close"]]

    if len(ticker_data) < 1:
        st.warning(
            "No data found. Please select a Sector, Ticker, Period, and Interval from the sidebar to proceed"
        )
        st.stop()

    pattern_found = []
    completion = iter(np.linspace(0, 1, len(all_candlestick_patterns) + 1)[1:])
    candlestick_scanning_pb = st.progress(0, text="")
    cdl_plot_size_col1, _ = st.columns([1, 4])

    cdl_patterns_plot_size = State.state_add(st, "cdl_patterns_plot_size", "400px")
    plot_size_list = ["300px", "400px", "500px", "600px", "700px"]
    with cdl_plot_size_col1:
        cdl_patterns_plot_size = st.selectbox(
            "plot size",
            index=plot_size_list.index(cdl_patterns_plot_size),
            options=plot_size_list,
            placeholder="Plot size",
            key="cdl_plot_size_key",
        )

    for name, pattern in all_candlestick_patterns.items():
        candlestick_scanning_pb.progress(next(completion), text=f"Scanning for {name}")
        result = pattern(
            ticker_data["Open"],
            ticker_data["High"],
            ticker_data["Low"],
            ticker_data["Close"],
        )
        result_temp = [x == 0 for x in result]
        if all(result_temp):
            continue

        pattern_found.append(name)
        ticker_data["cdl_pattern"] = result

        # Selecting the high of the row where candle pattern is detected to plot the pin above the candle in the chart
        pattern_df_temp = ticker_data.loc[
            ticker_data["cdl_pattern"] != 0, ["Datetime", "High"]
        ].values.tolist()

        pattern_mark_points = [
            {"name": "coordinate", "coord": [str(x) for x in row]} for row in pattern_df_temp
        ]
        plot_candlestick_pattern(st, ticker_data=ticker_data, name=name, mark_points=pattern_mark_points, plot_size=cdl_patterns_plot_size)

    if len(pattern_found) > 1:
        candlestick_scanning_pb.success(
            f"""
            Scanning for all candlestick patterns complete. Below are the patterns found for the selected ticker\n
            {", ".join(pattern_found)}
            """
        )
    else:
        candlestick_scanning_pb.info(
            "Scanning for all candlestick patterns complete. No pattern found in the selected ticker"
        )
