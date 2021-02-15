from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import logging

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
@app.route('/backtest_sma')
def backtest_sma():
    # Get stock tickers, return error message if it's not set.
    if not 'stock_ticker' in request.args:
        return json.dumps({'err_msg': 'stock_ticker must be specified!'})
    ticker = request.args.get('stock_ticker')
    stock_obj = get_data.yFinData(ticker)
    # Get last days to backtest, return error messsage if it's not set.
    # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,3y,5y,10y,ytd,max 
    #if not 'last_days' in request.args:
    #    return json.dumps({'err_msg': 'last_days must be specified!'})
    #last_days = request.args.get('last_days')

    print('Get request with ticker=' + stock_ticker)

    # Pull max stocks data
    try:
        ydata = stock_obj.get_ohlcv()
    except:
        logging.error('Uable to download data.')
        return json.dumps({'err_msg': 'uable to download stock data.'})
    
    # backtest
    backtest_returns, backtest_trades = backtest.backtest_with_all_strats(ydata)
    
    # TODO: convert dataframe and dict to json digestables
    
    #   - Convert result into JSON and return it.
    result = [{'key': field, 'value': str(stats[field])} for field in stats.keys()]
    ## Fake data for testing.
    #result = [{'key': 'Start',   'value': '2020-01-01'},
    #          {'key': 'End',     'value': '2020-02-09'},
    #          {'key': 'Gain',    'value': 10000},
    #          {'key': 'WinRate', 'value': 0.89}]

    return json.dumps({'data': result, 'err_msg': 'OK'})
 

@app.route('/')
def w210():
    print('Received request')
    #return 'Best Trading Indicators Ever!'
    return render_template('index.html')
