import pandas as pd
from state import State
from streamlit_echarts import st_echarts

from config import (
    candlestick_down_color,
    candlestick_down_border_color,
    candlestick_up_color,
    candlestick_up_border_color,
    candlestick_mark_color,
)


def plot_candlestick_pattern(st, ticker_data, name, mark_points, plot_size):
    # Converting ticker data Close to string to be able to plot mark points
    ticker_data["Close"] = ticker_data["Close"].astype(str)

    options_yaxis_data = []

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

    options = {
        "title": {"text": ""},
        "tooltip": {
            "trigger": "axis",
            "axisPointer": {
                "type": "cross",
            },
        },
        "legend": {},
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
        "dataZoom": [
            {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
            {"type": "inside", "xAxisIndex": [0], "start": 0, "end": 100},
        ],
    }

    candlestick_config["markPoint"] = {
        "name": name,
        "data": mark_points,
        "symbolSize": 30,
        "label": {"show": True},
        "itemStyle": {"color": candlestick_mark_color},
        "animation": False
    }

    options["legend"] = {"data": name}
    options["series"] = candlestick_config
    st.subheader(name)
    st_echarts(options=options, height=plot_size)
