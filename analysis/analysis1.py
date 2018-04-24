from statsmodels.tsa.stattools import adfuller
import pandas as pd
import numpy as np
import os
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf


def assembleData(filename, year, flag):
	dataSource = "/Users/tomokitakasawa/Documents/GitHub/ds220/processed/tom/"
	FileLoc = os.path.join(dataSource, filename)
	
	dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
	data = pd.read_csv(FileLoc, parse_dates=['day'], index_col='day',date_parser=dateparse)
	TS_Price = data['price'] 
	if year is not 'none':
		TS_Price = TS_Price[year]

	if flag == 0:
		plt.title('Original data')
		orig = plt.plot(TS_Price, color='blue',label='Original')
		plt.show()
	elif flag == 1:
		return TS_Price


def test_stationarity(timeseries):
    
    #Determing rolling statistics
    #rolmean = pd.rolling_mean(timeseries, window=12)
    rolmean = timeseries.rolling(window=12,center=False).mean()
    #rolstd = pd.rolling_std(timeseries, window=12)
    rolstd = timeseries.rolling(window=12,center=False).std()

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    #plt.show(block=False)
    plt.show()
    
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)



"""
@param: choice
@param: flag		0 for ploting, 1 for returning
"""
def doTransform(TS_Price, choice, flag):

	if choice is 'log':
		plt.title('Transform performed')
		LogTransform = np.log(TS_Price)
		if flag == 1:
			return LogTransform
		plt.plot(LogTransform, color='blue', label='log transform')
		plt.show()
	elif choice is 'sqrt':
		plt.title('Transform performed')
		SqrtTransform = np.sqrt(TS_Price)
		if flag == 1:
			return SqrtTransform
		plt.plot(SqrtTransform, color='red', label='sqrt transform')
		plt.show()
	else:
		print("Error: " + choice + " cannot be selected as transform.")

def MovAvg(logTimeSeries, choice):
	smoothAvg = logTimeSeries.rolling(window=12,center=False).mean()
	if choice is 'smoothAvg':
		print(smoothAvg)
		return smoothAvg
	elif choice is 'plotSmoothAvg':
		plt.plot(logTimeSeries, color='blue', label='log transform')
		plt.plot(smoothAvg, color='red', label='smooth')
		plt.show()
	elif choice is 'movingAvgDiff':
		ts_log_moving_avg_diff = logTimeSeries - smoothAvg
		print(ts_log_moving_avg_diff.head(12))
		return ts_log_moving_avg_diff.head(12)
	else:
		ts_log_moving_avg_diff = logTimeSeries - smoothAvg
		ts_log_moving_avg_diff.dropna(inplace=True)
		test_stationarity(ts_log_moving_avg_diff)


def calcEWMV(LogTransform, choice):
	EWMA = LogTransform.ewm(halflife=12,min_periods=0,adjust=True,ignore_na=False).mean()
	EWMA_diff = LogTransform - EWMA
	if choice is 'getExpWeightedAvg':
		return EWMA
	elif choice is 'getExpWeightedAvg_Diff':
		return EWMA_diff
	elif choice is 'plotExpWeightedAvg':
		plt.plot(LogTransform, color='blue')
		plt.plot(EWMA, color='red')
		plt.show()
	else:
		test_stationarity(EWMA_diff)

def differencing(logTrensform, choice):
	differenncing_LogTransform = logTrensform - logTrensform.shift()
	if choice is 'plot':
		differenncing_LogTransform.dropna(inplace=True)
		test_stationarity(differenncing_LogTransform)
	else:
		return differenncing_LogTransform


def decomposition(LogTransform, flag):
	decomposition = seasonal_decompose(LogTransform)
	trend = decomposition.trend
	seasonal = decomposition.seasonal
	residual = decomposition.resid

	if flag == 0:
		plt.subplot(411)
		plt.plot(LogTransform, label='Original')
		plt.legend(loc='best')
		plt.subplot(412)
		plt.plot(trend, label='Trend')
		plt.legend(loc='best')
		plt.subplot(413)
		plt.plot(seasonal,label='Seasonality')
		plt.legend(loc='best')
		plt.subplot(414)
		plt.plot(residual, label='Residuals')
		plt.legend(loc='best')
		plt.tight_layout()
		plt.show()
	else:
		decomposedResidual = residual
		decomposedResidual.dropna(inplace=True)
		test_stationarity(decomposedResidual)

def testDecomposition():
	ts_log_decompose = residual
	ts_log_decompose.dropna(inplace=True)
	test_stationarity(ts_log_decompose)



def autoCorrelation(differencedTS):
	lag_acf = acf(differencedTS, nlags=20)
	#plt.subplot(121) 
	plt.plot(lag_acf, color='blue')
	plt.axhline(y=0,linestyle='--',color='gray')
	plt.axhline(y=-1.96/np.sqrt(len(differencedTS)),linestyle='--',color='gray')
	plt.axhline(y=1.96/np.sqrt(len(differencedTS)),linestyle='--',color='gray')
	plt.title('Autocorrelation (blue) partial(red)')

	lag_pacf = pacf(differencedTS, nlags=20, method='ols')
	#plt.subplot(122)
	plt.plot(lag_pacf, color='red')
	plt.axhline(y=0,linestyle='--',color='gray')
	plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
	plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
	plt.tight_layout()

	plt.show()

