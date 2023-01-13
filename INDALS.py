from kiteconnect import KiteConnect
import requests,json,time,datetime, os
import pandas as pd, numpy as np, math
import pickle, redis, telegram, random
import sys
import definitions as defs
rRr = redis.Redis(host='127.0.0.1', port=6379, db=0)
from utility_main import *
# -----------------------
strat_id= 'BN' #sys.argv[1]
if strat_id == 'BN':
    inst_base='BANKNIFTY'; inst_name='NIFTY BANK'; strikes=100; lot_size=25; hedge_far_strike_perc=1/100
    name = 'BANK NIFTY'
else:
    inst_base='NIFTY'; inst_name='NIFTY 50'; strikes=50; lot_size=50; hedge_far_strike_perc=1/100
    name = 'NIFTY'
strat_title = " * IND ALS * " + name
strategy_name= 'IND_ALS ' # sys.argv[2] ;
strategy_name = strategy_name + strat_id
print("#####------------------------------#####")
print("STARTING",strat_title)
print("#####------------------------------#####")

CurrentTime = datetime.datetime.today().time()
time_change = datetime.timedelta(minutes=1)
Test = True
if Test:
    StartTime = datetime.time(CurrentTime.hour, CurrentTime.minute + 1, CurrentTime.second)
    EnterTime = datetime.time(CurrentTime.hour, CurrentTime.minute + 2, CurrentTime.second)
else:
    EnterTime = datetime.time(9, 30, 0)
    StartTime = datetime.time(9,0,0)

# -----------------------

