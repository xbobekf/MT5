from mpl_finance import candlestick2_ohlc
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime
import numpy as np
import MetaTrader5 as mt5
import sys
import pandas as pd

if(sys.argv[1]==None):
    pair = "ETHUSD."
else:
    pair = sys.argv[1]

if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

timeframe = mt5.TIMEFRAME_M1

quotes = mt5.copy_rates_from(pair, timeframe, datetime.now(), 100)
quotes = pd.DataFrame(quotes)
print(quotes)
fig, ax = plt.subplots()
candlestick2_ohlc(ax,quotes['open'],quotes['high'],quotes['low'],quotes['close'],width=0.6)

xdate = [datetime.fromtimestamp(i) for i in quotes['time']]

ax.xaxis.set_major_locator(ticker.MaxNLocator(6))

def mydate(x,pos):
    try:
        return xdate[int(x)]
    except IndexError:
        return ''

ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

fig.autofmt_xdate()
fig.tight_layout()

plt.show()