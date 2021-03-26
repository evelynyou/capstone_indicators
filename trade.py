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
    backtest_returns, backtest_trades = backtest.backtest_with_all_strats(ydata, cash, commission)
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


@app.route("/details")
def details_page():
    ticker = request.args.get('stock_ticker')
    strategy = request.args.get('strategy')
    return render_template('details.html', stock_ticker=ticker, strategy = strategy)


@app.route("/vs_buy_and_hold")
def vs_buy_and_hold():
    # Extract common parameters
    ticker = request.args.get('stock_ticker')
    strategy = request.args.get('strategy')
    long_only = request.args.get('long_only') # 'Yes' or 'No'
    date_range = request.args.get('date_range') # '6m', '1y', '2y', '2016', '2017', '2018', '2019', '2020'

    # Object to hold strategy specific parameters
    strategy_specific_params = {}
    if (strategy == 'SmaCross'):
      strategy_specific_params['slow'] = int(request.args.get('sma_slow'))
      strategy_specific_params['fast'] = int(request.args.get('sma_long'))
    elif (strategy == 'MacdSignal'):
      strategy_specific_params['fastperiod'] = int(request.args.get('fast_period'))
      strategy_specific_params['slowperiod'] = int(request.args.get('slow_period'))
      strategy_specific_params['signalperiod'] = int(request.args.get('signal_period'))
    elif (strategy == 'StochOsci'):
      strategy_specific_params['fastk_period'] = int(request.args.get('fast_k_period'))
      strategy_specific_params['slowk_period'] = int(request.args.get('slow_k_period'))
      strategy_specific_params['slowd_period'] = int(request.args.get('slow_d_period'))
      strategy_specific_params['overbought'] = int(request.args.get('overbought'))
      strategy_specific_params['oversold'] = int(request.args.get('oversold'))
    elif (strategy == 'StochRsi'):
      strategy_specific_params['timeperiod'] = int(request.args.get('time_period'))
      strategy_specific_params['fastk_period'] = int(request.args.get('fast_k_period'))
      strategy_specific_params['slowk_period'] = int(request.args.get('slow_k_period'))
      strategy_specific_params['slowd_period'] = int(request.args.get('slow_d_period'))
      strategy_specific_params['overbought'] = int(request.args.get('overbought'))
      strategy_specific_params['oversold'] = int(request.args.get('oversold'))
    else: 
      # Invalid strategy
      pass

    strategy_specific_params['long_only'] = long_only
    
    stock_obj = get_data.yFinData(ticker)
    print('Get request with ticker=' + ticker)
    try:
        ydata = stock_obj.get_ohlcv()
    except:
        logging.error('Uable to download data.')
        return json.dumps({'err_msg': 'unable to download stock data.'})

    # Likely invalid ticker
    if ydata.shape[0] < 1:
        return json.dumps({'err_msg': 'Unable to download stock data, please check the ticker!'})
    
    backtest_returns = get_back_test_comparasion(ydata, strategy, data_range, strategy_specific_params,
                                                 cash=1_000_000, commission=0.)
    
    # this is same as run_backtests() but now with custom params and comparison of B/H and strategy
    return backtest_returns.to_json()


@app.route("/reliability_test")
def reliability_test():
    preload = ['SPY', 'QQQ', 'EEM', 'AAPL', 'MSFT', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA']
    ticker = request.args.get('stock_ticker')
    strategy = request.args.get('strategy')
    corresponding_dict = {'SmaCross':backtest.sma_reliability, 
                          'MacdSignal':backtest.macd_reliability,
                          'RsiSignal':backtest.rsi_reliability}
    reliability_test = corresponding_dict[strategy]
    
    stock_obj = get_data.yFinData(ticker)
    print('Get request with ticker=' + ticker)
    try:
        ydata = stock_obj.get_ohlcv()
    except:
        logging.error('Uable to download data.')
        return json.dumps({'err_msg': 'unable to download stock data.'})

    # Likely invalid ticker
    if ydata.shape[0] < 1:
        return json.dumps({'err_msg': 'Unable to download stock data, please check the ticker!'})
    
    if ticker in preload:
        #TODO: add preload htmls, now no difference, expect this to take ~5 min
        train_stats, test_stats = reliability_test(ydata)
        train_df, test_df = backtest.gather_sims(train_stats, test_stats)
        train_plot, test_plot = backtest.visualize(train_df, ticker, strategy), backtest.visualize(test_df, ticker, strategy)
    else:
        return None
    # Return html content directly just like the function `backtest_details`
    
    # Potential solution:
    # - Just check the ticker and read pre-generated data file, then return it.
    # - Return empty for not supported tickers
    
    # train_plot, test_plot, and corr_plot should be htmls, checkout the reliability_plots folder.
    # display this similarly to how we are displaying in details page
    # pbo is a single float, just show "Probability of Overfitting: pbo" somewhere
    return train_plot, test_plot, pbo, corr_plot
 

 
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
