import pandas as pd
import inspect
import numpy as np
import json
import logging
from backtesting import Backtest
import inspect
import pandas as pd
import strats
from typing import Tuple




# directly import sma
import get_data, backtest

def test_backtest():
    ticker = "SPY"
    cash = "10000.0"
    commission = "0.0"

    stock_obj = get_data.yFinData(ticker)
    # Get last days to backtest, return error messsage if it's not set.
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,3y,5y,10y,ytd,max 
    #if not 'last_days' in request.args:
    #    return json.dumps({'err_msg': 'last_days must be specified!'})
    #last_days = request.args.get('last_days')

    print('Get request with ticker=' + ticker)

    # Pull max stocks data
    try:
        ydata = stock_obj.get_ohlcv()
    except:
        logging.error('Uable to download data.')
        print("err_msg:" +  "uable to download stock data.")
    
    # backtest
    backtest_returns, backtest_trades = backtest.backtest_with_all_strats(ydata,
            cash, commission)
    print(backtest_returns.to_json())


def test_backtest_details():
    ticker = "SPY"
    cash = "10000.0"
    commission = "0.0"

    stock_obj = get_data.yFinData(ticker)
    # Get last days to backtest, return error messsage if it's not set.
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,3y,5y,10y,ytd,max 
    #if not 'last_days' in request.args:
    #    return json.dumps({'err_msg': 'last_days must be specified!'})
    #last_days = request.args.get('last_days')

    print('Get request with ticker=' + ticker)

    # Pull max stocks data
    try:
        ydata = stock_obj.get_ohlcv()
    except:
        logging.error('Uable to download data.')
        print("err_msg:" +  "uable to download stock data.")

    # backtest
    # <class 'strats.MacdSignal'>
    # <class 'strats.RsiSignal'>
    # <class 'strats.SmaCross'>
    # <class 'strats.StochOsci'>
    # <class 'strats.StochRsi'>
    plot = backtest.get_backtest_plot(ydata, strats.MacdSignal(), cash, commission)
    print(type(plot))
    print(str(plot))


test_backtest_details()


