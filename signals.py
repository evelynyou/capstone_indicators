import numpy as np
import pandas as pd
from talib import abstract

# directly import strategies
SMA = abstract.SMA
EMA = abstract.EMA
MACD = abstract.MACD
RSI = abstract.RSI
STOCH = abstract.STOCH
STOCHRSI = abstract.STOCHRSI


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    this is a temp function that generates all the singals for an OHLCV dataframe
    input: OHLCV dataframe
    output: OHLCV dataframe with signals
    """
    # Adding Return Data
    # Daily return based on Close price
    df["Return"] = df["Close"] - df["Close"].shift(1)
    df["Return%"] = df["Return"] / df["Close"]
    # Next 5 day return based on Close price
    df["N5D_Return"] = (df["Close"] - df["Close"].shift(-5)) * -1
    df["N5D_Return%"] = df["N5D_Return"] / df["Close"]

    # Adding Common TA levels/signals
    # Add simple moving averages (SMAs)
    df["SMA3"] = SMA(df.Close, 3)
    df["SMA5"] = SMA(df.Close, 5)
    df["SMA10"] = SMA(df.Close, 10)
    df["SMA15"] = SMA(df.Close, 15)
    df["SMA20"] = SMA(df.Close, 20)
    df["SMA30"] = SMA(df.Close, 30)
    df["SMA50"] = SMA(df.Close, 50)
    # Add exponential moving averages (EMAs)
    # More info: https://www.investopedia.com/terms/e/ema.asp
    df["EMA3"] = EMA(df.Close, 3)
    df["EMA5"] = EMA(df.Close, 5)
    df["EMA10"] = EMA(df.Close, 10)
    df["EMA15"] = EMA(df.Close, 15)
    df["EMA20"] = EMA(df.Close, 20)
    df["EMA30"] = EMA(df.Close, 30)
    df["EMA50"] = EMA(df.Close, 50)
    # Add pivot point (PP) and classical support and resistance pivot points
    # More info: https://www.investopedia.com/terms/p/pivotpoint.asp
    df["PP"] = (df.High + df.Low + df.Close) / 3
    df["S1C"] = df.PP * 2 - df.High
    df["S2C"] = df.PP - (df.High - df.Low)
    df["S3C"] = df.Low - 2 * (df.High - df.PP)
    df["R1C"] = df.PP * 2 - df.Low 
    df["R2C"] = df.PP + (df.High - df.Low)
    df["R3C"] = df.High + 2 * (df.PP - df.Low)
    # Add Fibonacci support and resistance pivot points
    # More info: https://www.interactivebrokers.com/en/software/tws/usersguidebook/technicalanalytics/fibonaccipivotpoints.htm
    df["S1F"] = df.PP - 0.382 * (df.High - df.Low)
    df["S2F"] = df.PP - 0.618 * (df.High - df.Low)
    df["S3F"] = df.PP - 1.0 * (df.High - df.Low)
    df["R1F"] = df.PP + 0.382 * (df.High - df.Low)
    df["R2F"] = df.PP + 0.618 * (df.High - df.Low)
    df["R3F"] = df.PP + 1.0 * (df.High - df.Low)

    # Add SMA Crossing Signal
    sma_fast = SMA(df.Close, 3)
    sma_slow = SMA(df.Close, 15)
    sma_signal = pd.Series(sma_fast > sma_slow).astype(int).diff().fillna(0)
    df["SMA_Signal"] = sma_signal.values
    # Add MACD Signal
    macd, macdsignal, macdhist = MACD(df.Close, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_signal = pd.Series(macd > macdsignal).astype(int).diff().fillna(0)
    df["MACD_Signal"] = macd_signal.values
    # Add RSI Level and Signal
    real = RSI(df.Close, timeperiod=14)
    df["RSI"] = real
    overbought = 70
    oversold = 30
    buy_signal = pd.Series(real <= oversold).astype(int)
    sell_signal = pd.Series(real >= overbought).astype(int) * -1
    rsi_signal = buy_signal + sell_signal
    df["RSI_Signal"] = rsi_signal.values
    # Add Stochastic Oscillator levels
    slowk, slowd = STOCH(df.High, df.Low, df.Close, 
                         fastk_period=5, slowk_period=3, 
                         slowk_matype=0, slowd_period=3, slowd_matype=0)
    overbought = 80
    oversold = 20
    buy_signal = pd.Series(slowk <= oversold).astype(int) + pd.Series(slowd <= oversold).astype(int)
    sell_signal = pd.Series(slowk >= overbought).astype(int) * -1 + pd.Series(slowd >= overbought).astype(int) * -1
    stoch_signal = buy_signal + sell_signal
    df["Slow_K"] = slowk
    df["Slow_D"] = slowd
    df["Stoch_Osci"] = stoch_signal.values
    # Add Stochastic RSI levels
    fastk, fastd = STOCHRSI(df.Close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
    overbought = 80
    oversold = 20
    buy_signal = pd.Series(fastk <= oversold).astype(int) + pd.Series(fastd <= oversold).astype(int)
    sell_signal = pd.Series(fastk >= overbought).astype(int) * -1 + pd.Series(fastd >= overbought).astype(int) * -1
    stoch_signal = buy_signal + sell_signal
    df["Fast_K"] = fastk
    df["Fast_D"] = fastd
    df["Stoch_RSI"] = stoch_signal.values
    return df
