from datetime import datetime
import MetaTrader5 as mt5
import time
import collections

def period(pair, period, timeframe, array):

    ratesDE = collections.deque([0.0] *array)

    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()

    currentTime = datetime.now()

    rates = mt5.copy_rates_from(pair, timeframe, currentTime, period+array)

    for arr in range(array):
        calculated=0
        for pos in range(period):
            calculated+=rates[arr+pos][4]
        ratesDE.appendleft(calculated/period)
        ratesDE.pop()

    return ratesDE