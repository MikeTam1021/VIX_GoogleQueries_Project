import numpy as np
from pandas_datareader import data
import pandas as pd
from sklearn import linear_model
from copy import deepcopy
from datetime import date, timedelta

"""gathering the query and VIX data from the internet here."""

data_lis = []

root_ext = 'GOOGLEINDEX_US:'

indices = ['ADVERT', 'AIRTVL', 'AUTOBY', 'AUTOFI', 'AUTO', 'BIZIND', 'BNKRPT',
           'COMLND', 'COMPUT', 'CONSTR', 'CRCARD', 'DURBLE', 'EDUCAT',
           'INVEST', 'FINPLN', 'FURNTR', 'INSUR', 'JOBS', 'LUXURY', 'MOBILE',
           'MTGE', 'RLEST', 'RENTAL', 'SHOP', 'SMALLBIZ', 'TRAVEL', 'UNEMPL']

for ind in indices:        
    data_lis.append(data.DataReader(root_ext + ind, 'google').Close)         
    data_lis[-1].name = ind

first_date = data_lis[0].index[0]
last_date = data_lis[0].index[-1]

dataVIX = data.DataReader('^VIX', 'yahoo', first_date, last_date)
dataVIX.columns = ['Open', 'High', 'Low', 'VIX', 'vol', 'adj']
data_lis.append((dataVIX.VIX))

frame_queries_VIX = pd.concat(data_lis, join= 'outer', axis = 1)

"""Tamillow's Algorithm. The goal is to optimize leading indicators.
Method: 
1) create a matrix of Correlations with the VIX lagging all indices.
2) find the row that maximizes the absolute value of the correlation for each index.
3) shift the index in the original DataFrame by this many rows"""


number_of_days = last_date.date() - first_date.date()
quarter = number_of_days.days / 4

core_corr_lis = []
frame_shifts = deepcopy(frame_queries_VIX)

for shift_per in range(0, -quarter, -1):
    frame_shifts['VIX'] = frame_queries_VIX['VIX'].shift(periods=shift_per)
    corr_matrix = frame_shifts.dropna().corr(method = 'pearson')    
    core_corr_lis +=  [[corr_matrix['VIX'].loc[ind] for ind in indices]]

corr_serieses = pd.DataFrame(core_corr_lis, columns=[ind for ind in indices])

now = date.today()
date = last_date.date()

difference = now - date

shift_rows = []
for ind in indices:    
    i = corr_serieses[ind][corr_serieses.index > (difference.days + 31) ]\
        .abs().idxmax()
    m = corr_serieses[ind].loc[i]
    shift_rows.append(i)

futr_dates = [last_date + timedelta(days=i) for i in range(1,quarter+2)]

prediction_mat = frame_queries_VIX[-quarter-1:].drop(['VIX'], 1)

dataframe_shifts = deepcopy(frame_queries_VIX)

pack_sift = zip(indices, shift_rows)

for ind, st in pack_sift:
    dataframe_shifts[ind] = frame_queries_VIX[ind].shift(periods=st)
    prediction_mat[ind] = frame_queries_VIX[ind].shift(periods=-(quarter-st))

prediction_mat.index = futr_dates

dataframe_shifts = dataframe_shifts.dropna()
prediction_mat = prediction_mat.dropna()

"""setting up our machine learning linear model."""

X = np.array(dataframe_shifts.loc[:,:'UNEMPL']) 
y = np.array(dataframe_shifts.loc[:,'VIX'])

P = np.array(prediction_mat)

tt = -30
features_train = X[:tt]
features_test = X[tt:]

targets_train = y[:tt]
targets_test = y[tt:]

model_line = linear_model.LinearRegression()
model_line.fit(features_train, targets_train)
