import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import datetime

import yfinance as yf
from talib import abstract

from backtesting import Strategy, Backtest
from backtesting.lib import crossover

# SK-learn libraries for data processing and learning
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB

# SK-learn libraries for evaluation.
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

# directly import strategies
SMA = abstract.SMA
EMA = abstract.EMA
MACD = abstract.MACD
RSI = abstract.RSI
STOCH = abstract.STOCH
STOCHRSI = abstract.STOCHRSI


def add_features(data):
    """Add all features needed to a dataset for the logistic regression model"""
    df = data.copy()
    
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
    # More info: https://www.interactivebrokers.com/en/software/tws/usersguidebook/
    #technicalanalytics/fibonaccipivotpoints.htm
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
	

def normalize_features(df):
    """Get the normalized features from the data frame"""
    
    # Only use standardized features for model
    data = df[['Stock Splits', 'Return%', 'L5D_Return%', \
           '%52Wk_High','%52Wk_Low', 'Open%PriorClose', \
           'Close%Open', 'Close%High', 'Close%Low','Div%Close', \
           'SMA3%', 'SMA5%', 'SMA10%', 'SMA15%', 'SMA20%', 'SMA30%', 'SMA50%', \
           'EMA3%', 'EMA5%', 'EMA10%', 'EMA15%', 'EMA20%', 'EMA30%', 'EMA50%', \
           'PP%', 'S1C%', 'S2C%','S3C%', 'R1C%', 'R2C%', 'R3C%', \
           'S1F%', 'S2F%', 'S3F%', 'R1F%', 'R2F%', 'R3F%', \
           'SMA_Signal', 'MACD_Signal', 'RSI', 'RSI_Signal', 'Slow_K', 'Slow_D', \
           'Stoch_Osci', 'Fast_K', 'Fast_D', 'Stoch_RSI']]

    # Scale all features between 0 and 1
    norm = MinMaxScaler().fit(data)
    norm_data = pd.DataFrame(norm.transform(data), columns=data.columns)

    # Rename the "Stock Split" column
    norm_data.rename(columns={'Stock Splits': 'Stock_Splits_norm'}, inplace=True)
    
    return norm_data


def generate_model_data(df, metric="N5D_Return_Delayed%", buy_threshold=0.01, sell_threshold=-0.01):
    """
    Generate regression model data from a ticker download from yfinance.
    buy_threshold is the return threshold for labelling "buy".
    sell_threshold is the return threshold for labelling "sell".
    metric is the return metric used.
    
    """
    
    # Generate features
    data = add_features(df)
    
    # Drop NA rows where metrics cannot be computed (beginning and end of the dataframe)
    # Drops about a year plus a few days of data
    data = data.dropna(axis=0, how='any')
    
    # Generate labels
    return_metric = data[metric]
    
    buy_signal = pd.Series(return_metric >= buy_threshold).astype(int)
    sell_signal = pd.Series(return_metric <= sell_threshold).astype(int) * -1
    labels = buy_signal + sell_signal
    
    # Generate normalized model data
    norm_data = normalize_features(data)
    
    return norm_data, labels


def generate_lrmodel(ticker, model_timeframe="16y", 
                     metric="N5D_Return_Delayed%", buy_threshold=0.01, sell_threshold=-0.01):
    """
    Generate a logistic regression model for a ticker.
    model_timeframe is the timeframe where the model gets trained on.
    metric is the return metric the model is basing its labels on.
    """
    
    # Get model data
    data = yf.Ticker(ticker).history(period="16y")
    norm_data, labels = generate_model_data(data, metric, buy_threshold, sell_threshold)
    
    # Splitting training data to train and test data
    train_data, test_data, train_labels, test_labels = train_test_split(
        norm_data, labels, test_size=0.2, shuffle=False)

    ## Logistic Regression model, feature select using L2 regularization
    print("Logistic Regression Model:\n")
    print("{:>8}  {:>10}{:>10}".format("L2 c", "accuracy", "f1"))
    print("-" * 30)

    # Produce Logistic Regression models with various C values
    c_values = [0.1, 0.5, 1, 2, 5, 10, 100, 500, 1000, 2500, 5000, 7000, 8000]
    best_c, best_f1 = 0, 0

    for c in c_values:
        lr_model = LogisticRegression(C=c, solver="liblinear")
        lr_model.fit(train_data, train_labels)
        accuracy = lr_model.score(test_data, test_labels)
        f1 = metrics.f1_score(test_labels, lr_model.predict(test_data), average='weighted')
        print("{:>8}  {:10.4f}{:10.4f}".format(c, accuracy, f1))
        if f1 > best_f1:
            best_c = c
            best_f1 = f1 

    print("\nBest f1 score of {:.4f} at C={}".format(best_f1, best_c))
    c_l2 = best_c
    
    # Get the best model results
    lr_model = LogisticRegression(C=best_c, solver="liblinear")
    lr_model.fit(train_data, train_labels)
    """
    accuracy = lr_model.score(test_data, test_labels)
    f1 = metrics.f1_score(test_labels, lr_model.predict(test_data), average='weighted')
    print("Accuracy:", accuracy, "F1:", f1)
    """
    
    # Signals based on model results
    signal_data = normalize_features(add_features(data).tail(252*7)) #last 7 years
    signals = lr_model.predict(signal_data)
    
    # Generate output data
    output_data = data.tail(252*7).copy()
    output_data['LR_Signal'] = signals
    
    return lr_model, output_data


def LR_SIGNAL(data):
    return data['LR_Signal']
	

# class LogReg_Signal(Strategy): 
#     # Define parameters of the strategy
#     buy_signal = 1
#     sell_signal = -1
#     long_only = 1
    
#     def init(self):
#         # Compute signal
#         self.lr_sig = self.I(LR_SIGNAL, self.data)
        
#     def next(self):
#         # If RSI enters oversold territory
#         if self.lr_sig == self.buy_signal:
#             if self.long_only == 0:
#                 self.position.close()
#             self.buy()
        
#         # If RSI enters overbought territory
#         elif self.lr_sig == self.sell_signal:
#             self.position.close()
#             if self.long_only == 0:
#                 self.sell()


# ## Demo and export to CSV file

# model, signal_data = generate_lrmodel("SPY", buy_threshold=0.01, sell_threshold=-0.01)
# data = signal_data
# strategy = LogReg_Signal

# # Run backtesting
# bt = Backtest(data, strategy, cash=1_000_000, commission=0)
# stats = bt.run()

# # Display stats and plot results
# print(stats)
# bt.plot()

# ## Export to CSV: tickers we will pre-generate model results for
# tickers = ['SPY', 'QQQ', 'EEM', 'AAPL', 'MSFT', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA']

# ## Export to csv if easier to process
# for ticker in tickers:
#     model, signal_data = generate_lrmodel(ticker, buy_threshold=0.01, sell_threshold=-0.01)
#     signal_data.to_csv("lr_signal_data/" + ticker + "_lr_signal.csv")