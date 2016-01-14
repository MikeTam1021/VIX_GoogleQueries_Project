import numpy as np
from pandas_datareader import data
import pandas as pd


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
