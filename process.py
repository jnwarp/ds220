import pandas as pd
import numpy as np

class bitpayUSD():
    def __init__(self):
        self.preprocess()
        print(self.df)

    def preprocess(self, period='D'):
        # import the USD price data
        self.df = pd.read_csv(
            'raw/bitpayUSD.csv',
            header=None,
            names=['time', 'usd', 'vol'])

        # convert unix timestamp into usable number
        self.df['time'] = pd.to_datetime(self.df['time'], unit='s')

        # make timestamp the index
        self.df.set_index('time', inplace=True)

        # get daily totals instead of hourly info
        self.df = self.df.resample(period, how={'usd': 'ohlc', 'vol': np.sum})

        # drop empty rows
        self.df = self.df.dropna(axis=0)

bp = bitpayUSD()
bp.df.to_csv('processed/bitpayUSD.csv')
