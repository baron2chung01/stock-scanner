import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from condition import *
 
stock_list = ['TSLA','AAPL','SNAP','TSM'] # please loop this as well

df = web.DataReader('TSLA', 'yahoo', datetime(2020,1,1).strftime('%Y-%m-%d'), datetime(2020,3,1).strftime('%Y-%m-%d'))
print(df)
print(df.index.get_loc(datetime(2020,1,7).strftime('%Y-%m-%d')))
print(datetime(2020,1,1).strftime('%Y-%m-%d'))
print('prinprintprintprint')
