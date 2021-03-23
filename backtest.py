from backtesting import Backtest
import inspect
import pandas as pd
import numpy as np
import seaborn as sns
from itertools import combinations
import tensorflow as tf
import scipy.stats as ss
import strats
from typing import Tuple
import time
from sklearn.model_selection import BaseCrossValidator
import matplotlib.pyplot as plt
import base64
from io import BytesIO



# Run backtesting
avail_strats = [obj for name, obj in inspect.getmembers(strats, inspect.isclass) if obj.__module__ == 'strats']

def backtest_with_all_strats(ydata: pd.DataFrame, cash: int=1_000_000, commission: float=0.) -> Tuple[pd.DataFrame, dict]:
    """
    backtest all strategies in strats.py
    input: stock OHLCV dataframe
    output: dataframe of strategy returns, dictionary of trades and equity curve
    """
    temp = []
    sname_temp = []
    equity_trades = {}
    periods = ['0.5', '1', '2', 2020, 2019, 2018, 2017, 2016]
    
    for s in avail_strats:
        for period in periods:
            if isinstance(period, str):
                data = ydata.iloc[-int(float(period)*252):]
            elif isinstance(period, int):
                data = ydata.loc["{}-12-31".format(period-1):"{}-12-31".format(period),]

            # No data
            if data.shape[0] == 0:
                continue

            bt = Backtest(data, s, cash=cash, commission=commission)
            stats = bt.run()
            sname = str(stats["_strategy"])
            sname_temp.append("{}_{}".format(sname, period))
            temp.append(stats[:27])
            equity_trades["{}_{}".format(sname, period)] = (stats["_equity_curve"], stats["_trades"])

    strat_returns = pd.concat(temp, axis=1)
    strat_returns.columns = sname_temp
    return strat_returns, equity_trades

def get_back_test_comparasion(ydata: pd.DataFrame, strategy: str, data_range, strategy_params: dict,
                              cash: int=1_000_000, commission: float=0.):
    """
    backtest vs buy/hold strategy in strats.py
    input: stock OHLCV dataframe
    output: dataframe of strategy returns, dictionary of trades and equity curve
    """
    avail_strats = [obj for name, obj in inspect.getmembers(strats, inspect.isclass) 
                    if (obj.__name__ == strategy) or (obj.__name__ == "BuyAndHold")]
    if not data_range.isdecimal():
        corresponding = {"6m":0.5, "1y":1., "2y":2.}
        data = ydata.iloc[-int(float(corresponding[data_range])*252):]
    else:
        data = ydata.loc["{}-12-31".format(int(data_range)-1):"{}-12-31".format(int(data_range)),]
    
    temp = []
    sname_temp = []
    equity_trades = {}
    for s in avail_strats:
        if data.shape[0] == 0:
            continue

        bt = Backtest(data, s, cash=cash, commission=commission)
        if s.__name__ == 'SmaCross':
            stats = bt.run(slow = strategy_params['slow'],
                           fast = strategy_params['fast'],
                           long_only = strategy_params['long_only'])
        elif s.__name__ == 'MacdSignal':
            stats = bt.run(fastperiod = strategy_params['fastperiod'],
                           slowperiod = strategy_params['slowperiod'],
                           signalperiod = strategy_params['signalperiod'],
                           long_only = strategy_params['long_only'])
        elif s.__name__ == 'StochOsci':
            stats = bt.run(fastk_period = strategy_params['fastk_period'],
                           slowk_period = strategy_params['slowk_period'],
                           slowd_period = strategy_params['slowd_period'],
                           overbought = strategy_params['overbought'],
                           oversold = strategy_params['oversold'],
                           long_only = strategy_params['long_only'])
        elif s.__name__ == 'StochRsi':
            stats = bt.run(timeperiod = strategy_params['timeperiod'],
                           fastk_period = strategy_params['fastk_period'],
                           slowk_period = strategy_params['slowk_period'],
                           slowd_period = strategy_params['slowd_period'],
                           overbought = strategy_params['overbought'],
                           oversold = strategy_params['oversold'],
                           long_only = strategy_params['long_only']) 
        else:
            stats = bt.run()
        sname = str(stats["_strategy"])
        sname_temp.append("{}_{}".format(sname, data_range))
        temp.append(stats[:27])
        equity_trades["{}_{}".format(sname, data_range)] = (stats["_equity_curve"], stats["_trades"])

    strat_returns = pd.concat(temp, axis=1)
    strat_returns.columns = sname_temp
    return strat_returns

def get_backtest_plot(ydata, strat, cash=1_000_000, commission=0.):
    """
    get auto generated backtestplot
    input: stock OHLCV dataframe, strategy
    output: plot obj
    """
    bt = Backtest(ydata, strat, cash=cash, commission=commission)
    stats = bt.run()
    # Save plots to file
    filename = "./tmp_plots/" + str(time.time()) + ".html"
    bt.plot(filename = filename)
    # Conver it to string
    with open(filename, 'r') as file:
        data = file.read().replace('\n', '')
    return data
    

