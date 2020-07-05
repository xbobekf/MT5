from period import period
import MetaTrader5 as mt5
from grad import grad
from makeTrade import startTrade,stopTrade
import time
import sys

if(sys.argv[1]==None):
    pair = "ZECETH"
else:
    pair = sys.argv[1]

timeframe = mt5.TIMEFRAME_M1
array = 10
lot = 50.0
deviation = 20
signal = ''
prevSignal = ''
orders = 0

while True:
    
    rates7de = period(pair,7,timeframe,array)
    rates25de = period(pair,25,timeframe,array)
    rates99de = period(pair,99,timeframe,array)

    r7g = grad(rates7de)
    r25g = grad(rates25de)
    #r99g = grad(rates99de) 

    ask = mt5.symbol_info_tick(pair).ask #BUY
    bid = mt5.symbol_info_tick(pair).bid #SELL
    point = mt5.symbol_info(pair).point
    price = 0
    tradeType = 0 

    print('symbol: ',pair)
    print('bid: ', bid, 'ask: ', ask)
    print('speread: ', ask-bid)

    print('##############################################################################################')

    if((r25g == 'FALLING') and (r7g == 'RISING')):
        if(bid > rates99de[0]*1.02):
            signal = 'SELL'
            price = bid
            tradeType= mt5.ORDER_TYPE_SELL


    elif((r25g == 'RISING') and (r7g == 'FALLING')):
        if(ask < rates99de[0]*0.98):
            signal = 'BUY'
            price = ask
            tradeType= mt5.ORDER_TYPE_BUY


    print(signal)
    print('##############################################################################################')
    
    if( signal != prevSignal ):

        prevSignal = signal

        if(orders==0):
            
            result = startTrade(pair, lot, price, tradeType)
            orders = 1

        elif (orders==1):
            
            position_id=result.order
            stopTrade(pair, lot, price, position_id, tradeType)
            result = startTrade(pair, lot, price, tradeType)
    
    time.sleep(1)