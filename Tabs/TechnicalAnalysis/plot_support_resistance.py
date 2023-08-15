import pandas as pd
from state import State
from streamlit_echarts import st_echarts

from config import (
    candlestick_down_color,
    candlestick_down_border_color,
    candlestick_up_color,
    candlestick_up_border_color,
)
from Tabs.TechnicalAnalysis.CustomStrategies.price_action import (
    get_support_resistance_levels,
    average_levels,
)


def get_cleanted_levels(st, ticker_data, sr_past_window_size, sr_future_window_size):
    support_levels, resistance_levels = get_support_resistance_levels(
        st, df=ticker_data, n1=sr_past_window_size, n2=sr_future_window_size
    )

    avg_price = ticker_data["Close"].mean()
    maxgap = (
        avg_price * 0.02
    )  # taking a range of 1% of the avg close price of the ticker for gap

    if len(support_levels) > 0:
        support_levels = average_levels(support_levels, maxgap)

    if len(resistance_levels) > 0:
        resistance_levels = average_levels(resistance_levels, maxgap)

    return support_levels, resistance_levels


def plot_support_resistance(st):
    DATA_UPDATED = False
    sandr_plot_size = State.state_add(st, "sandr_plot_size", "500px")
    sr_past_window_size = State.state_add(st, "sr_past_window_size ", 3)
    sr_future_window_size = State.state_add(st, "sr_future_window_size", 3)

    ticker_data = State.get(st, "ticker_data")
    ticker_data.rename(columns={"Date": "Datetime"}, inplace=True)
    ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
    plot_sizes = ["300px", "400px", "500px", "600px", "700px"]

    support_levels, resistance_levels = get_cleanted_levels(
        st, ticker_data, sr_past_window_size, sr_future_window_size
    )

    (sandr_col1, sandr_col2, sandr_col3, _, _) = st.columns(5)
    with sandr_col1:
        sandr_plot_size = st.selectbox(
            "plot size",
            index=plot_sizes.index(sandr_plot_size),
            options=plot_sizes,
            placeholder="Plot size",
            key="sandr_plot_size_key",
        )
        if sandr_plot_size:
            State.state_update(st, "sandr_plot_size", sandr_plot_size)

    with sandr_col2:
        sr_past_window_size_update = st.selectbox(
            "Back Candles",
            index=range(0, 200).index(sr_past_window_size),
            options=range(0, 200),
            placeholder="RSI Window",
            key="sr_past_window_size_key",
            help="3 yields best results",
        )
        if sr_past_window_size != sr_past_window_size_update:
            sr_past_window_size = sr_past_window_size_update
            State.state_update(st, "sr_past_window_size ", sr_past_window_size)
            ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
            support_levels, resistance_levels = get_cleanted_levels(
                st, ticker_data, sr_past_window_size, sr_future_window_size
            )
            DATA_UPDATED = True

    with sandr_col3:
        sr_future_window_size_update = st.selectbox(
            "Future Candles",
            index=range(0, 200).index(sr_future_window_size),
            options=range(0, 200),
            placeholder="RSI Window",
            key="sr_future_window_size_key",
            help="3 yields best results",
        )
        if sr_future_window_size != sr_future_window_size_update:
            sr_future_window_size = sr_future_window_size_update
            State.state_update(st, "sr_future_window_size", sr_future_window_size)
            ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
            support_levels, resistance_levels = get_cleanted_levels(
                st, ticker_data, sr_past_window_size, sr_future_window_size
            )
            DATA_UPDATED = True

    if not DATA_UPDATED:
        support_levels, resistance_levels = get_cleanted_levels(
            st, ticker_data, sr_past_window_size, sr_future_window_size
        )

    series = []

    candlestick_config = {
        "name": State.get(st, "ticker"),
        "type": "candlestick",
        "smooth": True,
        "position": "left",
        "data": ticker_data[["Open", "Close", "Low", "High"]].values.tolist(),
        "itemStyle": {
            "color": candlestick_down_color,
            "color0": candlestick_up_color,
            "borderColor": candlestick_down_border_color,
            "borderColor0": candlestick_up_border_color,
        },
    }
    series.append(candlestick_config)

    options = {
        "title": {"text": ""},
        "tooltip": {
            "show": False,  # disabling the data on hover in chart
        },
        "legend": {},
        "grid": {"left": "2%", "right": "5%", "bottom": "12%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "data": ticker_data["Datetime"].tolist(),
        },
        "yAxis": {
            "scale": True,
            "type": "value",
            "min": ticker_data["Close"].min(),
        },
        "dataZoom": [
            {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
            # {"type": "slider", "show": True, "yAxisIndex": [0], "start": 0, "end": 100},
            {
                "type": "inside",
                "xAxisIndex": [0],
                "start": 0,
                "end": 100,
            },  # This allows the chart to expand contract when scrolling inside the chart
            # {
            #     "type": "inside",
            #     "yAxisIndex": [0],
            #     "start": 0,
            #     "end": 100,
            # },  # This allows the chart to expand contract when scrolling inside the chart
        ],
    }

    # Plot support levels
    base_level_config = {
        "smooth": True,
        "position": "left",
        "data": [0, 0],
    }
    support_mark_line_data = []
    for level in support_levels:
        support_mark_line_data.append({"yAxis": level[1]})

    support_mark_line = {
        "data": support_mark_line_data,
        "lineStyle": {"color": candlestick_down_border_color},
        "silent": True,
    }
    support_series = candlestick_config.copy()
    support_series["name"] = "Support Levels"
    support_series["markLine"] = support_mark_line

    resistance_mark_line_data = []
    for level in resistance_levels:
        resistance_mark_line_data.append({"yAxis": level[1]})

    resistance_mark_line = {
        "data": resistance_mark_line_data,
        "lineStyle": {"color": candlestick_up_border_color},
        "silent": True,
    }
    resistance_series = candlestick_config.copy()
    resistance_series["name"] = "Resistance Levels"
    resistance_series["markLine"] = resistance_mark_line

    series.append(support_series)
    series.append(resistance_series)

    options["legend"] = {"data": "Support and Resistance"}
    # plotting the cadlesticks and any other lines/marks
    options["series"] = series

    st.subheader("Support and Resistance Levels")
    st_echarts(options=options, height=sandr_plot_size)
