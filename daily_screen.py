import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from condition import *
from stock_screener import *
from stock_screener_backtest import *

stock_screen('midcap', datetime.now())
stock_screen('smallcap', datetime.now())

