import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from condition import *

test_Date = datetime(2021,1,4)
# scan_temp = []
# test_Date = (test_Date - timedelta(days=1)).strftime('%Y-%m-%d')
# scan_temp_df = pd.read_csv('output\Stocks worth buying_midcap_{}.csv'.format(test_Date), header = None)
# TEMP = scan_temp_df.values.tolist()[1:]
# for stock in TEMP:
#     stock = stock[0][3:]
#     scan_temp.append(stock)
# print(scan_temp)
test_Date = test_Date + timedelta(days = 1)
print(test_Date)