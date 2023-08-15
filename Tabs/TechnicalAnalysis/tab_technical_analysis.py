from Tabs.TechnicalAnalysis.plot_close_ema import plot_close_ema
from Tabs.TechnicalAnalysis.plot_close_wma import plot_close_wma
from Tabs.TechnicalAnalysis.plot_stochrsi import plot_stochrsi
from Tabs.TechnicalAnalysis.plot_support_resistance import plot_support_resistance


def tab_technical_analysis(st):
    available_plots = {
        "Close vs EMAs(9, 21, 50, 90 ,200)": plot_close_ema,
        "Stochastic RSI": plot_stochrsi,
        "Close vs WMAs(9, 21, 50, 90 ,200)": plot_close_wma,
        "Support and Resistance": plot_support_resistance,
    }

    selected_plots = st.multiselect(
        label="Available plots for Technical Analysis:",
        options=available_plots.keys(),
        placeholder="Select option(s) to see plots below",
        default=["Support and Resistance"]
    )

    for plot in selected_plots:
        available_plots[plot](st)
