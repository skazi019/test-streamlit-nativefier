"""
Follow https://echarts.apache.org/en/option.html#title for more configuration
"""
import pandas as pd
from state import State
from streamlit_echarts import st_echarts
from Core.technical_indicators import calculate_all_emas

from config import (
    candlestick_down_color,
    candlestick_down_border_color,
    candlestick_up_color,
    candlestick_up_border_color,
)


def plot_close_ema(st):
    ema_plot_size = State.state_add(st, "ema_plot_size", "500px")
    ticker_data = State.get(st, "ticker_data")
    ticker_data.rename(columns={"Date": "Datetime"}, inplace=True)
    ticker_data = calculate_all_emas(ticker_data)
    ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)

    options_yaxis_data = []
    legend = []
    for col in ticker_data.columns.tolist():
        if col.startswith("EMA_"):
            temp_yaxis_config = {
                "name": str(col),
                "type": "line",
                "data": ticker_data[col].fillna(0).tolist(),
                "lineStyle": {"opacity": 0.5},
                "smooth": True,
                "symbol": None,
                "alignTicks": True,
                "position": "right",
                "axisLine": {"show": True},
            }
            options_yaxis_data.append(temp_yaxis_config)
            legend.append(col)
            del temp_yaxis_config

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

    options_yaxis_data.insert(0, candlestick_config)

    options = {
        "title": {"text": ""},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross",
            },
        },
        "legend": {"data": legend},
        "grid": {"left": "2%", "right": "2%", "bottom": "12%", "containLabel": True},
        # "toolbox": {"feature": {"saveAsImage": {}}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ticker_data["Datetime"].tolist(),
            "axisline": {"onZero": False},
            "splitline": {"show": False},
        },
        "yAxis": {
            "scale": True,
            "type": "value",
            "min": ticker_data["Close"].min(),
        },
        "series": options_yaxis_data,
        "dataZoom": [
            {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
            {"type": "inside", "xAxisIndex": [0], "start": 0, "end": 100},
        ],
    }

    st.subheader("Close vs EMAs")
    ema_plot_size_col1, _ = st.columns([1, 4])
    with ema_plot_size_col1:
        plot_size_list = ["300px", "400px", "500px", "600px", "700px"]
        ema_plot_size = st.selectbox(
            "plot size",
            index=plot_size_list.index(ema_plot_size),
            options=plot_size_list,
            placeholder="Plot size",
            key="ema_plot_size_key",
        )
    st_echarts(options=options, height=ema_plot_size)
