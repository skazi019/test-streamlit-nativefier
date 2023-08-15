def isEngulfing(l, open, close, high, low, bodydiff, highdiff, lowdiff, ratio1, ratio2):
    row = l
    bodydiff[row] = abs(open[row] - close[row])
    if bodydiff[row] < 0.000001:
        bodydiff[row] = 0.000001

    bodydiffmin = 0.002
    if (
        bodydiff[row] > bodydiffmin
        and bodydiff[row - 1] > bodydiffmin
        and open[row - 1] < close[row - 1]
        and open[row] > close[row]
        and (open[row] - close[row - 1]) >= -0e-5
        and close[row] < open[row - 1]
    ):  # +0e-5 -5e-5
        return 1

    elif (
        bodydiff[row] > bodydiffmin
        and bodydiff[row - 1] > bodydiffmin
        and open[row - 1] > close[row - 1]
        and open[row] < close[row]
        and (open[row] - close[row - 1]) <= +0e-5
        and close[row] > open[row - 1]
    ):  # -0e-5 +5e-5
        return 2
    else:
        return 0


def isStar(l, open, close, high, low, bodydiff, highdiff, lowdiff, ratio1, ratio2):
    bodydiffmin = 0.0020
    row = l
    highdiff[row] = high[row] - max(open[row], close[row])
    lowdiff[row] = min(open[row], close[row]) - low[row]
    bodydiff[row] = abs(open[row] - close[row])
    if bodydiff[row] < 0.000001:
        bodydiff[row] = 0.000001
    ratio1[row] = highdiff[row] / bodydiff[row]
    ratio2[row] = lowdiff[row] / bodydiff[row]

    if (
        ratio1[row] > 1
        and lowdiff[row] < 0.2 * highdiff[row]
        and bodydiff[row] > bodydiffmin
    ):  # and open[row]>close[row]):
        return 1
    elif (
        ratio2[row] > 1
        and highdiff[row] < 0.2 * lowdiff[row]
        and bodydiff[row] > bodydiffmin
    ):  # and open[row]<close[row]):
        return 2
    else:
        return 0
