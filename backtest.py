from backtesting import Backtest
import inspect
import pandas as pd
import strats
from typing import Tuple


# Run backtesting
avail_strats = [obj for name, obj in inspect.getmembers(strats, inspect.isclass) if obj.__module__ == 'strats']

def backtest_with_all_strats(ydata: pd.DataFrame, cash=10_000: int) -> Tuple[pd.DataFrame, dict]:
    """
    backtest all strategies in strats.py
    input: stock OHLCV dataframe
    output: dataframe of strategy returns, dictionary of trades and equity curve
    """
    temp = []
    sname_temp = []
    equity_trades = {}
    for s in avail_strats:
        bt = Backtest(ydata, s, cash=cash, commission=0)
        stats = bt.run()
        sname = str(stats["_strategy"])
        sname_temp.append(sname)
        temp.append(stats[:27])
        equity_trades[sname] = (stats["_equity_curve"], stats["_trades"])

    strat_returns = pd.concat(temp, axis=1)
    strat_returns.columns = sname_temp
    return strat_returns, equity_trades

def get_backtest_plot(ydata, strat, cash=10_000):
    """
    get auto generated backtestplot
    input: stock OHLCV dataframe, strategy
    output: plot obj
    """
    bt = Backtest(ydata, strat, cash=cash, commission=0)
    stats = bt.run()
    return bt.plot()
    
    