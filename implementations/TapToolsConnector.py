import requests
import json
import datetime as dt
import math
from PriceHistory import PriceHistory

__url = 'https://openapi.taptools.io/api/v1/token/ohlcv'
__headers = { 'Accept': 'application/json', 'x-api-key': 'xxx'} #needs TapTools API key instead of xxx
__tokenIds = {'snek':'279c909f348e533da5808898f87f9a14bb2c3dfbbacccd631d927a3f534e454b',
              'axo':'420000029ad9527271b1b1e3c27ee065c18df70a4a4cfc3093a41a4441584f',
              'nike':'c881c20e49dbaca3ff6cef365969354150983230c39520b917f5cf7c4e696b65',
              'indy':'533bb94a8850ee3ccbe483106489399112b74c905342cb1792a797a0494e4459',
              'djed':'8db269c3ec630e06ae29f74bc39edd1f87c819f1056206e879a1cd61446a65644d6963726f555344',
              'wmt':'1d7f33bd23d85e1a25d87d86fac4f199c3197a2f7afeb662a0f34e1e776f726c646d6f62696c65746f6b656e',
              'hunt':'95a427e384527065f2f8946f5e86320d0117839a5e98ea2c0b55fb0048554e54'}

def GetPriceHistoryPath(asset, timeDelta: dt.timedelta):
        numIntervals = math.ceil(timeDelta / dt.timedelta(minutes=3)) + 1
        id = __tokenIds[asset]
        data = {
                'unit':id, 
                'onchainID': id,
                'interval':'3m',
                'numIntervals':numIntervals,
                }

        response = requests.get(__url, params= data, headers=__headers)
        data = json.loads(response.text)
        dates = [dt.datetime.fromtimestamp(x['time']) for x in data]
        prices = [x['close'] for x in data]
        return PriceHistory(dates, prices)
