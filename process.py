import pandas as pd
import numpy as np

class bitpayUSD():
    def __init__(self):
        self.preprocess()
        self.calcVolatility()
        print('\n\nbitpayUSD')
        print('=========')
        print(self.df.describe())

    def preprocess(self, period='D'):
        # import the bitcoin USD price data
        self.df = pd.read_csv(
            'raw/bitpayUSD.csv',
            header=None,
            names=['date', 'usd', 'vol'])

        # convert unix timestamp into usable number
        self.df['date'] = pd.to_datetime(self.df['date'], unit='s')

        # make timestamp the index
        self.df.set_index('date', inplace=True)

        # get daily totals instead of hourly info
        self.df = self.df.resample(period, how={'usd': 'ohlc', 'vol': np.sum})

        # drop empty rows
        self.df = self.df.dropna(axis=0)

    def calcVolatility(self):
        self.df.pct_change().rolling('10D')

class GSPC():
    def __init__(self):
        self.preprocess()
        print('\n\nGSPC')
        print('====')
        print(self.df.describe())

    def preprocess(self):
        # import S&P500 price data
        self.df = pd.read_csv('raw/GSPC.csv')

        self.df.columns = ['date', 'open', 'high', 'low', 'close', 'adj_close', 'vol']


bp = bitpayUSD()
#bp.df.to_csv('processed/bitpayUSD.csv')

#gspc = GSPC()
