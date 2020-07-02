from datetime import datetime
import MetaTrader5 as mt5
import time
import collections

killer = 0

timeframe = mt5.TIMEFRAME_M1
pair = "ETHUSD."
array = [0.0] * 10

rates7de = collections.deque(array) 
rates25de = collections.deque(array) 
rates99de = collections.deque(array) 

# connect to MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

while(True):
    signal = ''
    currentTime = datetime.now()
    rates7 = mt5.copy_rates_from(pair, timeframe, currentTime, 7)
    rates25 = mt5.copy_rates_from(pair, timeframe, currentTime, 25)
    rates99 = mt5.copy_rates_from(pair, timeframe, currentTime, 99)
    ticks = mt5.copy_ticks_from(pair, currentTime, 1, mt5.COPY_TICKS_ALL)
    
    calculated7 = 0
    for pos in rates7:
        calculated7+=pos[4]
    rates7de.appendleft(calculated7/7)
    rates7de.pop()
    print ('7:', rates7de)

    calculated25 = 0
    for pos in rates25:
        calculated25+=pos[4]
    rates25de.appendleft(calculated25/25)
    rates25de.pop()
    print ('25:', rates25de) 

    calculated99 = 0
    for pos in rates99:
        calculated99+=pos[4]
    rates99de.appendleft(calculated99/99)
    rates99de.pop()
    print ('99:', rates99de)

    print (ticks[0][1]-ticks[0][2])

    if(rates99de[0]<rates99de[-1]):
        r99g ='FALLING'
    else:
        r99g ='RISING'

    if(rates7de[0]<rates7de[-1]):
        r7g = 'FALLING'
    else:
        r7g = 'RISING' 

    if(rates25de[0]<rates25de[-1]):
        r25g = 'FALLING'
    else:
        r25g = 'RISING' 
    
    orders=mt5.orders_get(symbol=pair)

    if orders is None:
        print("No orders on ETHUSD., error code={}".format(mt5.last_error()))
    else:
        print("Total orders on ETHUSD.:",len(orders))
        for order in orders:
            print(order)
    print('bid ',ticks[0][1])
    print('ask ',ticks[0][2])
    
    print('###################################################################################################')

    #(len(orders)==0)
    if(killer>10):
        if((r25g == 'FALLING') and (r7g == 'RISING')):
            if(ticks[0][2]>rates99de[0]*0.97):
                signal = 'SELL'
        elif((r25g == 'RISING') and (r7g == 'FALLING')):
            if(ticks[0][1]<rates99de[0]*1.03):
                signal = 'BUY'
    print(signal)
    killer+=1
    print('###################################################################################################')
    time.sleep(60)

mt5.shutdown()