input = ind_straddle_4 = {"EntryTime": EnterTime, "ExitTime": datetime.time(15, 15, 0), "Delta":0, 'TradingAmount':100000, 'TradingQty':1, 
                "SquareOffSL": defs.ONELEGSL, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.YES, "ReEntryTG": defs.YES, "SLEvery":20, "SLPcFar":500,
                "MaxReEnterCounterSL": 6, "MaxReEnterCounterTG": 2, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":30, "TargetPc":70}

#----------------------------
market_start_time = datetime.time(9, 14, 0)
market_close_time = datetime.time(15, 29, 0)   # Let's NOT change it
#---------------
qty_per_lot = 50 

while True:
    decision = market_hours(open_time = datetime.time(9, 5, 0))
    if decision=='OPEN':
        print('##### MARKET OPEN :: Sync in Strategy #####')
        break
    get_up_time=datetime.datetime.fromtimestamp(decision+time.time()).strftime('%H:%M:%S %A, %d-%b-%Y')
    print('Login Credentials will be updated again @ ',get_up_time)
    time.sleep(random.sample([1,2,3],1)[0])
    telegram_msg("Scheduling"+strat_title+  "@ "+get_up_time)
    time.sleep(decision)

# -----------------------

########### Sync with Zerodha #############
sleep_secs = wake_up_time(wakeup_at = StartTime)
time.sleep(sleep_secs)
login_credentials = pickle.loads(rRr.get('login_credentials'))
inst = pickle.loads(rRr.get('inst_df'))
inst_req = pickle.loads(rRr.get('inst_REQ'))
token_info_req = pickle.loads(rRr.get('token_info_REQ'))
inst_req_index = pickle.loads(rRr.get('inst_'+strat_id))
token_info_req_index = pickle.loads(rRr.get('token_info_'+strat_id))

### Calculate remaining expiry days
index_token = inst[inst.name==inst_name]['instrument_token'].iloc[0]
#---------------------
while True:
    try:
        index_price = login_credentials['kite'].ltp(index_token)[str(index_token)]['last_price']
        break
    except:time.sleep(.5)

ATM_price = round(index_price/strikes)*strikes
expiry_date = [y['expiry'] for x,y in token_info_req_index.items() if y['strike']==ATM_price and y['instrument_type']=='CE'][0]
all_remaining_dates = [datetime.datetime.today().date()]
current_date = datetime.datetime.today().date()
while current_date < expiry_date:
    current_date += datetime.timedelta(days=1)
    all_remaining_dates.append(current_date)
all_remaining_dates = [x for x in all_remaining_dates if x not in nse_calendar and x.strftime("%A") not in ['Saturday','Sunday']]
expiry_days = len(all_remaining_dates)
print("Number of remaining days to Weekly Expiry: ",expiry_days)

### Day Inputs
all_input_variables = aiv = input
#-----

### Telegram Msg
tele_msg="---Running %s with following INPUTS---"%(strategy_name) + '\n\n'
for x,y in aiv.items():
    tele_msg+=x+' :: '+str(y) + '\n'
telegram_msg(tele_msg); print(tele_msg)

hedge_start_time = (datetime.datetime.combine(datetime.date.today(), aiv['EntryTime']) + datetime.timedelta(seconds=-45)).time()
sleep_secs = wake_up_time(wakeup_at = hedge_start_time)
time.sleep(sleep_secs)

### 
def get_straddle_strangle_pair():
    while True:
        try:
            index_price = login_credentials['kite'].ltp([index_token])[str(index_token)]['last_price']
            all_prices = login_credentials['kite'].ltp(inst_req_index.instrument_token.tolist())
            break
        except Exception as pe:
            print(str(pe)); time.sleep(.5);continue
    ATM_price = round(index_price/strikes)*strikes
    strangle_width=aiv['Delta']
    call_option = [x for x,y in token_info_req_index.items() if y['strike']==ATM_price+strangle_width and y['instrument_type']=='CE'][0]
    put_option = [x for x,y in token_info_req_index.items() if y['strike']==ATM_price-strangle_width and y['instrument_type']=='PE'][0]
    call_option_price = all_prices[str(call_option)]['last_price']
    put_option_price = all_prices[str(put_option)]['last_price']              
    return call_option, put_option, call_option_price, put_option_price

def get_req_hedge_option(opt_type, main_option_price, hedge_far_strike_perc):
    while True:
        try:
            all_prices = login_credentials['kite'].ltp(inst_req_index.instrument_token.tolist())
            break
        except Exception as ltp_e:
            print("Err to retrieve all option prices :: ",str(ltp_e)); time.sleep(1)
    hedge_req_price=main_option_price*hedge_far_strike_perc
    all_prices = {int(x):y['last_price'] for x,y in all_prices.items()}
    opt_list = [[abs(p-hedge_req_price),t,p] for t,p in all_prices.items() if token_info_req_index[t]['instrument_type']==opt_type and p>=hedge_req_price]
    opt_list.sort()
    return opt_list[0][-2]

def get_margin_req(margin_param):
    while True:
        try:return login_credentials['kite'].basket_order_margins(params=margin_param)['final']['total']
        except:time.sleep(.5)                
# -----------------------

### Dynamic Hedge ---
call_option_token, put_option_token, call_option_price, put_option_price = get_straddle_strangle_pair()
call_sell_trading_symbol = token_info_req_index[call_option_token]['tradingsymbol']
put_sell_trading_symbol = token_info_req_index[put_option_token]['tradingsymbol']

call_strangle = {'tradingsymbol':call_sell_trading_symbol, 'transaction_type':'SELL',
    "exchange":"NFO", "variety":"regular", "product":"MIS", "order_type":"MARKET",
    "quantity":lot_size*aiv['TradingQty'], "price":0, "trigger_price":0}
put_strangle = {'tradingsymbol':put_sell_trading_symbol, 'transaction_type':'SELL',
    "exchange":"NFO", "variety":"regular", "product":"MIS", "order_type":"MARKET",
    "quantity":lot_size*aiv['TradingQty'], "price":0, "trigger_price":0}
margin_param=[call_strangle, put_strangle]
margin_req = get_margin_req(margin_param)

if margin_req <= aiv['TradingAmount']*.99:
    print("No need to hedge as required margin is ",margin_req)
    HEDGE=False
else:
    print("Need to hedge as required margin is ",margin_req)
    HEDGE=True

while margin_req > aiv['TradingAmount']*.99:    
    call_option_token, put_option_token, call_option_price, put_option_price = get_straddle_strangle_pair()
    call_sell_trading_symbol = token_info_req_index[call_option_token]['tradingsymbol']
    put_sell_trading_symbol = token_info_req_index[put_option_token]['tradingsymbol']

    call_strangle = {'tradingsymbol':call_sell_trading_symbol, 'transaction_type':'SELL',
        "exchange":"NFO", "variety":"regular", "product":"MIS", "order_type":"MARKET",
        "quantity":lot_size*aiv['TradingQty'], "price":0, "trigger_price":0}
    put_strangle = {'tradingsymbol':put_sell_trading_symbol, 'transaction_type':'SELL',
        "exchange":"NFO", "variety":"regular", "product":"MIS", "order_type":"MARKET",
        "quantity":lot_size*aiv['TradingQty'], "price":0, "trigger_price":0}
    
    call_hedge_token = get_req_hedge_option('CE', call_option_price, hedge_far_strike_perc)
    put_hedge_token = get_req_hedge_option('PE', put_option_price, hedge_far_strike_perc)
    call_hedge_trading_symbol = token_info_req_index[call_hedge_token]['tradingsymbol']
    put_hedge_trading_symbol = token_info_req_index[put_hedge_token]['tradingsymbol']
    
    call_hedge = {'tradingsymbol':call_hedge_trading_symbol, 'transaction_type':'BUY',
        "exchange":"NFO", "variety":"regular", "product":"MIS", "order_type":"MARKET",
        "quantity":lot_size*aiv['TradingQty'], "price":0, "trigger_price":0}
    put_hedge = {'tradingsymbol':put_hedge_trading_symbol, 'transaction_type':'BUY',
        "exchange":"NFO", "variety":"regular", "product":"MIS", "order_type":"MARKET",
        "quantity":lot_size*aiv['TradingQty'], "price":0, "trigger_price":0}
    margin_param=[call_strangle, put_strangle, call_hedge, put_hedge]
    
    margin_req = get_margin_req(margin_param)
    print("Req. Margin is %d and Hedge Perc is %f"%(margin_req,hedge_far_strike_perc))
    hedge_far_strike_perc+=.5/100
    time.sleep(.5)
# --------------------------

if HEDGE:    
    signal_list=[["BUY",call_hedge_trading_symbol,aiv['TradingQty'], qty_per_lot, 'NFO','MIS','TRADE_NEW'],
                 ["BUY",put_hedge_trading_symbol,aiv['TradingQty'], qty_per_lot,'NFO','MIS','TRADE_NEW']]
    notification_msg = strategy_name +  " :: Buying HEDGEs %s & %s"%(call_hedge_trading_symbol, put_hedge_trading_symbol)
    print(notification_msg,' :: ', time_now())
    signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
    rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))
    call_hedge_pos=1; put_hedge_pos=1

