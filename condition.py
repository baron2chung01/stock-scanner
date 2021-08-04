import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def MA(df, N, attri):
    return df[attri].rolling(window=N).mean()

def HHV(df, N, time=-1):
    return df['High'].rolling(window=N).max()[time]

def LLV(df, N, time=-1):
    return df['Low'].rolling(window=N).min()[time]

def REF(df, N, time=-1):
    return df[time-N]

def condition_1245(current_price,ma50,ma150,ma200):
    if current_price>ma150>ma200 and ma50>ma200 and current_price>ma50:
        return True
    else:
        return False

def condition_3(ma200_increasing,time=-1):
    if ma200_increasing[time] > ma200_increasing[time-20]:
        return True
    else:
        return False

def condition_67(current_price,low52week,high52week):
    if current_price > 1.3*low52week and 0.75*high52week <= current_price <= 1.25*high52week:
        return True
    else:
        return False

def vol_range(df,time=-1):
    if df['Volume'][time] > 50000:
        return True
    else:
        return False

def VCP_Detection(df,current_price,time=-1):
    VolTf=50
    PVLimit=0.1
    IsPivot_cond=0

    # Volume must be decreasing

    VMA = MA(df,VolTf,'Volume')
    x = np.array(range(1,VolTf+1)).reshape((-1,1))
    y = np.array(VMA)[time-50:time]
    model = LinearRegression().fit(x, y)
    VolDecreasing = model.coef_ < 0

    # High must be at the start of pivot
    # Low must not be at the end of pivot
    # Reference to 3 - 10 days
    # Pivot width < 10%

    for PivotLength in range(5,10):
        PivotHighPrice = HHV(df, PivotLength,time)
        PivotLowPrice = LLV(df, PivotLength,time)
        PivotWidth = (PivotHighPrice - PivotLowPrice)/current_price
        PivotStartHP = REF(df['High'], PivotLength-1,time)
        PivotEndLP = REF(df['Low'],0,time)
        IsPivot = PivotWidth < PVLimit and PivotHighPrice == PivotStartHP and PivotLowPrice != PivotEndLP
        IsPivot_cond = IsPivot_cond or IsPivot

        # Volume inside pivot must be below 50VMA

        VolDryUp = True
        for i in range(PivotLength):
            VolDryUp = VolDryUp and REF(df['Volume'],i,time) < REF(VMA,i,time)
            cond = VolDecreasing and IsPivot_cond and VolDryUp

        if cond == 1:
            # print('Pivot Length: ',PivotLength)
            break
    # print(f'VCP Condition: {cond}')
    return cond

def calculate_macd(df, PRICE_NAME, period1, period2, period3): 
    # default MACD period values are: period1 = 26, period2 = 12, period3 = 9.
    EMA_1 = df[PRICE_NAME].ewm(span=period1, adjust=False).mean()
    EMA_2 = df[PRICE_NAME].ewm(span=period2, adjust=False).mean()
    MACD_line = EMA_2 - EMA_1
    MACD_Signal_line = MACD_line.ewm(span=period3, adjust=False).mean()
    return MACD_line, MACD_Signal_line

# def cross_macd(array1,array2):
#   # index: -1 or len()-1
#   # array1: MACD line, array2: MACD Signal
#   if array1[len(array1)-2]<=array2[len(array2)-2] and array1[len(array1)-1]>array2[len(array2)-1]:
#     # MACD line surpasses MACD Signal
#     return 1
#   else:
#     return 0

def macd_cond(array1,array2,time=-1):
    # array1: MACD linel
    # MACD > 0 and MACD increasing
    if (array1[time] > array2[time]) and array2[time] > 0:
        # print(f'MACD cond: 1')
        return 1
    else:
        # print(f'MACD cond: 0')
        return 0