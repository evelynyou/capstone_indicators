from backtesting import Backtest
import inspect
import pandas as pd
import strats
from typing import Tuple


# Run backtesting
avail_strats = [obj for name, obj in inspect.getmembers(strats, inspect.isclass) if obj.__module__ == 'strats']

def backtest_with_all_strats(ydata: pd.DataFrame, cash: int=10_000, commission: float=0.) -> Tuple[pd.DataFrame, dict]:
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
            bt = Backtest(data, s, cash=cash, commission=commission)
            stats = bt.run()
            sname = str(stats["_strategy"])
            sname_temp.append("{}_{}".format(sname, period))
            temp.append(stats[:27])
            equity_trades["{}_{}".format(sname, period)] = (stats["_equity_curve"], stats["_trades"])

    strat_returns = pd.concat(temp, axis=1)
    strat_returns.columns = sname_temp
    return strat_returns, equity_trades

def get_backtest_plot(ydata, strat, cash=10_000, commission=0.):
    """
    get auto generated backtestplot
    input: stock OHLCV dataframe, strategy
    output: plot obj
    """
    bt = Backtest(ydata, strat, cash=cash, commission=commission)
    stats = bt.run()
    return bt.plot()


    
    