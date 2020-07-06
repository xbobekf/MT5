from period import period,periodHigh,periodLow
import MetaTrader5 as mt5
from mpl_finance import candlestick2_ohlc
from grad import grad
from makeTrade import startTrade,stopTrade
import time
import sys
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import matplotlib.animation as animation
import matplotlib.ticker as ticker
from period import period,periodHigh,periodLow

fig, ax1 = plt.subplots()

if(sys.argv[1]==None):
    pair = "ETHUSD."
else:
    pair = sys.argv[1]

timeframe = mt5.TIMEFRAME_M1
array = 200

if not mt5.initialize():
    print("initialize() failed, error code =",mt5.last_error())
    quit()

def animate(i):
    ax1.clear()
    rates = mt5.copy_rates_from(pair, timeframe, datetime.now(), array)
    rates_frame = pd.DataFrame(rates)
    
    candlestick2_ohlc(ax1,rates_frame['open'],rates_frame['high'],rates_frame['low'],rates_frame['close'],width=0.6)
    xdate = [datetime.fromtimestamp(i) for i in rates_frame['time']]

    ax1.xaxis.set_major_locator(ticker.MaxNLocator(6))

    def mydate(x,pos):
        try:
            return xdate[int(x)]
        except IndexError:
            return ''

    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(mydate))

    fig.autofmt_xdate()
    fig.tight_layout()

    highMA = periodHigh(pair,4,timeframe,array)
    lowMA = periodLow(pair,4,timeframe,array)
    rates7de = period(pair,7,timeframe,array)
    rates25de = period(pair,25,timeframe,array)
    rates99de = period(pair,99,timeframe,array)

    ax1.plot(lowMA)
    ax1.plot(highMA)
    ax1.plot(rates99de)
    ax1.plot(rates25de)
    ax1.plot(rates7de)


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()