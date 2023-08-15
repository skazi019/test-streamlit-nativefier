"""
Follow https://echarts.apache.org/en/option.html#title for more configuration
"""
import pandas as pd
from state import State
from streamlit_echarts import st_echarts
from ta.momentum import StochRSIIndicator


def plot_stochrsi(st):
    DATA_UPDATED = False
    rsi_plot_size = State.state_add(st, "rsi_plot_size", "400px")
    rsi_window = State.state_add(st, "rsi_window", 14)
    rsi_smooth_1 = State.state_add(st, "rsi_smooth_1", 3)
    rsi_smooth_2 = State.state_add(st, "rsi_smooth_2", 3)

    ticker_data = State.get(st, "ticker_data")
    ticker_data.rename(columns={"Date": "Datetime"}, inplace=True)

    st.subheader("Stochastic RSI")
    (
        ema_plot_size_col1,
        ema_plot_size_col2,
        ema_plot_size_col3,
        ema_plot_size_col4,
        ema_plot_size_col5,
    ) = st.columns(5)
    with ema_plot_size_col1:
        rsi_plot_size = st.selectbox(
            "plot size",
            index=2,
            options=["300px", "400px", "500px", "600px", "700px"],
            placeholder="Plot size",
            key="rsi_plot_size_key",
        )
        if rsi_plot_size:
            State.state_update(st, "rsi_plot_size", rsi_plot_size)
    with ema_plot_size_col2:
        rsi_window_update = st.selectbox(
            "RSI Window",
            index=rsi_window - 2,
            options=range(2, 200),
            placeholder="RSI Window",
            key="rsi_window_key",
            help="Please select this option twice, for some reason selecting one time doesn't trigger reload",
        )
        if rsi_window != rsi_window_update:
            rsi_window = rsi_window_update
            State.state_update(st, "rsi_window", rsi_window)
            ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
            indicator_stoch_rsi = StochRSIIndicator(
                close=ticker_data["Close"],
                window=rsi_window,
                smooth1=rsi_smooth_1,
                smooth2=rsi_smooth_2,
            )
            ticker_data["S.RSI"] = indicator_stoch_rsi.stochrsi()
            DATA_UPDATED = True
            st.experimental_rerun()

    with ema_plot_size_col3:
        rsi_smooth_1_update = st.selectbox(
            "RSI Smooth 1",
            index=2,
            options=range(2, 200),
            placeholder="RSI Window",
            key="rsi_smooth1_key",
        )
        if rsi_smooth_1 != rsi_smooth_1_update:
            rsi_smooth_1 = rsi_smooth_1_update
            State.state_update(st, "rsi_smooth_1", rsi_smooth_1)
            ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
            indicator_stoch_rsi = StochRSIIndicator(
                close=ticker_data["Close"],
                window=rsi_window,
                smooth1=rsi_smooth_1,
                smooth2=rsi_smooth_2,
            )
            ticker_data["S.RSI"] = indicator_stoch_rsi.stochrsi()
            DATA_UPDATED = True
            st.experimental_rerun()

    with ema_plot_size_col4:
        rsi_smooth_2_update = st.selectbox(
            "RSI Smooth 2",
            index=2,
            options=range(2, 200),
            placeholder="RSI Window",
            key="rsi_smooth2_key",
        )
        if rsi_smooth_2 != rsi_smooth_2_update:
            rsi_smooth_2 = rsi_smooth_2_update
            State.state_update(st, "rsi_smooth_2", rsi_smooth_2)
            ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
            indicator_stoch_rsi = StochRSIIndicator(
                close=ticker_data["Close"],
                window=rsi_window,
                smooth1=rsi_smooth_1,
                smooth2=rsi_smooth_2,
            )
            ticker_data["S.RSI"] = indicator_stoch_rsi.stochrsi()
            DATA_UPDATED = True
            st.experimental_rerun()

    if not DATA_UPDATED:
        ticker_data["Datetime"] = ticker_data["Datetime"].astype(str)
        indicator_stoch_rsi = StochRSIIndicator(
            close=ticker_data["Close"],
            window=rsi_window,
            smooth1=rsi_smooth_1,
            smooth2=rsi_smooth_2,
        )
        ticker_data["S.RSI"] = indicator_stoch_rsi.stochrsi()

    ticker_data["S.RSI"] = (ticker_data["S.RSI"]*100).round(2)

    options = {
        "title": {"text": ""},
        "tooltip": {
            "trigger": "axis",
        },
        "legend": {"data": ["Close", "Stochastic RSI"]},
        "grid": {"left": "1%", "right": "1%", "bottom": "10%", "containLabel": True},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": ticker_data["Datetime"].tolist(),
        },
        "yAxis": [
            # {"name": "Close", "type": "value", "min": ticker_data["Close"].min()},
            {"name": "Stochastic RSI", "type": "value", "min": 0, "max": 100},
            # {"name": "Volume", "type": "value"},
        ],
        "series": [
            # {
            #     "name": "Close",
            #     "type": "line",
            #     "data": ticker_data["Close"].fillna(0).tolist(),
            #     "alignTicks": True,
            #     "yAxisIndex": 0,
            # },
            {
                "name": "S.RSI",
                "type": "line",
                "data": ticker_data["S.RSI"].fillna(0).tolist(),
                "alignTicks": True,
                "yAxisIndex": 0,
            },
            # {
            #     "name": "Volume",
            #     "type": "bar",
            #     "position": "right",
            #     "data": ticker_data["Volume"].fillna(0).tolist(),
            #     "alignTicks": True,
            #     "yAxisIndex": 2,
            # },
        ],
        "dataZoom": [
            {"type": "slider", "show": True, "xAxisIndex": [0], "start": 0, "end": 100},
            {"type": "inside", "xAxisIndex": [0], "start": 0, "end": 100},
        ],
    }

    st_echarts(options=options, height=rsi_plot_size)
