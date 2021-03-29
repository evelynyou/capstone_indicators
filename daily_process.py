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


### Satoshi added for Arima Signal Dataframes on 3.28.2021 ###

# Getting the last 6 years data at once
def get_ydata(ticker):
    data = yf.download(ticker, period="6y")
    data = data.asfreq('D')
    data = data.ffill()
    return data

# Making a function to create prediction of days future
# Based on given data, returning "days" future predicted price
def arima_fcst(p, q, d, data, days):
    model = ARIMA(data['Close'], order=(p,d,q))
    results = model.fit()
    fcst = results.predict(len(data),len(data)+40, dynamic=False, typ='levels')  #.rename('ARIMA Forecast') #levels, linear
    return fcst[days]

tickers = ['SPY', 'QQQ', 'EEM', 'AAPL', 'MSFT', 'AMZN', 'FB', 'GOOGL', 'GOOG', 'TSLA']

# Setting parameters
p = 0
d = 1
q = 3
days = 5 

ARIMA_df_list = []

# Getting ARIMA signals for each ticker
for ticker in tickers:
    data = get_ydata(ticker)
    
    ARIMA_pred = []
    
    for n in range(len(data)-50):
        ARIMA_pred.append(arima_fcst(p, q, d, data.iloc[0+n:50+n], days))      
        
    data2 = data[50:]
    data2['ARIMA_Pred'] = ARIMA_pred
    data2['Arima_Signal'] = data2['ARIMA_Pred']/data2['Close']
    
    ARIMA_df_list.append(data2)

for n in range(len(tickers)):
    ARIMA_df_list[n].to_csv(f'ARIMA_csv_files/{tickers[n]}.csv', index=True)