"""
depricated: lol -> No longer used. Just used to compare some of the manipulation methods. Newer one is @ checkStationlityAfterManipulation::method
@param filename: 			(String)	name of file(include csv)
@param year: 				(Srting)	desired year. If 'none', then whole datasets
@param testStationarity: 	(Bool)		whether or not to test staionarity
@param transform:			(String)	'none', 'log', or 'sqrt'
@param smoothing:			(String)	'none' smoothAvg', 'plotSmoothAvg', 'movingAvgDiff', 'plotMovingAvgDiff'
@param expWeightdAvg:		(String)	'getExpWeightedAvg', 'plotExpWeightedAvg', 'getExpWeightedAvg_Diff', 'plotExpWeightedAvg_Diff'

"""
def DataPreparationTerminal(filename, year, testStationarity, transform, smoothing, ewmv, differencing):
	dataSource = "/Users/tomokitakasawa/Documents/GitHub/ds220/processed/tom/"
	FileLoc = os.path.join(dataSource, filename)
	
	dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
	data = pd.read_csv(FileLoc, parse_dates=['day'], index_col='day',date_parser=dateparse)
	TS_Price = data['price'] 
	if year is not 'none':
		TS_Price = TS_Price[year]

	if testStationarity:
		test_stationarity(TS_Price)

	if transform is not 'none':
		doTransform(TS_Price, transform, 0)

	if smoothing is not 'none':
		if smoothing is 'smoothAvg' or 'movingAvgDiff':
			return MovAvg(doTransform(TS_Price, 'log', 1), smoothing)
		elif smoothing is 'plotMovingAvgDiff' or 'plotSmoothAvg':
			MovAvg(doTransform(TS_Price, 'log', 1), smoothing)
		else:
			print("Error at smoothing!!")


	if ewmv is not 'none':
		if ewmv is 'getExpWeightedAvg' or 'getExpWeightedAvg_Diff':
			return calcEWMV(doTransform(TS_Price, 'log', 1), ewmv)
		elif ewmv is 'plotExpWeightedAvg' or 'plotExpWeightedAvg_Diff':
			calcEWMV(doTransform(TS_Price, 'log', 1), ewmv)
		else:
			print('Error at exponential weighted average')
		
		
	if differencing:
		ts_log_diff = doTransform(TS_Price, 'log', 1) - doTransform(TS_Price, 'log', 1).shift()
		ts_log_diff.dropna(inplace=True)
		test_stationarity(ts_log_diff)



"""
Use it for checking stationarity of time series, or do some sort of manipulations
@param method: 			(String)	name of file(include csv)
@param action: 			(Srting)	describe action, 'plot' or 'get'
@param year:			(String)	If you are looking for one year. If not, just put 'none'
"""
def checkStationlityAfterManipulation(method, action, year):
	filename = 'DatePrice_BitCoin.csv'

	if action is 'plot':
		if method is 'MovingAverage':
			return MovAvg(doTransform(assembleData(filename, year, 1), 'log', 1), 'plotMovingAvgDiff')
		elif method is 'ExponentiallyWeightedMovingAverage':
			return calcEWMV(doTransform(assembleData(filename, year, 1), 'log', 1), 'plotExpWeightedAvg_Diff')
		elif method is 'differencing':
			return differencing(doTransform(assembleData(filename, year, 1), 'log', 1), 'plot')
		elif method is 'decomposition':
			return decomposition(doTransform(assembleData(filename, year, 1), 'log', 1), 1)
			#flag 0 to decompose
			# flag 1 to decomposition analysis
		elif method is 'noAction':
			return assembleData(filename, year, 0)
		#
	elif action is 'get':
		if method is 'MovingAverage':
			return MovAvg(doTransform(assembleData(filename, year, 1), 'log', 1), 'movingAvgDiff')
		elif method is 'ExponentiallyWeightedMovingAverage':
			return calcEWMV(doTransform(assembleData(filename, year, 1), 'log', 1), 'getExpWeightedAvg_Diff')
		elif method is 'differencing':
			return differencing(doTransform(assembleData(filename, year, 1), 'log', 1), 'get')
		elif method is 'decomposition':
			return decomposition(doTransform(assembleData(filename, year, 1), 'log', 1), 1)
			#flag 0 to decompose
			# flag 1 to decomposition analysis
		elif method is 'noAction':
			assembleData(filename, year, 1)


ManipulationMethodList = {
	#All action here is either to return or plot
	0: 'noAction', 								# time series
	1: 'MovingAverage', 						# Use of moving average
	2: 'ExponentiallyWeightedMovingAverage', 	# Use of exponential weight moving average
	3: 'differencing', 							# differencing
	4: 'decomposition'							# decomposition
}

ActionList = {
	0: 'plot', 
	1: 'get'
}

year = {
	0: 'none',
	1: '2014',
	2: '2015',
	3: '2016',
	4: '2017',
	5: '2018'
}


diff_Diff = checkStationlityAfterManipulation(ManipulationMethodList[3], ActionList[1], year[0])
autoCorrelation(diff_Diff)


#checkStationlityAfterManipulation(ManipulationMethodList[3], ActionList[0], year[0])






