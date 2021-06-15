import pandas as pd
from pandas.core.frame import DataFrame
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from stock_screener_backtest import *
from condition import *

startyear = 2020
startmonth = 1
startday = 8

endyear = 2020
endmonth = 1
endday = 14

start = datetime(startyear,startmonth,startday)
end = datetime(endyear,endmonth,endday)
test_Date = start
# end = datetime.now()
# scan stock_list
stock_list = []

while test_Date <= end:
    if (0 <= test_Date.weekday() <= 4):
        scan_temp = stock_screen_backtest('midcap', test_Date)

        for stock in scan_temp:

            if stock not in stock_list:
                stock_list.append(stock)

    test_Date = test_Date + timedelta(days = 1)



# stock_list = ['SNAP','TSM','TSLA'] # please loop this as well

for stock in stock_list:

    df = web.DataReader(stock, 'yahoo', (start - timedelta(days=365)).strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    # get data
    df['MovingAverage200'] = df['Close'].rolling(window=200).mean()
    ma200_increasing = df['MovingAverage200'].tolist()

    bp = -1 # buy price
    pos = 0 # position, 1: owning stock, 0:not owning
    num = 0 
    percentchange = []

    for i in range(df.index.get_loc(start.strftime('%Y-%m-%d')),len(df.index)):
        close = df['Close'][i]
        ma50 = MA(df,50,'Close')[i]
        ma150 = MA(df,150,'Close')[i]
        ma200 = MA(df,200,'Close')[i]
        low52week = LLV(df,252,i)
        high52week = HHV(df,252,i)
        MACD_line, MACD_Signal_line = calculate_macd(df, 'Close', 26, 12, 9)

        if (condition_1245(close,ma50,ma150,ma200) and condition_67(close,low52week,high52week) and condition_3(ma200_increasing,i) and vol_range(df,i) and macd_cond(MACD_line, MACD_Signal_line,i) and VCP_Detection(df,close,i)):
            print("Condition satisfied.")
            if (pos == 0):
                bp = close
                pos = 1
                print("Buying now at " + str(bp))

        elif (bp > 0 and (close > 1.1 * bp or close < 0.94 * bp)):
            # take profit @ 10%, stop loss @ 6%
            if (pos == 1):
                pos = 0
                sp = close
                print("Selling now at " + str(sp))
                pc = (sp/bp-1) * 100
                percentchange.append(pc)
    
        if (num == df['Close'].count()-252-1 and pos == 1):
            pos = 0
            sp = close
            print("Selling now at "+str(sp))
            pc = (sp/bp-1)*100
            percentchange.append(pc)
    
        num+=1

    print(percentchange)

    gains = 0
    ng = 0 # number of gains
    losses = 0
    nl = 0 # number of losses
    totalR = 1

    for i in percentchange:
        if(i > 0):
            gains += i
            ng += 1
        else:
            losses += i
            nl += 1
        totalR = totalR * ((i/100) + 1)

    totalR = round((totalR - 1) * 100, 2)

    if(ng > 0):
        avgGain = gains/ng
        maxR = str(max(percentchange))
    else:
        avgGain = 0
        maxR = "undefined"

    if(nl > 0):
        avgLoss = losses/nl
        maxL = str(min(percentchange))
        ratio = str(-avgGain/avgLoss)
    else:
        avgLoss = 0
        maxL = "undefined"
        ratio = "inf"

    if(ng > 0 or nl > 0):
        battingAvg = ng/(ng+nl)
    else:
        battingAvg = 0

    print()
    print("Results for "+ stock +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades")
    print("Batting Avg: "+ str(battingAvg))
    print("Gain/loss ratio: "+ ratio)
    print("Average Gain: "+ str(avgGain))
    print("Average Loss: "+ str(avgLoss))
    print("Max Return: "+ maxR)
    print("Max Loss: "+ maxL)
    print("Total return over " + str(ng + nl) + " trades: " + str(totalR) +"%" )
    print()
    # print("Example return Simulating "+str(n)+ " trades: "+ str(nReturn)+"%" )