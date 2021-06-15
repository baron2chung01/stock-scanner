import pandas as pd
from pandas.core.frame import DataFrame
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from main import *

stop_loss = 0.06
take_profit = 0.1
trans_cost = 2
total_cost = 0
Money = 0

stock_list = []
profit_stocks = []
loser_stocks = []
bought_date = []
count_profit = 0
count_lose = 0
test_startDate = datetime(2021,1,4)
test_endDate = datetime(2021,2,1)
current_price = 0
test_Date = test_startDate

# retrieve stock list to be backtested
while test_Date <= test_endDate:
    print(f"Date is {test_Date}")
    scan_temp = stock_screener('midcap', test_Date())

    for stock in scan_temp:
        if stock not in stock_list:
            # df = web.DataReader(stocks_scanned[i], 'yahoo', test_startDate.strftime('%Y-%m-%d'), test_endDate.strftime('%Y-%m-%d'))
            stock_list.append(stock)
            bought_date.append(test_Date)

    test_Date = test_Date + timedelta(days = 1)

# execute stocks one by one
data = {'Stock': stock_list, 'Bought Date': bought_date}
df_data = pd.DataFrame(data)
for stock in stock_list:
    