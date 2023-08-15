"""
If TA-Lib is installed successfully and you still cannot import talib successfully then follow below link:
    https://stackoverflow.com/questions/66687712/modulenotfounderror-no-module-named-talib answer with tar unzip

Steps to install Ta-Lib in a virutal environment:
    Step 1: Install TA-Lib for your OS; for mac it is `brew install ta-lib`. 
        check https://ta-lib.github.io/ta-lib-python/install.html for more details
    Step 2: Download the tar or zip from the link in Step 1 and unzip it in your project folder anywhere
    Step 3: Make sure your virutal environment is active
    Step 4: verify that the commands python and pip are using your virtual env's instances 
        and not global python and pip instances by using command which python && which pip
    Step 5: cd into the extracted TA-Lib folder in Step 2
    Step 6: run command pip install -r requirements.txt
    Step 7: run command python setup.py install
    Step 8: Verify Ta-lib has been installed in the virtual env by opening python shell and typing import talib
"""
import talib


def get_all_candlestick_patterns():
    all_candlestick_patterns = {
        "Two Crows": talib.CDL2CROWS,
        "Three Black Crows": talib.CDL3BLACKCROWS,
        "Three Inside Up/Down": talib.CDL3INSIDE,
        "Three-Line Strike": talib.CDL3LINESTRIKE,
        "Three Outside Up/Down": talib.CDL3OUTSIDE,
        "Three Stars In The South": talib.CDL3STARSINSOUTH,
        "Three Advancing White Soldiers": talib.CDL3WHITESOLDIERS,
        "Abandoned Baby": talib.CDLABANDONEDBABY,
        "Advance Block": talib.CDLADVANCEBLOCK,
        "Belt-hold": talib.CDLBELTHOLD,
        "Breakaway": talib.CDLBREAKAWAY,
        "Closing Marubozu": talib.CDLCLOSINGMARUBOZU,
        "Concealing Baby Swallow": talib.CDLCONCEALBABYSWALL,
        "Counterattack": talib.CDLCOUNTERATTACK,
        "Dark Cloud Cover": talib.CDLDARKCLOUDCOVER,
        "Doji": talib.CDLDOJI,
        "Doji Star": talib.CDLDOJISTAR,
        "Dragonfly Doji": talib.CDLDRAGONFLYDOJI,
        "Engulfing Pattern": talib.CDLENGULFING,
        "Evening Doji Star": talib.CDLEVENINGDOJISTAR,
        "Evening Star": talib.CDLEVENINGSTAR,
        "Up/Down-gap side-by-side white lines": talib.CDLGAPSIDESIDEWHITE,
        "Gravestone Doji": talib.CDLGRAVESTONEDOJI,
        "Hammer": talib.CDLHAMMER,
        "Hanging Man": talib.CDLHANGINGMAN,
        "Harami Pattern": talib.CDLHARAMI,
        "Harami Cross Pattern": talib.CDLHARAMICROSS,
        "High-Wave Candle": talib.CDLHIGHWAVE,
        "Hikkake Pattern": talib.CDLHIKKAKE,
        "Modified Hikkake Pattern": talib.CDLHIKKAKEMOD,
        "Homing Pigeon": talib.CDLHOMINGPIGEON,
        "Identical Three Crows": talib.CDLIDENTICAL3CROWS,
        "In-Neck Pattern": talib.CDLINNECK,
        "Inverted Hammer": talib.CDLINVERTEDHAMMER,
        "Kicking": talib.CDLKICKING,
        "Kicking - bull/bear determined by the longer marubozu": talib.CDLKICKINGBYLENGTH,
        "Ladder Bottom": talib.CDLLADDERBOTTOM,
        "Long Legged Doji": talib.CDLLONGLEGGEDDOJI,
        "Long Line Candle": talib.CDLLONGLINE,
        "Marubozu": talib.CDLMARUBOZU,
        "Matching Low": talib.CDLMATCHINGLOW,
        "Mat Hold": talib.CDLMATHOLD,
        "Morning Doji Star": talib.CDLMORNINGDOJISTAR,
        "Morning Star": talib.CDLMORNINGSTAR,
        "On-Neck Pattern": talib.CDLONNECK,
        "Piercing Pattern": talib.CDLPIERCING,
        "Rickshaw Man": talib.CDLRICKSHAWMAN,
        "Rising/Falling Three Methods": talib.CDLRISEFALL3METHODS,
        "Separating Lines": talib.CDLSEPARATINGLINES,
        "Shooting Star": talib.CDLSHOOTINGSTAR,
        "Short Line Candle": talib.CDLSHORTLINE,
        "Spinning Top": talib.CDLSPINNINGTOP,
        "Stalled Pattern": talib.CDLSTALLEDPATTERN,
        "Stick Sandwich": talib.CDLSTICKSANDWICH,
        "Takuri (Dragonfly Doji with very long lower shadow)": talib.CDLTAKURI,
        "Tasuki Gap": talib.CDLTASUKIGAP,
        "Thrusting Pattern": talib.CDLTHRUSTING,
        "Tristar Pattern": talib.CDLTRISTAR,
        "Unique 3 River": talib.CDLUNIQUE3RIVER,
        "Upside Gap Two Crows": talib.CDLUPSIDEGAP2CROWS,
        "Upside/Downside Gap Three Methods": talib.CDLXSIDEGAP3METHODS,
    }

    return all_candlestick_patterns
