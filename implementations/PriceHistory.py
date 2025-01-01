from dataclasses import dataclass
import datetime as dt
import numpy as np
import copy
import math

@dataclass(unsafe_hash=True)
class PriceHistory:
    DateGrid: np.array
    Prices: np.array
    
    def __init__(self, dates, prices):
        self.DateGrid = np.array(dates)
        self.Prices = np.array(prices)
        
    def getprice(self, date):
        index = self.DateGrid.searchsorted(date, 'right') - 1
        return self.Prices[index]
    
    def project_to_grid(self, gridstart: dt.datetime, gridend:dt.datetime, interval:dt.timedelta):
        if gridstart < self.DateGrid[0] or gridstart > self.DateGrid[-1] or gridend < self.DateGrid[0] or gridend > self.DateGrid[-1]:
            raise Exception
        
        numintervals = math.floor((gridend - gridstart) / interval)
        curDate = gridstart       
        i = d = 0
        dates = np.empty(numintervals, dtype=dt.datetime)
        prices = np.zeros(numintervals,dtype = float)
        while d < self.DateGrid.size:
            if self.DateGrid[d] <= curDate and ((d == self.DateGrid.size - 1) or self.DateGrid[d+1] > curDate):
                dates[i] = curDate
                prices[i] = self.Prices[d]
                
                if i >= numintervals - 1:
                    break
                curDate += interval
                i += 1
            else:
                d+=1
        return PriceHistory(dates, prices)