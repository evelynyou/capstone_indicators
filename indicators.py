from talib import abstract
import numpy as np

# directly import base indicators
SMA = abstract.SMA
EMA = abstract.EMA
MACD = abstract.MACD
RSI = abstract.RSI
STOCH = abstract.STOCH
STOCHRSI = abstract.STOCHRSI

def modCloseStrategy(strategy, close, *args):
    converted = []
    for arg in args:
        if np.issubdtype(arg, np.integer):
            converted.append(arg.item())
    return strategy(close, *converted)

def modHLCStrategy(strategy, high, low, close, *args):
    converted = []
    for arg in args:
        if np.issubdtype(arg, np.integer):
            converted.append(arg.item())
    return strategy(high, low, close, *converted)
