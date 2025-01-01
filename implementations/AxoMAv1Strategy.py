import sys
sys.path.append('C:/Users/user/Documents/GitHub/AxoStratSimulator/')

from ATradingStrategy import ATradingStrategy
from StrategyResult import StrategyResult
import datetime as dt
import TapToolsConnector as ttc
from PriceHistory import PriceHistory
import math

class AxoMAv1Strategy(ATradingStrategy):
    StartPrice: float
    MaSteps: int
    CheckInterval: dt.timedelta
    Spread: float 
    MAPrice: float    
    MAPricePop: float 
    Iteration: int  
    NextCheck: dt.datetime
    
    def __init__(self, params:dict):
        ATradingStrategy.__init__(self)
        self.StartPrice = params['startPrice']
        self.MaSteps = params['maSteps']
        self.CheckInterval = dt.timedelta(minutes = params['checkInterval'])
        self.Spread = params['spread']
        
        
    def UpdateStateAndTrade(self, price, p, date, result: StrategyResult, isLastPeriod):
        fee = 0
        if result.VOBBuy[p] > price and result.HoldingABop[p] > 0:
            buy = result.HoldingABop[p] / price
            if not isLastPeriod:
                result.HoldingBBop[p + 1] = result.HoldingBBop[p] + buy
                result.HoldingABop[p + 1] = 0
            result.BuyAmount[p] = buy
            fee = 0.25 
        elif result.VOBSell[p] < price and result.HoldingBBop[p] > 0:
            sell = result.HoldingBBop[p] * price
            if not isLastPeriod:
                result.HoldingABop[p + 1] = result.HoldingABop[p] + sell
                result.HoldingBBop[p + 1] = 0
            result.SellAmount[p] = sell
            fee = 0.25
        elif not isLastPeriod:
            result.HoldingABop[p + 1] = result.HoldingABop[p]
            result.HoldingBBop[p + 1] = result.HoldingBBop[p]
                
        result.TotalHoldingsInABop[p] = result.HoldingABop[p] + result.HoldingBBop[p] * price - result.CumFees[p]
        
        if date >= self.NextCheck:
            self.NextCheck += self.CheckInterval        
            if self.Iteration % self.MaSteps == 1:
                self.MAPricePop = self.MAPrice
            self.MAPrice -= (self.MAPricePop / self.MaSteps)
            self.MAPrice += (price / self.MaSteps)
            self.Iteration += 1
            fee += 0.5      

        
        result.Price[p] = price
        if not isLastPeriod:
            result.VOBBuy[p + 1] = self.MAPrice / (1 + self.Spread)
            result.VOBSell[p + 1] = self.MAPrice * (1 + self.Spread)
            result.CumFees[p + 1] = result.CumFees[p] + fee
    
    def SetInitialState(self, result: StrategyResult):
        result.VOBBuy[0] = self.StartPrice / (1 + self.Spread)
        result.VOBSell[0] = self.StartPrice * (1 + self.Spread)
        self.MAPrice = self.MAPricePop = self.StartPrice
        self.Iteration = 1
        self.NextCheck = result.DateGrid[0]
    
    @staticmethod
    def getstrategyparams(pricehistory:PriceHistory, simparamslist:list[dict]):
        paramsList = []
        for params in simparamslist:
            startDate = params['startDate']
            endDate = params['endDate']
            days = (endDate-startDate).days
            startPrice = pricehistory.getprice(startDate)
            for checkInterval in [round(x*60) for x in [0.5,1,2,4,6,8,12,16,24]]:
                maxMaSteps = min(math.floor(24*60*max(days-1,1)/checkInterval),12)
                for maSteps in range(2,maxMaSteps,1):
                    for spreadPct in [1.5,2.5,5,7.5,10,15,25,30,35,40,45,50,75,100]:
                        strategyParams = {'startPrice':startPrice,'maSteps':maSteps, 'checkInterval':checkInterval, 'spread':spreadPct/1000 }
                        paramsList.append({'strategyParams':strategyParams, 'priceHistory':pricehistory,'simulationParams':params})
        return paramsList
            