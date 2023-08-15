import pandas as pd
from state import State
from streamlit_echarts import st_echarts
from talib import WMA

from config import (
    candlestick_down_color,
    candlestick_down_border_color,
    candlestick_up_color,
    candlestick_up_border_color,
)


def plot_close_wma(st):
    wma_plot_size = State.state_add(st, "wma_plot_size", "500px")
    ticker_data = State.get(st, "ticker_data")
    ticker_data.rename(columns={"Date": "Datetime"}, inplace=True)
    emas = [9, 21, 50, 90, 200]
    for ma in emas:
        ticker_data[f"WMA_{ma}"] = WMA(ticker_data["Close"], timeperiod=ma).round(2)
    ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)

    options_yaxis_series = []
    options_yaxis_data = []
    legend = []
    for col in ticker_data.columns.tolist():
        if col.startswith("WMA_"):
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
            options_yaxis_series.append(temp_yaxis_config)
            options_yaxis_data.append(
                {"name": str(col), "type": "value"},
            )
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

    # volume_config = (
    #     {
    #         "name": "Volume",
    #         "type": "bar",
    #         "position": "bottom",
    #         "data": ticker_data["Volume"].fillna(0).tolist(),
    #     },
    # )

    options_yaxis_series.insert(0, candlestick_config)
    options_yaxis_data.insert(
        0,
        {
            "name": "Close",
            "scale": True,
            "type": "value",
            "min": ticker_data["Close"].min(),
        },
    )
    # options_yaxis_series.append(volume_config)
    # options_yaxis_data.append({"name": "Volume", "type": "value"})

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
        "yAxis": options_yaxis_data,
        "series": options_yaxis_series,
        "dataZoom": [
            {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
            {"type": "inside", "xAxisIndex": [0], "start": 0, "end": 100},
        ],
    }

    st.subheader("Close vs WMAs")
    wma_plot_size_col1, _ = st.columns([1, 4])
    with wma_plot_size_col1:
        plot_size_list = ["300px", "400px", "500px", "600px", "700px"]
        wma_plot_size = st.selectbox(
            "plot size",
            index=plot_size_list.index(wma_plot_size),
            options=plot_size_list,
            placeholder="Plot size",
            key="wma_plot_size_key",
        )
    st_echarts(options=options, height=wma_plot_size)
