"""
Support and Resistance from - https://www.youtube.com/watch?v=aJ8Og-iLaas&t=295s
"""
import numpy as np
import pandas as pd
from Tabs.TechnicalAnalysis.CustomStrategies.cndl_patterns import isEngulfing, isStar


def average_levels(data, maxgap):
    """Arrange data into groups where successive elements
    differ by no more than *maxgap*

     >>> cluster([1, 6, 9, 100, 102, 105, 109, 134, 139], maxgap=10)
     [[1, 6, 9], [100, 102, 105, 109], [134, 139]]

     >>> cluster([1, 6, 9, 99, 100, 102, 105, 134, 139, 141], maxgap=10)
     [[1, 6, 9], [99, 100, 102, 105], [134, 139, 141]]

    Args:
        data: would be a list of levels(Support/Resistance)
            level: [["date", value, "S"/"R"], ["date", value, "S"/"R"], ..]

        maxgap: range for grouping the values

    Returns:
        Return levels with each group averaged out to make a single level

    """
    data.sort(key=lambda x: x[1]) # sorting all the levels based on the value of the level which is the 2nd element of 3 element tuple
    groups = [[data[0]]]
    for x in data[1:]:
        if abs(x[1] - groups[-1][-1][1]) <= maxgap:
            groups[-1].append(x)
        else:
            groups.append([x])

    new_levels = []
    for group in groups:
        average_value = np.mean(list(zip(*group))[1])
        new_levels.append((group[0][0], average_value, group[0][2]))

    return new_levels


