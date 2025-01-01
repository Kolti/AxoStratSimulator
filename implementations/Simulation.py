import sys
sys.path.append('C:/Users/user/Documents/GitHub/AxoStratSimulator/')

import TapToolsConnector as ttc
from AxoMAv1Strategy import AxoMAv1Strategy
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from PriceHistory import PriceHistory
import os
from varname import nameof
from infrastructure import DateUtils as dtu

from concurrent.futures import ProcessPoolExecutor
from timeit import default_timer as timer

def RunSinglePath(pathParams:dict):
    priceHistory = pathParams['priceHistory']
    strategyParams = pathParams['strategyParams']
    simParams = pathParams['simulationParams']
    strat = AxoMAv1Strategy(strategyParams)
    #print("Simulating "+str(strategyParams)+str(simParams))
    return strat.SimulateStrategy(priceHistory, simParams)

def Simulate(startAmountA:float, token:str, overall_days:int, interval_days:int,parallel:bool=True):
    print('Simulating: '+token+'.')
    paramsList = AxoMAv1Strategy.get_simparams(startAmountA, token, overall_days, interval_days)
    resultlist = []
    
    if (parallel):
        with ProcessPoolExecutor(max_workers=4) as executor:
            for params, result in zip(paramsList, executor.map(RunSinglePath, paramsList)):
                startDate = params['simulationParams']['startDate']
                endDate = params['simulationParams']['endDate']
                days = (endDate-startDate).days
                apr = ((result.TotalHoldingsInABop[-1] / result.TotalHoldingsInABop[0]) ** (1.0/days)) -1
                priceApr = ((result.Price[-1] / result.Price[0]) ** (1.0/days)) -1
                surplusApr = apr-priceApr
                numTransactions = sum((x > 0 for x in np.add(result.BuyAmount, result.SellAmount)))
                newresult = [token,nameof(AxoMAv1Strategy),params['simulationParams']['startDate'].strftime("%Y-%m-%d"),params['simulationParams']['endDate'].strftime("%Y-%m-%d"),params['strategyParams']['maSteps']*params['strategyParams']['checkInterval']/60,params['strategyParams']['maSteps'],params['strategyParams']['checkInterval']/60,params['strategyParams']['spread'],apr,priceApr,surplusApr,numTransactions/days,result.CumFees[-1]/days]
                resultlist.append(newresult)
    else:
        for params in paramsList:
            result = RunSinglePath(params)
            startDate = params['simulationParams']['startDate']
            endDate = params['simulationParams']['endDate']
            days = (endDate-startDate).days
            apr = ((result.TotalHoldingsInABop[-1] / result.TotalHoldingsInABop[0]) ** (1.0/days)) -1
            priceApr = ((result.Price[-1] / result.Price[0]) ** (1.0/days)) -1
            surplusApr = apr-priceApr
            numTransactions = sum((x > 0 for x in np.add(result.BuyAmount, result.SellAmount)))
            newresult = [token,nameof(AxoMAv1Strategy),params['simulationParams']['startDate'].strftime("%Y-%m-%d"),params['simulationParams']['endDate'].strftime("%Y-%m-%d"),params['strategyParams']['maSteps']*params['strategyParams']['checkInterval']/60,params['strategyParams']['maSteps'],params['strategyParams']['checkInterval']/60,params['strategyParams']['spread'],apr,priceApr,surplusApr,numTransactions/days,result.CumFees[-1]/days]
            resultlist.append(newresult)
                    
    df = pd.DataFrame(resultlist, columns = ['token','strategy','from','to','maTime','maSteps','updateInterval','spread','return','assetReturn','surplusReturn','numTransactions','totalFees'])
    df = df.groupby(['token','strategy','maTime','maSteps','updateInterval','spread'], as_index=False) \
        .agg(minDailyReturn=('return','min'), avgDailyReturn=('return','mean'),avgDailyAssetReturn=('assetReturn','mean'),avgDailySurplusReturn=('surplusReturn','mean'), avgDailyTransactions=('numTransactions','mean'),avgDailyFees=('totalFees','mean'),count=('from','count'))

    df = df.reset_index().sort_values('avgDailyReturn', ascending=False)
    outputPath = 'C:\\Users\\user\\Documents\\GitHub\\StratSimulator\\outputs'
    fileName = token+'_'+dt.datetime.now().strftime("%Y%m%d_%H%M%S")+'.csv'
    df.to_csv(os.path.join(outputPath,fileName), index=False)

if __name__ == '__main__':
    start = timer()
    Simulate(1000,'snek',14,4,True)
    #Simulate(1000,'axo',14,4)
    #Simulate(1000,'nike',14,4)
    end = timer()
    print(end-start)