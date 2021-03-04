from backtesting import Strategy
from backtesting.lib import crossover
import numpy as np
import indicators as ind


class BuyAndHold(Strategy):
    # This strategy actually starts at day 2 of the time period because of the next() method
    # Making it more comparable as a control for the rest of the strategies
    def init(self):
        next
    def next(self):
        self.buy()

class SmaCross(Strategy):
    # Define parameters of the strategy
    fast = 5
    slow = 15
    long_only = 1
    def init(self):
        # Compute moving averages
        if np.prod([isinstance(param, int) for param in [self.fast, self.slow]]):
            self.fast_sma = self.I(ind.SMA, self.data.Close, self.fast)
            self.slow_sma = self.I(ind.SMA, self.data.Close, self.slow)
        else:
            self.fast_sma = self.I(ind.modCloseStrategy, ind.SMA, self.data.Close, self.fast)
            self.slow_sma = self.I(ind.modCloseStrategy, ind.SMA, self.data.Close, self.slow)
            
    def next(self):
        # If fast SMA crosses above slow SMA
        if crossover(self.fast_sma, self.slow_sma):
            if self.long_only == 0:
                self.position.close()
            self.buy()

        # Else, if fast SMA crosses below slow SMA
        elif crossover(self.slow_sma, self.fast_sma):
            self.position.close()
            if self.long_only == 0:
                self.sell()
        
        
class MacdSignal(Strategy): 
    # Define parameters of the strategy
    fastperiod = 12
    slowperiod = 26
    signalperiod = 9
    long_only = 1
    
    def init(self):
        # Compute MACD
        if np.prod([isinstance(param, int) for param in [self.fastperiod, self.slowperiod, self.signalperiod]]):
            self.macd, self.macdsignal, self.macdhist = self.I(
                 ind.MACD, self.data.Close, self.fastperiod, self.slowperiod, self.signalperiod)
        else:
            self.macd, self.macdsignal, self.macdhist = self.I(
                 ind.modCloseStrategy, ind.MACD, self.data.Close, self.fastperiod, self.slowperiod, self.signalperiod)  
        
    def next(self):
        # If MACD crosses above signal line
        if crossover(self.macd, self.macdsignal):
            if self.long_only == 0:
                self.position.close()
            self.buy()

        # Else, if MACD crosses below signal line
        elif crossover(self.macdsignal, self.macd):
            self.position.close()
            if self.long_only == 0:
                self.sell()
                
                
class RsiSignal(Strategy): 
    # Define parameters of the strategy
    timeperiod = 14
    overbought = 70
    oversold = 30
    long_only = 1
    
    def init(self):
        # Compute RSI
        if np.prod([isinstance(param, int) for param in [self.timeperiod]]):
            self.real = self.I(ind.RSI, self.data.Close, self.timeperiod)
        else:
            self.real = self.I(ind.modCloseStrategy, ind.RSI, self.data.Close, self.timeperiod)
        
    def next(self):
        # If RSI enters oversold territory
        if self.real <= self.oversold:
            if self.long_only == 0:
                self.position.close()
            self.buy()
        
        # If RSI enters overbought territory
        elif self.real >= self.overbought:
            self.position.close()
            if self.long_only == 0:
                self.sell()
                
    
class StochOsci(Strategy): 
    # Define parameters of the strategy
    fastk_period = 14
    slowk_period = 3
    slowk_matype = 0
    slowd_period = 3
    slowd_matype = 0
    overbought = 80
    oversold = 20
    long_only = 1
    
    def init(self):
        # Compute K and D lines
        if np.prod([isinstance(param, int) for param in [self.fastk_period, self.slowk_period,
                                                         self.slowk_matype, self.slowd_period, self.slowd_matype]]):
            self.slowk, self.slowd = self.I(ind.STOCH, self.data.High, self.data.Low, self.data.Close, 
                                            self.fastk_period, self.slowk_period, self.slowk_matype, 
                                            self.slowd_period, self.slowd_matype)
        else:
            self.slowk, self.slowd = self.I(ind.modHLCStrategy, ind.STOCH, self.data.High, self.data.Low, self.data.Close, 
                                            self.fastk_period, self.slowk_period, self.slowk_matype, 
                                            self.slowd_period, self.slowd_matype)
        
    def next(self):
        # If K and D enter oversold territory
        if self.slowk <= self.oversold and self.slowd < self.oversold:
            if self.long_only == 0:
                self.position.close()
            self.buy()
        
        # If K and D enter overbought territory
        elif self.slowk >= self.overbought and self.slowd > self.overbought:
            self.position.close()
            if self.long_only == 0:
                self.sell()
                
                
class StochRsi(Strategy): 
    # Define parameters of the strategy
    timeperiod = 14
    fastk_period = 14
    fastd_period = 3
    fastd_matype = 0
    overbought = 80
    oversold = 20
    long_only = 1
    
    def init(self):
        # Compute K and D lines
        if np.prod([isinstance(param, int) for param in [self.timeperiod, self.fastk_period, 
                                                         self.fastd_period, self.fastd_matype]]):
            self.fastk, self.fastd = self.I(ind.STOCHRSI, self.data.Close, self.timeperiod,
                                            self.fastk_period, self.fastd_period, self.fastd_matype)
        else:
            self.fastk, self.fastd = self.I(ind.modCloseStrategy, ind.STOCHRSI, self.data.Close, self.timeperiod,
                                            self.fastk_period, self.fastd_period, self.fastd_matype)
            
    def next(self):
        # If K and D enter oversold territory
        if self.fastk < self.oversold and self.fastd < self.oversold:
            if self.long_only == 0:
                self.position.close()
            self.buy()
        
        # If K and D enter overbought territory
        elif self.fastk > self.overbought and self.fastd > self.overbought:
            self.position.close()
            if self.long_only == 0:
                self.sell()
                
                
