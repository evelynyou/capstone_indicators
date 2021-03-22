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
    # Add all features

    # Daily return based on Close price
    df["Return"] = df["Close"] - df["Close"].shift(1)
    df["Return%"] = df["Return"] / df["Close"].shift(1)

    # Last 5 day return based on Close price
    df["L5D_Return"] = df["Close"] - df["Close"].shift(5)
    df["L5D_Return%"] = df["L5D_Return"] / df["Close"].shift(5)

    # Next 5 day return based on Close price
    df["N5D_Return"] = (df["Close"] - df["Close"].shift(-5)) * -1
    df["N5D_Return%"] = df["N5D_Return"] / df["Close"]

    # Next 5 day return based on Open price next day
    df["N5D_Return_Delayed"] = (df["Open"].shift(-1) - df["Close"].shift(-5)) * -1
    df["N5D_Return_Delayed%"] = df["N5D_Return_Delayed"] / df["Open"].shift(-1)

    # Close price as a % of 52-Week high and low
    df["52Wk_High"] = df["Close"].rolling(min_periods=252, window=252).max()
    df["52Wk_Low"] = df["Close"].rolling(min_periods=252, window=252).min()
    df["%52Wk_High"] = df["Close"] / df["52Wk_High"]
    df["%52Wk_Low"] = df["Close"] / df["52Wk_Low"]

    # Open price as a % of prior Close
    df["Open%PriorClose"] = df["Open"] / df["Close"].shift(1)

    # Close price as a % of Open, High, and Low
    df["Close%Open"] = df["Close"] / df["Open"]
    df["Close%High"] = df["Close"] / df["High"]
    df["Close%Low"] = df["Close"] / df["Low"]

    # Dividend as a % of Close
    df["Div%Close"] = df["Dividends"] / df["Close"]

    # Volume as a % of 52-Week average volume
    df["52Wk_Avg_Volume"] = df["Volume"].rolling(min_periods=252, window=252).mean()
    df["%52Wk_Avg_Volume"] = df["Volume"] / df["52Wk_Avg_Volume"]

    # Add simple moving averages (SMAs)
    df["SMA3"] = SMA(df.Close, 3)
    df["SMA5"] = SMA(df.Close, 5)
    df["SMA10"] = SMA(df.Close, 10)
    df["SMA15"] = SMA(df.Close, 15)
    df["SMA20"] = SMA(df.Close, 20)
    df["SMA30"] = SMA(df.Close, 30)
    df["SMA50"] = SMA(df.Close, 50)

    # Standardized % above or below simple trading averages
    df["SMA3%"] = df["Close"] / df["SMA3"] - 1
    df["SMA5%"] = df["Close"] / df["SMA5"] - 1
    df["SMA10%"] = df["Close"] / df["SMA10"] - 1
    df["SMA15%"] = df["Close"] / df["SMA15"] - 1
    df["SMA20%"] = df["Close"] / df["SMA20"] - 1
    df["SMA30%"] = df["Close"] / df["SMA30"] - 1
    df["SMA50%"] = df["Close"] / df["SMA50"] - 1

    # Add exponential moving averages (EMAs)
    # More info: https://www.investopedia.com/terms/e/ema.asp
    df["EMA3"] = EMA(df.Close, 3)
    df["EMA5"] = EMA(df.Close, 5)
    df["EMA10"] = EMA(df.Close, 10)
    df["EMA15"] = EMA(df.Close, 15)
    df["EMA20"] = EMA(df.Close, 20)
    df["EMA30"] = EMA(df.Close, 30)
    df["EMA50"] = EMA(df.Close, 50)

    # Standardized % above or below exponential trading averages
    df["EMA3%"] = df["Close"] / df["EMA3"] - 1
    df["EMA5%"] = df["Close"] / df["EMA5"] - 1
    df["EMA10%"] = df["Close"] / df["EMA10"] - 1
    df["EMA15%"] = df["Close"] / df["EMA15"] - 1
    df["EMA20%"] = df["Close"] / df["EMA20"] - 1
    df["EMA30%"] = df["Close"] / df["EMA30"] - 1
    df["EMA50%"] = df["Close"] / df["EMA50"] - 1

    # Add pivot point (PP) and classical support and resistance pivot points
    # More info: https://www.investopedia.com/terms/p/pivotpoint.asp
    df["PP"] = (df.High + df.Low + df.Close) / 3
    df["S1C"] = df.PP * 2 - df.High
    df["S2C"] = df.PP - (df.High - df.Low)
    df["S3C"] = df.Low - 2 * (df.High - df.PP)
    df["R1C"] = df.PP * 2 - df.Low 
    df["R2C"] = df.PP + (df.High - df.Low)
    df["R3C"] = df.High + 2 * (df.PP - df.Low)

    # Standardized % above or below classical pivot points
    df["PP%"] = df["Close"] / df["PP"] - 1
    df["S1C%"] = df["Close"] / df["S1C"] - 1
    df["S2C%"] = df["Close"] / df["S2C"] - 1
    df["S3C%"] = df["Close"] / df["S3C"] - 1
    df["R1C%"] = df["Close"] / df["R1C"] - 1
    df["R2C%"] = df["Close"] / df["R2C"] - 1
    df["R3C%"] = df["Close"] / df["R3C"] - 1

    # Add Fibonacci support and resistance pivot points
    # More info: https://www.interactivebrokers.com/en/software/tws/usersguidebook/technicalanalytics/fibonaccipivotpoints.htm
    df["S1F"] = df.PP - 0.382 * (df.High - df.Low)
    df["S2F"] = df.PP - 0.618 * (df.High - df.Low)
    df["S3F"] = df.PP - 1.0 * (df.High - df.Low)
    df["R1F"] = df.PP + 0.382 * (df.High - df.Low)
    df["R2F"] = df.PP + 0.618 * (df.High - df.Low)
    df["R3F"] = df.PP + 1.0 * (df.High - df.Low)

    # Standardized % above or Fibonacci classical pivot points
    df["S1F%"] = df["Close"] / df["S1F"] - 1
    df["S2F%"] = df["Close"] / df["S2F"] - 1
    df["S3F%"] = df["Close"] / df["S3F"] - 1
    df["R1F%"] = df["Close"] / df["R1F"] - 1
    df["R2F%"] = df["Close"] / df["R2F"] - 1
    df["R3F%"] = df["Close"] / df["R3F"] - 1

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
                         fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    overbought = 80
    oversold = 20
    buy_signal = pd.Series(slowk <= oversold).astype(int) + pd.Series(slowd <= oversold).astype(int)
    sell_signal = pd.Series(slowk >= overbought).astype(int) * -1 + pd.Series(slowd >= overbought).astype(int) * -1
    stoch_signal = buy_signal + sell_signal
    df["Slow_K"] = slowk
    df["Slow_D"] = slowd
    df["Stoch_Osci"] = stoch_signal.values

    # Add Stochastic RSI levels
    fastk, fastd = STOCHRSI(df.Close, timeperiod=14, fastk_period=14, fastd_period=3, fastd_matype=0)
    overbought = 80
    oversold = 20
    buy_signal = pd.Series(fastk <= oversold).astype(int) + pd.Series(fastd <= oversold).astype(int)
    sell_signal = pd.Series(fastk >= overbought).astype(int) * -1 + pd.Series(fastd >= overbought).astype(int) * -1
    stoch_signal = buy_signal + sell_signal
    df["Fast_K"] = fastk
    df["Fast_D"] = fastd
    df["Stoch_RSI"] = stoch_signal.values    
    
    return df
