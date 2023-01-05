print("#####------------------------------#####")
print("STARTING NEW WS CODE")
print("#####------------------------------#####")

from kiteconnect import KiteConnect
import requests,json,time,datetime, os
import pandas as pd, numpy as np
import pickle, redis, random
rRr = redis.Redis(host='127.0.0.1', port=6379, db=0)
# -----------------------
from login import account_info, AC, get_request_token, login_and_host
from utility_main import market_hours, wake_up_time # , telegram_msg
# -----------------------

while True:
    decision = market_hours()
    if decision=='OPEN':
        print('##### MARKET OPEN :: Logging in #####')
        #telegram_msg("MARKET OPEN :: Logging in to Zerodha")
        break
    get_up_time=datetime.datetime.fromtimestamp(decision+time.time()).strftime('%H:%M:%S %A, %d-%b-%Y')
    print('Login Credentials will be updated again @ ',get_up_time)
    #telegram_msg('Zerodha Login Credentials will be updated again @ '+ get_up_time)
    time.sleep(decision)

print("###########################################################")
request_token = get_request_token()
login_and_host(request_token)
print("---------------------------------------------------")
login_credentials = pickle.loads(rRr.get('login_credentials'))
inst = pickle.loads(rRr.get('inst_df'))
print("###########################################################")
#telegram_msg("Logged in successfully to Zerodha Account")

#----------------------
# nearest_monthly_expiry = min(list(set(inst[inst.name=='RELIANCE']['expiry'].tolist())))
# nearest_weekly_expiry = min(list(set(inst[(inst.name=='NIFTY')]['expiry'].tolist())))
nearest_monthly_expiry = min([d for d in list(set(inst[(inst.name=='RELIANCE')]['expiry'].tolist())) if d>=datetime.datetime.now().date()])
nearest_weekly_expiry = min([d for d in list(set(inst[(inst.name=='NIFTY')]['expiry'].tolist())) if d>=datetime.datetime.now().date()])
inst_req = inst[(inst.tradingsymbol.isin(['NIFTY BANK'])) | # Index
               ((inst.name.isin(['BANKNIFTY']))&(inst.segment=='NFO-FUT')&(inst.expiry==nearest_monthly_expiry)) | # Futures
               ((inst.name=='BANKNIFTY')&(inst.segment=='NFO-OPT')&(inst.expiry==nearest_weekly_expiry))] # Bank Nifty OC
print("Required Instrument list retrieved :: ",inst_req.shape)

token_info_req = {x['instrument_token']:x for x in inst_req.to_dict('records')}
#----------------------

rRr.set('inst_REQ', pickle.dumps(inst_req))
rRr.set('token_info_REQ', pickle.dumps(token_info_req))
print('All required instruments, tokens & symbols are Hosted')
#----------------------
#######################
# BANK NIFTY ----------------------------------------------------------
inst_BN = inst[(inst.tradingsymbol.isin(['NIFTY BANK'])) | # Index
               ((inst.name.isin(['BANKNIFTY']))&(inst.segment=='NFO-FUT')&(inst.expiry==nearest_monthly_expiry)) | # Futures
               ((inst.name=='BANKNIFTY')&(inst.segment=='NFO-OPT')&(inst.expiry==nearest_weekly_expiry))] # Bank Nifty OC
token_info_BN = {x['instrument_token']:x for x in inst_BN.to_dict('records')}
#----------------------
rRr.set('inst_BN', pickle.dumps(inst_BN))
rRr.set('token_info_BN', pickle.dumps(token_info_BN))
print("Bank Nifty Instrument list retrieved & hosted :: ",inst_BN.shape)
# print(token_info_BN, flush=True)
print(inst_BN, flush=True)
#######################

#telegram_msg("Initiating Data Pool Connection")
req_instrument_token = inst_req.instrument_token.tolist()

###################### WEB SOCKET CONNECTION ######################
from kiteconnect import KiteTicker
kws = KiteTicker(login_credentials['api_key'], login_credentials['access_token'])

def on_ticks(ws, ticks):
    rRr.publish('ZERODHA_TICKS_UPDATE', pickle.dumps(ticks))
    print(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S'),sep='',end="\r",flush=True)
    if datetime.datetime.today().time() > datetime.time(15, 29, 55):
        print('Closing Connection')
        #######################
        ws.stop()

def on_order_update(ws, data):
    # rRr.publish('ZERODHA_ORDER_UPDATE', pickle.dumps(data))
    pass

def on_connect(ws, response):
    ws.subscribe(req_instrument_token)
    ws.set_mode(ws.MODE_LTP, req_instrument_token)

kws.on_ticks = on_ticks
# kws.on_order_update = on_order_update
kws.on_connect = on_connect
#######################
print("Streaming with Zerodha")
#telegram_msg("Streaming with Zerodha")
kws.connect()

print("#####------------------------------#####")
print("WS connection CLOSED Successfully")
#telegram_msg("Streaming closed successfully")
print("#####------------------------------#####")
time.sleep(300)

#######################

print("#####------------------------------#####")
print("Done for the day, closing code successfully")
print("#####------------------------------#####")