class CPCV(BaseCrossValidator):
    # TODO: add purge "holes" !!!
    def __init__(self, X, N, k):
        self.X = X
        self.N = N
        self.k = k

    def generate_eras(self):
        # assuming exact division, we will cut-off small piece of time series
        # in the very beginning
        return np.array(sum([
                    [i] * (len(self.X) // self.N) for i in range(self.N)
                    ], []
                   )
        )
        
    def split(self, X=None, y=None, groups=None):
        # removing first m items from time series
        eras = self.generate_eras()
        len_diff = abs(len(self.X) - len(eras))
        comb = list(combinations(range(self.N), self.N-self.k))
        all_splits = range(self.N)

        for combination in comb:
            train_indices, test_indices = [], []
            for c in combination:
                indices_train = list(np.where(eras == c)[0])
                train_indices.extend(indices_train)
            for t in list(set(all_splits) - set(combination)):
                indices_test = list(np.where(eras == t)[0])
                test_indices.extend(indices_test)
            yield(train_indices, test_indices)  
              
    def get_n_splits(self):
        comb = combinations(range(self.N), self.N-self.k)
        return len(list(comb))
    

def sma_reliability(data, N=6, k=2):
    data = data.iloc[-int(float(5)*252):-1]
    cpcv = CPCV(data, N, k)
    train_temp = []
    test_temp = []
    NSAMPLES = 5
    for e, (train_ids, test_ids) in enumerate(cpcv.split()):
        dataset_train, dataset_test = data.iloc[train_ids], data.iloc[test_ids]
        train, test = [], []
        bt = Backtest(dataset_train, strats.SmaCross, cash=10_000, commission=0.0)
        for i in range(NSAMPLES):
            stats_skopt, heatmap, optimize_result = bt.optimize(
                fast = [5, 50],
                slow = [10, 60],
                constraint=lambda p: p.fast < p.slow,
                maximize='Sharpe Ratio',
                method='skopt',
                max_tries=30,
                return_heatmap=True,
                return_optimization=True)
            btopt = Backtest(dataset_test, strats.SmaCross, cash=10_000, commission=0.0)
            optstats = btopt.run(fast = optimize_result.x[0], slow = optimize_result.x[1])
            train.append(stats_skopt)
            test.append(optstats)
        train_temp.append(train)
        test_temp.append(test)
    train_stats = [pd.concat(train, axis=1) for train in train_temp]
    test_stats = [pd.concat(test, axis=1) for test in test_temp]
    return train_stats, test_stats

def macd_reliability(data, N=6, k=2):
    data = data.iloc[-int(float(5)*252):-1]
    cpcv = CPCV(data, N, k)
    train_temp = []
    test_temp = []
    NSAMPLES = 5
    for e, (train_ids, test_ids) in enumerate(cpcv.split()):
        dataset_train, dataset_test = data.iloc[train_ids], data.iloc[test_ids]
        train, test = [], []
        bt = Backtest(dataset_train, strats.MacdSignal, cash=10_000, commission=0.0)
        for i in range(NSAMPLES):
            stats_skopt, heatmap, optimize_result = bt.optimize(
                fastperiod = [5, 50],
                slowperiod = [10, 60],
                signalperiod = [5, 20],
                constraint=lambda p: p.signalperiod < p.fastperiod < p.slowperiod,
                maximize='Sharpe Ratio',
                method='skopt',
                max_tries=30,
                return_heatmap=True,
                return_optimization=True)
            btopt = Backtest(dataset_test, strats.MacdSignal, cash=10_000, commission=0.0)
            optstats = btopt.run(fastperiod = optimize_result.x[0], slowperiod = optimize_result.x[1], signalperiod = optimize_result.x[2])
            train.append(stats_skopt)
            test.append(optstats)
        train_temp.append(train)
        test_temp.append(test)
    train_stats = [pd.concat(train, axis=1) for train in train_temp]
    test_stats = [pd.concat(test, axis=1) for test in test_temp]
    return train_stats, test_stats

def rsi_reliability(data, N=6, k=2):
    data = data.iloc[-int(float(5)*252):-1]
    cpcv = CPCV(data, N, k)
    train_temp = []
    test_temp = []
    NSAMPLES = 5
    for e, (train_ids, test_ids) in enumerate(cpcv.split()):
        dataset_train, dataset_test = data.iloc[train_ids], data.iloc[test_ids]
        train, test = [], []
        bt = Backtest(dataset_train, strats.RsiSignal, cash=10_000, commission=0.0)
        for i in range(NSAMPLES):
            stats_skopt, heatmap, optimize_result = bt.optimize(
                timeperiod = [10, 20],
                overbought = [70, 90],
                oversold = [10, 30],
                maximize='Sharpe Ratio',
                method='skopt',
                max_tries=30,
                return_heatmap=True,
                return_optimization=True)
            btopt = Backtest(dataset_test, strats.RsiSignal, cash=10_000, commission=0.0)
            optstats = btopt.run(timeperiod = optimize_result.x[0], overbought = optimize_result.x[1], oversold = optimize_result.x[2])
            train.append(stats_skopt)
            test.append(optstats)
        train_temp.append(train)
        test_temp.append(test)
    train_stats = [pd.concat(train, axis=1) for train in train_temp]
    test_stats = [pd.concat(test, axis=1) for test in test_temp]
    return train_stats, test_stats


def gather_sims(train_stats, test_stats):
    display = ['Return (Ann.) [%]', 'Exposure Time [%]', 'Win Rate [%]',
               '# Trades', 'Volatility (Ann.) [%]', 'Max. Drawdown [%]',
               'Sharpe Ratio', 'Sortino Ratio', 'Calmar Ratio']
    train_dict = {}
    test_dict = {}
    for d in display:
        train_collected = []
        test_collected = []
        for train, test in zip(train_stats, test_stats):
            train_data = train.loc[d,:].to_numpy()
            test_data = test.loc[d,:].to_numpy()
            train_collected = np.concatenate((train_collected, train_data), axis=None)
            test_collected = np.concatenate((test_collected, test_data), axis=None)
        train_dict[d] = train_collected
        test_dict[d] = test_collected
    return pd.DataFrame(train_dict), pd.DataFrame(test_dict)

def visualize(df, ticker, strategy):
    df['Sharpe Ratio (scaled, x100)'] = df['Sharpe Ratio'] * 100
    display = ['Return (Ann.) [%]', 'Exposure Time [%]', 'Win Rate [%]',
               'Volatility (Ann.) [%]', 'Max. Drawdown [%]',
               'Sharpe Ratio (scaled, x100)']
    dfl = df.loc[:,display].stack().reset_index(level=1).rename(columns={'level_1':'metric', 0:'value'})
    dfl = dfl.astype({'value':'float64'})
    df  = df.loc[:,display]
    g = sns.displot(data=dfl, x='value', col='metric', bins=40, kde=True, col_wrap=3, facet_kws={'sharex':False, 'sharey':False})
    for i, ax in enumerate(g.axes.flat): # set every-other axis for testing purposes
        mini = df.iloc[:,i].min()
        maxi = df.iloc[:,i].max()
        mean = df.iloc[:,i].mean()
        ax.axvline(mean, ls = '--', color = 'red', label = "mean: {}".format(round(mean, 3)))
        ax.set_xlim(int(mini)-5,int(maxi)+5)
        ax.legend()
    
    tmpfile = BytesIO()
    g.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    filename = "./reliability_plots/"+ ticker + "_" + strategy + "_" + str(time.time()) + ".html"
    with open(filename,'w') as f:
        f.write(html)
    with open(filename, 'r') as f:
        data = f.read().replace('\n', '')
    return data

def calculate_pbo(train_df, test_df):
    w_c_is = train_df['Sharpe Ratio']
    w_c_oos = test_df['Sharpe Ratio']
    n_star = np.argmax(w_c_is)
    n_star, ss.rankdata(w_c_oos)
    w_c = (ss.rankdata(w_c_oos) - n_star) / len(w_c_oos)
    w_c = w_c + np.abs(np.min(w_c))
    y_c = np.log(w_c / (1 - w_c))
    y_c[y_c==-np.inf] = 0
    y_c_neg = y_c[y_c < 0]
    y_c_neg = (y_c_neg - y_c_neg.min()) / (y_c_neg.max() - y_c_neg.min())
    pbo = np.mean(y_c_neg)
    return pbo

def corr_plot(train_df, test_df, ticker, strategy):
    train = train_df.loc[:,["Sharpe Ratio"]].rename(columns={"Sharpe Ratio":"Sharpe Ratio IS"})
    test = test_df.loc[:,["Sharpe Ratio"]].rename(columns={"Sharpe Ratio":"Sharpe Ratio OOS"})
    df = train.join(test)
    corr = plt.figure()
    sns.scatterplot(data=df, x="Sharpe Ratio IS", y="Sharpe Ratio OOS")
    plt.xlabel('Sharpe ratios IS')
    plt.ylabel('Sharpe ratios OOS')
    
    tmpfile = BytesIO()
    corr.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<img src=\'data:image/png;base64,{}\'>'.format(encoded)
    filename = "./reliability_plots/"+ ticker + "_" + strategy + "_corr_" + str(time.time()) + ".html"
    with open(filename,'w') as f:
        f.write(html)
    with open(filename, 'r') as f:
        data = f.read().replace('\n', '')
    return data