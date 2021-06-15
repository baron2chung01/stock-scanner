import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from condition import *
from stock_screener import *

stock_screen('midcap',datetime(2018,1,1))
stock_screen('midcap',datetime(2018,1,2))
stock_screen('midcap',datetime(2018,1,3))
stock_screen('midcap',datetime(2018,1,4))
stock_screen('midcap',datetime(2018,1,5))
