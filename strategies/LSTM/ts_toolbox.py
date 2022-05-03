# Author: Chao Li
# cholianli970518@gmail.com
# github: https://github.com/Cholianlll

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from statsmodels.tsa.stattools import adfuller

#! ############################ Data EDA #############################################

# test the sattionarity
def eda_test_stationarity(timeseries):
    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    
    # Print test outputs
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','pvalue','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput.round(4))

#! ############################ Data processing #####################################
    
# Generate the X and y
def dp_generate_X_y(data,col,lag):
    nrow=data.shape[0]
    tmp=data[col]
    
    # print('Raw data mean:',np.mean(tmp),'\nRaw data std:',np.std(tmp))
    tmp=(tmp-np.mean(tmp))/np.std(tmp)

    X=np.zeros((nrow-lag,lag))
    for i in range(nrow-lag):X[i,:lag]=tmp.iloc[i:i+lag]
    y=np.array(tmp[lag:]).reshape((-1,1))
    return (X,y)

# frame a sequence as a supervised learning problem
def dp_timeseries_to_supervised(data, lag=1):
	df = DataFrame(data)
	columns = [df.shift(i) for i in range(1, lag+1)]
	columns.append(df)
	df = concat(columns, axis=1)
	return df

# convert series to supervised learning
def dp_series_to_supervised(data, n_in=1, n_out=1, dropnan=True, y = False):
	'''
	data: pd.DataFrame
	'''
	
	cols, names = list(), list()
	n_vars = data.shape[1]
	col_names = data.columns
	
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(data.shift(i))
		names += [f'{col_names[j]}(t-{i})' for j in range(n_vars)]
  
	if not y:
		# forecast sequence (t, t+1, ... t+n)
		for i in range(0, n_out):
			cols.append(data.shift(-i))
			if i == 0:
				names += [f'{col_names[j]}(t)' for j in range(n_vars)]
			else:
				names += [f'{col_names[j]}(t-{i})' for j in range(n_vars)]
    
	elif y:
		# forecast sequence (t, t+1, ... t+n)
		for i in range(0, n_out):
			cols.append(data[y].shift(-i))
			if i == 0:
				names += [f'{y}(t)']
			else:
				names += [f'{y}(t-{i})']
    
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

# train test split for time series
def dp_train_test_split(X, y = False, train_rate = 0.8):
    '''
    X: pd.DataFrame
    '''
    train_test_idx = int(np.ceil(X.shape[0]*0.8))
    X_train = X[:train_test_idx]
    X_test = X[train_test_idx:]
    
    if y:
        y_train = y[:train_test_idx]
        y_test = y[train_test_idx:]
        return [X_train, y_train, X_test, y_test]
    return [X_train, X_test]

#! #################### Timeseries plotting #################

# plot time series with rolling mean and std
def plot_curve(timeseries, roll = 12):
    # Determing rolling statistics
    rolmean = timeseries.rolling(roll,center=True).mean()
    rolstd = timeseries.rolling(roll,center=True).std()

    # Plot rolling statistics:
    plt.figure(figsize=(15,6))
    plt.plot(timeseries, color='midnightblue',label='Original')
    plt.plot(rolmean, color='orangered', label='Rolling Mean')
    plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.grid(linestyle = "--",color='lightgrey')  
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()  

# plot multiple timeseries
def plot_multiTS(data, cols_idx, date_col):
    
    sns.set_theme(style="darkgrid")

    # cols_idx = [0, 1,3,4]
    features = (len(cols_idx),1)
    date = date_col
    fig, axes = plt.subplots(features[0], features[1], figsize=(features[0]*4,10))

    # data.date = pd.to_datetime(data.date)
    for i in range(features[0]):
        sns.lineplot(x = date,y = data.columns[cols_idx[i]], data = data,ax = axes[i,])
        
    return fig