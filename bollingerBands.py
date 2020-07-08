from period import period,periodHigh,periodLow
import MetaTrader5 as mt5
from makeTrade import startTrade,stopTrade
from datetime import datetime
import pandas as pd
import sys
import time
if(sys.argv[1]==None):
    pair = "ETHUSD."
else:
    pair = sys.argv[1]

timeframe = mt5.TIMEFRAME_H6
array = 10
lot = 50.0
deviation = 20
signal = ''
prevSignal = ''
orders = 0

while True:

    signal = ''
    #print(prevSignal)
    highMA = periodHigh(pair,10,timeframe,array)
    lowMA = periodLow(pair,10,timeframe,array)

    ask = mt5.symbol_info_tick(pair).ask #BUY
    bid = mt5.symbol_info_tick(pair).bid #SELL
    point = mt5.symbol_info(pair).point
    price = 0
    tradeType = 0 

    #print('symbol: ',pair)
    #print('bid: ', bid, 'ask: ', ask)
    #print('speread: ', ask-bid)

    #print('BUY: ',(ask-lowMA[-1])/(highMA[-1]-lowMA[-1]))
    #print('SELL: ',(bid-lowMA[-1])/(highMA[-1]-lowMA[-1]))

    #print('########################################')
    if(orders==0):
   
        if((ask-lowMA[-1])/(highMA[-1]-lowMA[-1])>1.0):
            signal = 'BUY'
            price = ask
            tradeType= mt5.ORDER_TYPE_BUY

        if((bid-lowMA[-1])/(highMA[-1]-lowMA[-1])<0.0):
            signal = 'SELL'
            price = bid
            tradeType= mt5.ORDER_TYPE_SELL
        
        if(signal!=''):
            result = startTrade(pair, lot, price, tradeType)
            prevSignal = signal
            orders = 1
            time.sleep(1)
    
    elif(orders==1):
        if(prevSignal=='BUY'):
            if((ask-lowMA[-1])/(highMA[-1]-lowMA[-1])<0.85):
                price = bid
                position_id=result.order
                stopTrade(pair, lot, price, position_id, tradeType)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    orders = 0
        
        if(prevSignal=='SELL'):
            if((bid-lowMA[-1])/(highMA[-1]-lowMA[-1])>0.15):
                price = ask
                position_id=result.order
                result = stopTrade(pair, lot, price, position_id, tradeType)
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    orders = 0


    #print(signal)
    #print('########################################')




