import unittest
import sys
sys.path.append('C:/Users/user/Documents/GitHub/StratSimulator/')
import datetime as dt
from implementations import PriceHistory as ph
from timeit import default_timer as timer
import math
import numpy as np

class pricehistorytest(unittest.TestCase):
    def test_getprice(self):
        startDate = dt.datetime(year=2024,month=7,day=1)
        increment = dt.timedelta(days=1)
        dates = [startDate + x*increment for x in range(0,10)]
        prices = [1-x/10 for x in range(0,10)]
        
        priceHist = ph.PriceHistory(dates, prices)
        
        date1 = dt.datetime(year=2024,month=7,day=4,hour=2)
        price1 = priceHist.getprice(date1)
        
        self.assertEqual(price1, 0.7)
            
        date2 = dt.datetime(year=2024,month=7,day=4,hour=3)
        price2 = priceHist.getprice(date2)
        self.assertEqual(price2, price1)
        
        date3 = dt.datetime(year=2024,month=7,day=6,hour=0)
        price3 = priceHist.getprice(date3)
        self.assertEqual(price3, 0.5)
        
    def test_projecttogrid(self):
        startDate = dt.datetime(year=2024,month=7,day=1)
        increment = dt.timedelta(days=1)
        dates = [startDate + x*increment for x in range(0,10)]
        prices = [1-x/10 for x in range(0,10)]
        
        priceHist = ph.PriceHistory(dates, prices)
        
        simstart = dt.datetime(year=2024,month=7,day=3,hour=5)
        simend = dt.datetime(year=2024,month=7,day=8,hour=23)
        
        gridhist = priceHist.project_to_grid(simstart, simend, dt.timedelta(days=1))
        self.assertTrue(np.allclose(gridhist.Prices,np.array([0.8,0.7,0.6,0.5,0.4])))
        
    def test_speed(self):
        self.__speedTest(100000)    
    
    def __speedTest(self, n:int):
        startDate = dt.datetime(year=2024,month=7,day=1,hour=2,minute=10)
        increment = dt.timedelta(minutes=3)
        dates = [startDate + x*increment for x in range(0,n)]
        prices = [1-x/n for x in range(0,n)]
        priceHist = ph.PriceHistory(dates, prices)
        
        start = timer()
        result = [priceHist.getprice(date+dt.timedelta(seconds=1)) for date in dates]              
        end = timer()
        print(end-start)
        return result   

#if __name__ == '__main__':
#    unittest.main()