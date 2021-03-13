from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import logging
import strats

# directly import sma
import get_data, backtest

app = Flask(__name__)

# NOTE: disable this after launch.
CORS(app)

# Return SMA backtesting result in JSON format, the high level
# JSON structure is ['data': data , 'err_msg': error_message].
# error_msg='OK' indicates success, or else it should contain
# the error message.
#
# You can test this function by visiting this url:
#   http://AWS_SITE_URL/backtest_sma
@app.route('/backtest')
def run_backtests():
    # TODO: handle invalid inputs: ticker, cash, commission

    # Get tickers
    if not 'stock_ticker' in request.args:
        return json.dumps({'err_msg': 'stock_ticker must be specified!'})
    ticker = request.args.get('stock_ticker')

    cash = 1000000.0
    commission = 0.0 

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
        return json.dumps({'err_msg': 'unable to download stock data.'})

    # Likely invalid ticker
    if ydata.shape[0] < 1:
        return json.dumps({'err_msg': 'Unable to download stock data, please check the ticker!'})
    
    # backtest
    backtest_returns, backtest_trades = backtest.backtest_with_all_strats(ydata,
            cash, commission)
    return backtest_returns.to_json()

@app.route("/backtest_details")
def backtest_details():
    print('In backtest_details')

    # Get tickers
    if not 'stock_ticker' in request.args:
        return json.dumps({'err_msg': 'stock_ticker must be specified!'})
    ticker = request.args.get('stock_ticker')

    # Get Strategy
    if not 'strategy' in request.args:
        return json.dumps({'err_msg': 'staregy must be specified!'})
    strategy = request.args.get('strategy')

    strategy_map = {
            "MacdSignal": strats.MacdSignal,
            "BuyAndHold": strats.BuyAndHold,
            "SmaCross": strats.SmaCross,
            "RsiSignal": strats.RsiSignal,
            "StochOsci": strats.StochOsci,
            "StochRsi": strats.StochRsi
    }


    stock_obj = get_data.yFinData(ticker)
    # Get last days to backtest, return error messsage if it's not set.
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,3y,5y,10y,ytd,max 
    #if not 'last_days' in request.args:
    #    return json.dumps({'err_msg': 'last_days must be specified!'})
    #last_days = request.args.get('last_days')

    print('Get request with ticker=' + ticker + ",strategy=" + strategy)

    # Pull max stocks data
    try:
        ydata = stock_obj.get_ohlcv()
    except:
        logging.error('Uable to download data.')
        return json.dumps({'err_msg': 'uable to download stock data.'})
    
    # Raw HTML file in string format
    return backtest.get_backtest_plot(ydata, strategy_map[strategy], cash=1000000.0, commission=0.0)

 
@app.route("/how_it_works")
def how_it_works():
    print('In how it works')
    #return 'Best Trading Indicators Ever!'
    return render_template('how_it_works.html')


@app.route("/indicators")
def indicators():
    print('In indicators')
    #return 'Best Trading Indicators Ever!'
    return render_template('indicators.html')


@app.route("/about")
def about():
    print('In about')
    #return 'Best Trading Indicators Ever!'
    return render_template('about.html')    


@app.route('/')
def w210():
    print('Received request')
    #return 'Best Trading Indicators Ever!'
    return render_template('index.html')
