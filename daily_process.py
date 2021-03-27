import backtest
import get_data
import pandas as pd


def daily_process():
    tickers = ['SPY', 'QQQ', 'EEM', 'AAPL', 'MSFT', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA']
    strategies = ['SmaCross', 'MacdSignal', 'RsiSignal']
    corresponding_dict = {'SmaCross':backtest.sma_reliability, 
                      'MacdSignal':backtest.macd_reliability,
                      'RsiSignal':backtest.rsi_reliability}
    for ticker in tickers:
        stock_obj = get_data.yFinData(ticker)
        try:
            data = stock_obj.get_ohlcv()
        except:
            print('Uable to download data.')
        pbos = []
        for strategy in strategies:
            reliability_test = corresponding_dict[strategy]
            train_stats, test_stats = reliability_test(data)
            train_df, test_df = backtest.gather_sims(train_stats, test_stats)
            backtest.visualize(train_df, "TRAIN", ticker, strategy), backtest.visualize(test_df, "TEST", ticker, strategy)
            backtest.corr_plot(train_df, test_df, ticker, strategy)
            pbo = backtest.calculate_pbo(train_df, test_df)
            pbos.append([strategy, pbo])
        pbos = pd.DataFrame(pbos, columns=["strategy", "pbo"])
        pbos["datetime"] = date.today().strftime("%d/%m/%Y")
        pbos.to_csv("reliability_pbo/{}_pbo.csv".format(ticker), index=False)