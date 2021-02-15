import yfinance as yf

# Other potential fields of interest
# stock.info
# stock.major_holders
# stock.recommendations
# stock.options

class yFinData:
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)

    def get_ohlcv(self):
        """
        get max OHLCV data through yfin
        params: none
        output: dataframe of max OHLCV data
        """
        return self.stock.history(period="max")
    
    def get_stock_info(self):
        """
        get basic info of stock on yfinance, sector, yeild, devidend, etc.
        params: none
        output: dictionary of stock basic info
        """
        return self.stock.info
    
    def get_recommendations(self):
        """
        get recommendations from major firms
        params: none
        output: dataframe of date, buy/sell recommendations
        """
        return self.stock.recommendations
    
    