if datetime.datetime.today().time()<aiv['EntryTime']:
    sleep_secs = wake_up_time(wakeup_at = aiv['EntryTime'])
    time.sleep(sleep_secs)

pubsub = rRr.pubsub()
pubsub.subscribe(['ZERODHA_TICKS_UPDATE'])
print("Reading market, waiting for Signals.....",'\n')

# CODE FOR STRATEGY
placed = False
ReEnterCounterSL = 0
ReEnterCounterTG = 0
ReEnterCE = False
ReEnterPE = False
ReEnterTG = False
CEActive = False
PEActive = False

for item in pubsub.listen():
    if datetime.datetime.today().time() > market_close_time:
        pubsub.unsubscribe()
        break
    if item['channel'].decode() == 'ZERODHA_TICKS_UPDATE' :
        try:
            data = pickle.loads(item['data'])
        except:
            continue
        try:
            call_option_price = [x['last_price'] for x in data if x['instrument_token']==call_option_token][0]
        except:
            pass
        try:
            put_option_price = [x['last_price'] for x in data if x['instrument_token']==put_option_token][0]
        except:
            pass
        if call_option_price==0 or put_option_price==0: 
            continue
        CurrentTime = datetime.datetime.today().time()
        Delta = CurrentTime.hour*60 + CurrentTime.minute - market_start_time.hour*60 - market_start_time.minute

        print("CALL OPTION : %f, PUT OPTION : %f "%(call_option_price, put_option_price),sep='',end="\r",flush=True)

        
        if aiv['EntryTime'] < datetime.datetime.today().time() < aiv['ExitTime'] :
            # PLACING THE ORDER FOR THE FIRST TIME
            if not placed:
                # Getting Option token and price
                call_option_token, put_option_token, call_option_price, put_option_price = get_straddle_strangle_pair()
                # Getting option symbol
                call_sell_trading_symbol = token_info_req_index[call_option_token]['tradingsymbol']
                put_sell_trading_symbol = token_info_req_index[put_option_token]['tradingsymbol']
                call_sell_entry_price = call_option_price
                put_sell_entry_price = put_option_price

                # Creating a signal list to send to Order Managment system
                signal_list=[["SELL", call_sell_trading_symbol, aiv['TradingQty'], lot_size, 'NFO', 'MIS', 'TRADE_NEW'],
                                ["SELL", put_sell_trading_symbol, aiv['TradingQty'], lot_size, 'NFO', 'MIS', 'TRADE_NEW']]
                # Creating notification message
                notification_msg = strategy_name +  " :: Selling %s & %s"%(call_sell_trading_symbol, put_sell_trading_symbol)
                print(notification_msg,' :: ', CurrentTime)
                # Sending signals to Order Managment System
                signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
                rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))

                # Calculating Near Stop Loss for call and put
                call_buy_sl_price = call_option_price * (1+aiv['SLPc']/100)
                put_buy_sl_price = put_option_price * (1+aiv['SLPc']/100)
                # Calculating Far Stop loss for call and put
                call_SLPcFar = call_option_price * (1+aiv['SLPcFar']/100)
                put_SLPcFar = put_option_price * (1+aiv['SLPcFar']/100)
                # Calculating Target for call and put
                call_Target = call_option_price * (1-aiv['TargetPc']/100)
                put_Target = put_option_price * (1-aiv['TargetPc']/100)
                print("SELL Price for Call is %f and Put is %f"%(call_sell_entry_price, put_sell_entry_price))
                print("SL for Call is %f and Put is %f"%(call_buy_sl_price, put_buy_sl_price))
                print("SLFar for Call is %f and Put is %f"%(call_SLPcFar, put_SLPcFar))
                placed = True
                CEActive = True
                PEActive = True

            # CHECKING FOR STOP LOSS RE-ENTRY
            if (ReEnterPE == True) and (ReEnterCE ==True) and (ReEnterCounterSL < aiv['MaxReEnterCounterSL']) and ((Delta-1) % aiv['SLEvery'] == 0):
                # Getting Option token and price
                call_option_token, put_option_token, call_option_price, put_option_price = get_straddle_strangle_pair()
                # Getting option symbol
                call_sell_trading_symbol = token_info_req_index[call_option_token]['tradingsymbol']
                put_sell_trading_symbol = token_info_req_index[put_option_token]['tradingsymbol']
                call_sell_entry_price = call_option_price
                put_sell_entry_price = put_option_price
                # Creating a signal list to send to Order Managment system
                # Sending order to Order Managment system
                signal_list=[["SELL", call_sell_trading_symbol, aiv['TradingQty'], lot_size, 'NFO', 'MIS', 'TRADE_NEW'],
                                ["SELL", put_sell_trading_symbol, aiv['TradingQty'], lot_size, 'NFO', 'MIS', 'TRADE_NEW']]
                # Creating notification message
                notification_msg = strategy_name +  " STOP LOSS RE-ENTRY :: Selling %s & %s"%(call_sell_trading_symbol, put_sell_trading_symbol)
                print(notification_msg,' :: ', CurrentTime)
                # Sending signals to Order Managment System
                signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
                rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))

                # Calculating Near Stop Loss for call and put
                call_buy_sl_price = call_option_price * (1+aiv['SLPc']/100)
                put_buy_sl_price = put_option_price * (1+aiv['SLPc']/100)
                # Calculating Far Stop loss for call and put
                call_SLPcFar = call_option_price * (1+aiv['SLPcFar']/100)
                put_SLPcFar = put_option_price * (1+aiv['SLPcFar']/100)
                # Calculating Target for call and put
                call_Target = call_option_price * (1-aiv['TargetPc']/100)
                put_Target = put_option_price * (1-aiv['TargetPc']/100)
                print("SELL Price for Call is %f and Put is %f"%(call_sell_entry_price, put_sell_entry_price))
                print("SL for Call is %f and Put is %f"%(call_buy_sl_price, put_buy_sl_price))
                print("SLFar for Call is %f and Put is %f"%(call_SLPcFar, put_SLPcFar))

                ReEnterPE = False
                ReEnterCE = False
                ReEnterCounterSL = ReEnterCounterSL + 1
                CEActive = True
                PEActive = True

            # CHECKING FOR CALL STOP LOSS
            if placed and (aiv['SL'] == defs.YES) and (CEActive == True) :
                if ((call_option_price >= call_SLPcFar) or ( Delta % aiv['SLEvery'] == 0 and call_option_price >= call_buy_sl_price) )  :
                    signal_list = [["BUY",call_sell_trading_symbol, aiv['TradingQty'], lot_size, 'NFO','MIS','SQ.OFF']]

                    notification_msg = strategy_name +  " CALL SL HIT :: Squaring off ", (call_sell_trading_symbol)
                    print(notification_msg,' :: ', CurrentTime)
                    print("Call Option Price when SL Hit was ", call_option_price)
                    print("Estimated PNL is ", lot_size*(call_sell_entry_price - call_option_price)*aiv["TradingQty"])

                    signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
                    rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))
                    SLTime = CurrentTime
                    ReEnterCE = True
                    CEActive = False

            # CHECKING FOR PUT STOP LOSS
            if placed and (aiv['SL'] == defs.YES) and (PEActive == True) :
                if ((put_option_price >= put_SLPcFar) or ( Delta % aiv['SLEvery'] == 0 and put_option_price >= put_buy_sl_price) )  :

                    signal_list = [["BUY", put_sell_trading_symbol, aiv['TradingQty'], lot_size, 'NFO','MIS','SQ.OFF']]

                    notification_msg = strategy_name +  " PUT SL HIT :: Squaring off %s"%(put_sell_trading_symbol)
                    print(notification_msg,' :: ', CurrentTime)
                    print("Put Option Price when SL Hit was %f"% put_option_price)
                    print("Estimated PNL is ",  lot_size*(put_sell_entry_price - put_option_price)*aiv["TradingQty"])

                    signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
                    rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))
                    SLTime = CurrentTime
                    ReEnterPE = True
                    PEActive = False

            
        # # CHECKING FOR TARGET RE-ENTRY (TARGET CODE INCOMPLETE)
        #     if (ReEnterTG == True) and (ReEnterCounterTG < aiv['MaxReEnterCounterTG']):
        #         # Sending order to Order Managment system
        #         signal_list=[["SELL", call_sell_trading_symbol, aiv['TradingQty'], 'NFO', 'MIS', 'TRADE_NEW'],
        #                         ["SELL", put_sell_trading_symbol, aiv['TradingQty'], 'NFO', 'MIS', 'TRADE_NEW']]
        #         # Creating notification message
        #         notification_msg = strategy_name +  " TARGET RE-ENTRY :: Selling %s & %s"%(call_sell_trading_symbol, put_sell_trading_symbol)
        #         print(notification_msg,' :: ', CurrentTime)
        #         # Sending signals to Order Managment System
        #         signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
        #         rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))
        #         ReEnterTG = False
        #         ReEnterCounterTG = ReEnterCounterTG + 1
        #         Active = True

        #     # CHECKING FOR TARGET (TARGET CODE INCOMPLETE)
        #     if placed and (aiv['Target'] == defs.YES) and Active and ((call_option_price <= call_Target ) or (put_option_price <= call_Target )):

        #         signal_list = [["BUY", call_sell_trading_symbol, aiv['TradingQty'],lot_size, 'NFO','MIS','SQ.OFF'],
        #                         ["BUY", put_sell_trading_symbol, aiv['TradingQty'],'NFO','MIS','SQ.OFF']]

        #         notification_msg = strategy_name +  " TARGET :: Squaring off Call %s & Put %s"%(call_sell_trading_symbol, put_sell_trading_symbol)
        #         print(notification_msg,' :: ', CurrentTime)

        #         signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
        #         rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))
        #         ReEnterTG = True
        #         Active = False

        # END OF DAY SQUARE OFF
        if aiv['ExitTime'] < datetime.datetime.today().time() :
            if PEActive:
                signal_list = [["BUY",put_sell_trading_symbol, aiv['TradingQty'],lot_size, 'NFO','MIS','SQ.OFF']]

                notification_msg = strategy_name +  " PUT EOD :: Squaring off %s"%(put_sell_trading_symbol)
                print(notification_msg,' :: ', CurrentTime)

                signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
                rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))

                print("Put Option Price when SL Hit was %f"% put_option_price)
                print("Estimated PNL is ", (put_sell_entry_price - put_option_price)*aiv["TradingQty"]*lot_size)
                PEActive = False

            if CEActive:
                signal_list = [["BUY",call_sell_trading_symbol, aiv['TradingQty'],lot_size, 'NFO','MIS','SQ.OFF']]

                notification_msg = strategy_name +  " CALL EOD :: Squaring off %s"%(call_sell_trading_symbol)
                print(notification_msg,' :: ', CurrentTime)

                signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
                rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))

                print("Put Option Price when SL Hit was %f"% put_option_price)
                print("Estimated PNL is ", (put_sell_entry_price - put_option_price)*aiv["TradingQty"]*lot_size)
                CEActive = False

            # SQUARING OFF HEDGE
            if HEDGE:
                signal_list=[["SELL", call_hedge_trading_symbol, aiv['TradingQty'], lot_size, 'NFO', 'MIS','SQ.OFF'],
                            ["SELL", put_hedge_trading_symbol, aiv['TradingQty'], lot_size, 'NFO', 'MIS', 'SQ.OFF']]
                notification_msg = strategy_name +  " :: Squaring off Hedge %s & %s"%(call_hedge_trading_symbol, put_hedge_trading_symbol)
                print(notification_msg,' :: ', CurrentTime)
                signal_info = {"ALGO":strategy_name, "telegram_msg":notification_msg, "SIGNALS":signal_list }
                rRr.publish('ORDER_MGMT_SYS', json.dumps(signal_info))
                HEDGE=False

print("#####------------------------------#####")
print("CLOSING CODE")
print("#####------------------------------#####")
telegram_msg("Closing"+strat_title)

sleep_secs = wake_up_time(wakeup_at = datetime.time(15,35,0))
time.sleep(sleep_secs)

