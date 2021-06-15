import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

# Stage 2 uptrend condition:
# 1,2,4,5: current price > 50-day > 150-day MA > 200-day MA
# 6,7: current price > 1.3*52weeklow and 0.75*52weekhigh < current price < 1.25*52weekhigh
# 3: 200-day MA line is trending up for 4-5 months

def MA(df, N, attri):
    return df[attri].rolling(window=N).mean()

def HHV(df, N):
    return df['High'].rolling(window=N).max()[-1]

def LLV(df, N):
    return df['Low'].rolling(window=N).min()[-1]

def REF(df, N):
    return df[len(df)-N-1]

def condition_1245():
  if current_price > ma50 > ma150 > ma200:
    return True
  else:
    return False

def condition_3():
  for i in range(math.floor(len(ma200_increasing)/5)):
    if ma200_increasing[i*5] > ma200_increasing[(i+1)*5]:
      return False
    else:
      continue
  return True

def condition_67():
  if current_price > 1.3*low52week and 0.75*high52week <= current_price <= 1.25*high52week:
    return True
  else:
    return False
# data.get_quote_yahoo(tickers)['marketCap']

def current_price_range():
  if 0 <= current_price <= 80:
    return True
  else:
    return False

def VCP_Detection():
  VolTf=50
  PVLimit=0.1
  IsPivot_cond=0
  
  # Volume must be decreasing

  VMA = MA(df,VolTf,'Volume')
  x = np.array(range(1,VolTf+1)).reshape((-1,1))
  y = np.array(VMA)[len(VMA)-50:len(VMA)]
  model = LinearRegression().fit(x, y)
  print('Slope=', model.coef_)
  VolDecreasing = model.coef_ < 0

  # High must be at the start of pivot
  # Low must not be at the end of pivot
  # Reference to 3 - 10 days
  # Pivot width < 10%

  for PivotLength in range(5,10):
    PivotHighPrice = HHV(df, PivotLength)
    PivotLowPrice = LLV(df, PivotLength)
    PivotWidth = (PivotHighPrice - PivotLowPrice)/current_price
    PivotStartHP = REF(df['High'], PivotLength-1)
    PivotEndLP = REF(df['Low'],0)
    IsPivot = PivotWidth < PVLimit and PivotHighPrice == PivotStartHP and PivotLowPrice != PivotEndLP
    IsPivot_cond = IsPivot_cond or IsPivot

    # Volume inside pivot must be below 50VMA

    VolDryUp = True
    for i in range(PivotLength):
      VolDryUp = VolDryUp and REF(df['Volume'],i) < REF(VMA,i)
    cond = VolDecreasing and IsPivot_cond and VolDryUp

    if cond == 1:
      print('Pivot Length: ',PivotLength)
      break
  return cond

# table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# s_p = table[0]
s_p = pd.read_csv('nasdaq_midcap_10June.csv', delimiter=',')

stocks_worth_buying = []
stocks_error = []
count_good = 0
count_bad = 0
count_error = 0
symbols = s_p['Symbol'].tolist()
# print(symbols)
# symbols = ['TSLA']

todayDate = datetime.today()
endDate = todayDate - timedelta(days = 1)
startDate = endDate - timedelta(days = 365)
print('Scan date: ',endDate.strftime('%Y-%m-%d'))

for i in range(len(symbols)):
  try:
    df = web.DataReader(symbols[i], 'yahoo', startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'))
    
    df['MovingAverage200'] = df['Close'].rolling(window=200).mean()
    ma200_increasing = df['MovingAverage200'].tolist()

    current_price = float(df.iloc[-1]['Close'])
    ma50 = MA(df,50,'Close')[-1]
    ma150 = MA(df,150,'Close')[-1]
    ma200 = MA(df,200,'Close')[-1]
    low52week=LLV(df,252)
    high52week=HHV(df,252)

    print(f'Stock: {symbols[i]}')
    # print(f'Current price: {current_price}')
    # print(f'ma50: {ma50}')
    # print(f'ma150: {ma150}')
    # print(f'ma200: {ma200}')
    # print(f'low52week: {low52week}')
    # print(f'high52week: {high52week}')

    if condition_1245() and condition_67() and condition_3() and VCP_Detection():
      print('Good')
      count_good=count_good+1
      stocks_worth_buying.append('31#' + symbols[i])
    else:
      print('Bad')
      count_bad=count_bad+1
  except:
     print(f'Stock: {symbols[i]}')
     print("Something's wrong")
     count_error=count_error+1
     stocks_error.append(symbols[i])
futuexport = pd.DataFrame(stocks_worth_buying)
filename = 'Stocks worth buying_mid_{}.csv'.format(endDate.strftime('%Y-%m-%d'))
futuexport.to_csv(filename, index=False)

# now scan small cap
# table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
# s_p = table[0]
s_p = pd.read_csv('nasdaq_smallcap_10June.csv', delimiter=',')

stocks_worth_buying = []
stocks_error = []
count_good = 0
count_bad = 0
count_error = 0
symbols = s_p['Symbol'].tolist()

for i in range(len(symbols)):
  try:
    df = web.DataReader(symbols[i], 'yahoo', startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'))
    
    df['MovingAverage200'] = df['Close'].rolling(window=200).mean()
    ma200_increasing = df['MovingAverage200'].tolist()

    current_price = float(df.iloc[-1]['Close'])
    ma50 = MA(df,50,'Close')[-1]
    ma150 = MA(df,150,'Close')[-1]
    ma200 = MA(df,200,'Close')[-1]
    low52week=LLV(df,252)
    high52week=HHV(df,252)

    print(f'Stock: {symbols[i]}')
    # print(f'Current price: {current_price}')
    # print(f'ma50: {ma50}')
    # print(f'ma150: {ma150}')
    # print(f'ma200: {ma200}')
    # print(f'low52week: {low52week}')
    # print(f'high52week: {high52week}')

    if condition_1245() and condition_67() and condition_3() and VCP_Detection() and current_price_range():
      print('Good')
      count_good=count_good+1
      stocks_worth_buying.append('31#' + symbols[i])
    else:
      print('Bad')
      count_bad=count_bad+1
  except:
     print(f'Stock: {symbols[i]}')
     print("Something's wrong")
     count_error=count_error+1
     stocks_error.append(symbols[i])
futuexport = pd.DataFrame(stocks_worth_buying)
filename = 'Stocks worth buying_small_{}.csv'.format(endDate.strftime('%Y-%m-%d'))
futuexport.to_csv(filename, index=False)
print('Program ends.')
# try https://chartink.com/screener/volatility-compression