import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from condition import *
from finviz.screener import Screener

# Stage 2 uptrend condition:
# 1,2,4,5: current price > 50-day > 150-day MA > 200-day MA
# 6,7: current price > 1.3*52weeklow and 0.75*52weekhigh < current price < 1.25*52weekhigh
# 3: 200-day MA line is trending up for 4-5 months
def stock_screen(scanDate):

    price_list = []
    bought_date = []
    stocks_worth_buying = []
    futu_list = []
    stocks_error = []
    count_good = 0
    count_bad = 0
    count_error = 0

    filters = ['sh_curvol_o200', 'sh_price_o10', 'ta_highlow52w_a30h', 'ta_sma200_sa50', 'ta_sma50_pa']
    stock_list = Screener(filters=filters, table='Performance')
    symbols = []
    for stock in stock_list:
        symbols.append(stock['Ticker'])

    todayDate = scanDate
    endDate = todayDate - timedelta(days = 1)
    startDate = endDate - timedelta(days = 365)
    print('Scan date: ',endDate.strftime('%Y-%m-%d'))

    for i in range(len(symbols)):
        try:
            df = web.DataReader(symbols[i], 'yahoo', startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'))
            
            # get data
            df['MovingAverage200'] = df['Close'].rolling(window=200).mean()
            ma200_increasing = df['MovingAverage200'].tolist()
            current_price = float(df['Close'][-1])
            ma50 = MA(df,50,'Close')[-1]
            ma150 = MA(df,150,'Close')[-1]
            ma200 = MA(df,200,'Close')[-1]
            low52week=LLV(df,252)
            high52week=HHV(df,252)
            MACD_line, MACD_Signal_line = calculate_macd(df, 'Close', 26, 12, 9)

            print(f'Stock: {symbols[i]}')
            print(f'Current price: {current_price}')
            print(f'ma50: {ma50}')
            print(f'ma150: {ma150}')
            print(f'ma200: {ma200}')
            print(f'low52week: {low52week}')
            print(f'high52week: {high52week}')

            if condition_1245(current_price,ma50,ma150,ma200) and condition_67(current_price,low52week,high52week) and condition_3(ma200_increasing) and vol_range(df) and VCP_Detection(df,current_price):

                print('Good')
                count_good=count_good+1
                stocks_worth_buying.append(symbols[i])
                futu_list.append('31#' + symbols[i])
                bought_date.append(scanDate)
                price_list.append(current_price)
            
            else:
                print('Bad')
                count_bad=count_bad+1

        except:
            print(f'Stock: {symbols[i]}')
            print("Something's wrong")
            count_error=count_error+1
            stocks_error.append(symbols[i])


    futuexport = pd.DataFrame(futu_list)
    filepath = 'output\Stocks worth buying_{}_{}.csv'.format(cap,endDate.strftime('%Y-%m-%d'))
    futuexport.to_csv(filepath, index = False)
    print(stocks_worth_buying)
    print(f'Scanning of {scanDate} is complete')
    return stocks_worth_buying