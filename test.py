import pandas as pd
import pandas_datareader as web
from pandas_datareader import data
import math
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from condition import *
from finviz.screener import Screener
cap = 'small'
filter_cap = 'cap_' + cap
print(filter_cap)