def support(df: pd.DataFrame, l, n1: int, n2: int):  # n1 n2 before and after candle l
    """
    This function finds whether the current candle in question is near a support level

    Args:
        df: The entire ticker data containing High, Low, Open, Close for a candlestic
        l: The current candlestick
        n1: How many candlestick to check for in the Past, before the current candlestick
        n2: How many candlestick to check for in the future, after the current candlestick

    Returns:
        1 if it's a support level else 0

    """
    for i in range(l - n1 + 1, l + 1):
        if df.Low[i] > df.Low[i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if df.Low[i] < df.Low[i - 1]:
            return 0
    return 1


def resistance(
    df: pd.DataFrame, l, n1: int, n2: int
):  # n1 n2 before and after candle l
    """
    This function finds whether the current candle in question is near a resistance level

    Args:
        df: The entire ticker data containing High, Low, Open, Close for a candlestic
        l: The current candlestick
        n1: How many candlestick to check for in the Past, before the current candlestick
        n2: How many candlestick to check for in the future, after the current candlestick

    Returns:
        1 if it's a resistance level else 0

    """
    for i in range(l - n1 + 1, l + 1):
        if df.High[i] < df.High[i - 1]:
            return 0
    for i in range(l + 1, l + n2 + 1):
        if df.High[i] > df.High[i - 1]:
            return 0
    return 1


def get_support_resistance_levels(st, df: pd.DataFrame, n1: int, n2: int):
    """

    Args:
        df: ticker data containing High, Open, Low, Close column values
        n1: How many candlestick to check for in the Past, before the current candlestick
        n2: How many candlestick to check for in the future, after the current candlestick

    Returns:
        List of tuples
        tuple - (candle index, High/Low value depending on the Resistance/Support, Resistance/Support)
    """
    support_levels = []
    resistance_levels = []

    for rowIndex in range(len(df)):
        try:
            if n1 > rowIndex:
                n1_temp = rowIndex
            else:
                n1_temp = n1

            if n2 + rowIndex >= len(df):
                n2_temp = len(df) - rowIndex
            else:
                n2_temp = n2

            if support(df, rowIndex, n1_temp, n2_temp):
                support_levels.append(
                    (df["Datetime"][rowIndex], df["Low"][rowIndex], "S")
                )

            if resistance(df, rowIndex, n1_temp, n2_temp):
                resistance_levels.append(
                    (df["Datetime"][rowIndex], df["High"][rowIndex], "R")
                )
        except KeyError:
            # st.write(f"Key error | rowIndex: {rowIndex} | len of df: {len(df)}")
            # st.write(f"n1_temp: {n1_temp} | n2_temp: {n2_temp}")
            pass

    return support_levels, resistance_levels


def closeResistance(l, levels, lim):
    if len(levels) == 0:
        return 0
    c1 = abs(df.high[l] - min(levels, key=lambda x: abs(x - df.high[l]))) <= lim
    c2 = (
        abs(
            max(df.open[l], df.close[l])
            - min(levels, key=lambda x: abs(x - df.high[l]))
        )
        <= lim
    )
    c3 = min(df.open[l], df.close[l]) < min(levels, key=lambda x: abs(x - df.high[l]))
    c4 = df.low[l] < min(levels, key=lambda x: abs(x - df.high[l]))
    if (c1 or c2) and c3 and c4:
        return 1
    else:
        return 0


def closeSupport(l, levels, lim):
    if len(levels) == 0:
        return 0
    c1 = abs(df.low[l] - min(levels, key=lambda x: abs(x - df.low[l]))) <= lim
    c2 = (
        abs(
            min(df.open[l], df.close[l]) - min(levels, key=lambda x: abs(x - df.low[l]))
        )
        <= lim
    )
    c3 = max(df.open[l], df.close[l]) > min(levels, key=lambda x: abs(x - df.low[l]))
    c4 = df.high[l] > min(levels, key=lambda x: abs(x - df.low[l]))
    if (c1 or c2) and c3 and c4:
        return 1
    else:
        return 0


def mytarget(barsupfront, df1):
    length = len(df1)
    high = list(df1["high"])
    low = list(df1["low"])
    close = list(df1["close"])
    open = list(df1["open"])
    signal = list(df1["signal"])
    trendcat = [0] * length
    amount = [0] * length
    SLTPRatio = 1.1  # TP/SL Ratio

    SL = 0
    TP = 0
    for line in range(backCandles, length - barsupfront - n2):
        if signal[line] == 1:
            SL = max(high[line - 1 : line + 1])  #!!!!! parameters
            TP = close[line] - SLTPRatio * (SL - close[line])
            for i in range(1, barsupfront + 1):
                if low[line + i] <= TP and high[line + i] >= SL:
                    trendcat[line] = 3
                    break
                elif low[line + i] <= TP:
                    trendcat[line] = 1  # win trend 1 in signal 1
                    amount[line] = close[line] - low[line + i]
                    break
                elif high[line + i] >= SL:
                    trendcat[line] = 2  # loss trend 2 in signal 1
                    amount[line] = close[line] - high[line + i]
                    break

        if signal[line] == 2:
            SL = min(low[line - 1 : line + 1])  #!!!!! parameters
            TP = close[line] + SLTPRatio * (close[line] - SL)

            for i in range(1, barsupfront + 1):
                if high[line + i] >= TP and low[line + i] <= SL:
                    trendcat[line] = 3
                    break
                elif high[line + i] >= TP:
                    trendcat[line] = 2  # win trend 2 in signal 2
                    amount[line] = high[line + i] - close[line]
                    break
                elif low[line + i] <= SL:
                    trendcat[line] = 1  # loss trend 1 in signal 2
                    amount[line] = low[line + i] - close[line]
                    break
    # return trendcat
    return amount


def get_price_action(df):
    length = len(df)
    high = list(df["high"])
    low = list(df["low"])
    close = list(df["close"])
    open = list(df["open"])

    bodydiff = [0] * length
    highdiff = [0] * length
    lowdiff = [0] * length
    ratio1 = [0] * length
    ratio2 = [0] * length

    SLTPRatio = 1.1  # TP/SL Ratio

    n1 = 2
    n2 = 2
    backCandles = 45
    signal = [0] * length

    for row in range(backCandles, len(df) - n2):
        ss = []
        rr = []
        for subrow in range(row - backCandles + n1, row + 1):
            if support(df, subrow, n1, n2):
                ss.append(df.low[subrow])
            if resistance(df, subrow, n1, n2):
                rr.append(df.high[subrow])
        #!!!! parameters
        if (
            isEngulfing(
                row, open, close, high, low, bodydiff, highdiff, lowdiff, ratio1, ratio2
            )
            == 1
            or isStar(
                row, open, close, high, low, bodydiff, highdiff, lowdiff, ratio1, ratio2
            )
            == 1
        ) and closeResistance(
            row, rr, 150e-5
        ):  # and df.RSI[row]<30
            signal[row] = 1
        elif (
            isEngulfing(
                row, open, close, high, low, bodydiff, highdiff, lowdiff, ratio1, ratio2
            )
            == 2
            or isStar(
                row, open, close, high, low, bodydiff, highdiff, lowdiff, ratio1, ratio2
            )
            == 2
        ) and closeSupport(
            row, ss, 150e-5
        ):  # and df.RSI[row]>70
            signal[row] = 2
        else:
            signal[row] = 0
