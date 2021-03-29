from talib import abstract
import numpy as np

# directly import base indicators
SMA = abstract.SMA
EMA = abstract.EMA
MACD = abstract.MACD
RSI = abstract.RSI
STOCH = abstract.STOCH
STOCHRSI = abstract.STOCHRSI

LR_SIGNAL = lambda data: data['LR_Signal']

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

def LR_SIGNAL(data):
    return data['LR_Signal']

def ARIMA_SIGNAL(data):
    return data['Arima_Signal']
