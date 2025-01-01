import sys
sys.path.append('C:/Users/user/Documents/GitHub/AxoStratSimulator/')

import abc
from StrategyResult import StrategyResult
import datetime as dt
import math
from PriceHistory import PriceHistory
import TapToolsConnector as ttc
from infrastructure import DateUtils as dtu

class ATradingStrategy(abc.ABC):  
    @abc.abstractmethod
    def SetInitialState(self, result: StrategyResult):
        pass
    
    @abc.abstractmethod
    def UpdateStateAndTrade(self, curPrice, p, curDate, result: StrategyResult, isLastPeriod):
        pass
    
    @abc.abstractmethod
    def getstrategyparams(pricehistory:PriceHistory, simparamslist:list[dict]):
        pass
    
    @classmethod
    def get_simparams(cls,startAmountA:float, token:str, overall_days:int, interval_days:int):
        pHLength = dt.timedelta(days=overall_days)
        priceHistoryFull = ttc.GetPriceHistoryPath(token, pHLength)
        historyEnd = priceHistoryFull.DateGrid[-1]
        timePeriods = dtu.GetPeriods(historyEnd,overall_days,interval_days)
        simparamslist = [{'startDate':x[0],'endDate':x[1],'checkFrequency':dt.timedelta(minutes=3),'startAmountA':startAmountA,'startAmountB':0} for x in timePeriods]
        return cls.getstrategyparams(priceHistoryFull, simparamslist)  
    
    def SimulateStrategy(self, priceHistory: PriceHistory, simParams:dict):
        startDate = simParams['startDate']
        enddate = simParams['endDate']
        checkFrequency = simParams['checkFrequency']
        pricehistory_short = priceHistory.project_to_grid(startDate, enddate, checkFrequency)
        numIntervals = pricehistory_short.DateGrid.size
        result = StrategyResult(numIntervals)
        result.DateGrid[0] = startDate
        result.HoldingABop[0] = simParams['startAmountA']
        result.HoldingBBop[0] = simParams['startAmountB']
        self.SetInitialState(result)
        for p in range(0, numIntervals):   
            curPrice = pricehistory_short.Prices[p]
            curDate = pricehistory_short.DateGrid[p]
            self.UpdateStateAndTrade(curPrice, p, curDate, result, p == numIntervals - 1)
        return result
            