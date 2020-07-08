import MetaTrader5 as mt5
import time

def startTrade(symbol, lot, price, tradeType):

    deviation = 20
    
    request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": tradeType,
    "price": price,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK,
    }

    # send a trading request
    result = mt5.order_send(request)

    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation))
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
    
        print("2. order_send failed, retcode={}".format(result.retcode))
    
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
    
        for field in result_dict.keys():
    
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
    
            if field=="request":
    
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
    
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    
        print("shutdown() and quit")
    
        mt5.shutdown()
        quit()
    
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))
    time.sleep(2)

    return result

def stopTrade(symbol, lot, price, position_id, tradeType):

    deviation=20

    request={
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": tradeType,
    "position": position_id,
    "price": price,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK,
    }

    # send a trading request
    result=mt5.order_send(request)

    # check the execution result
    print("3. close position #{}: sell {} {} lots at {} with deviation={} points".format(position_id,symbol,lot,price,deviation))

    if result.retcode != mt5.TRADE_RETCODE_DONE:
 
        print("4. order_send failed, retcode={}".format(result.retcode))
        print("   result",result)  

    else:
  
        print("4. position #{} closed, {}".format(position_id,result))
        
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        
        for field in result_dict.keys():
      
            print("   {}={}".format(field,result_dict[field]))
        
            # if this is a trading request structure, display it element by element as well
            if field=="request":
        
                traderequest_dict=result_dict[field]._asdict()
        
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    return result