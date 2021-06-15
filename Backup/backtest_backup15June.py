import pandas as pd
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

stocks_owned = []
profit_stocks = []
loser_stocks = []
count_profit = 0
count_lose = 0
test_startDate = datetime(2021,1,4)
test_endDate = datetime(2021,2,1)
current_price = 0
test_Date = test_startDate

while test_Date <= test_endDate:
    print(f"Date is {test_Date}")
    stocks_scanned = stock_screener('midcap', test_Date())
    # table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_400_companies')
    # s_p = table[0]
    # stocks_scanned = s_p['Ticker symbol'].tolist()[0:10]
    for i in range(len(stocks_scanned)):
        if stocks_scanned[i] not in stocks_owned:
            stocks_owned.append(stocks_scanned[i])
            print(f'Bought {stocks_scanned[i]}')
    
    for i in range(len(stocks_owned)-1,-1,-1):
        # fetch current price of stock concerned
        df = web.DataReader(stocks_owned[i], 'yahoo', test_startDate.strftime('%Y-%m-%d'), test_endDate.strftime('%Y-%m-%d'))
        # df = web.DataReader(symbols[i], 'yahoo', startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'))
        bought_price = df['Close'][0]
        current_price = df['Close'][i]
        # get data

        if (current_price >= bought_price * (1 + take_profit)):
            count_profit += 1
            profit_stocks.append(stocks_owned[i])
            Difference = current_price - bought_price
            Money = Money + Difference
            print(f'Current price of {stocks_owned[i]} is {current_price}')
            print(f'Sold {stocks_owned[i]} and earned ${Difference}')
            stocks_owned.remove(stocks_owned[i])

        elif (current_price <= bought_price * (1 - stop_loss)):
            count_lose += 1
            loser_stocks.append(stocks_owned[i])
            Difference = current_price - bought_price
            Money = Money + Difference
            print(f'Current price of {stocks_owned[i]} is {current_price}')
            print(f'Sold {stocks_owned[i]} and lost ${Difference}')
            stocks_owned.remove(stocks_owned[i])

    test_Date = test_Date + timedelta(days = 1)

print(f'I have ${Money} haha')