from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs
from kiteconnect import KiteConnect
import requests, json, time, datetime, os
import pandas as pd, numpy as np
import time, random, redis, pyotp, pickle, datetime
from kiteconnect import KiteConnect
from kiteconnect import KiteTicker
import requests, json, time, datetime, os
import pandas as pd, numpy as np
import pickle
from pathlib import Path
from utility_main import wake_up_time, telegram_msg

                                                                                                          

# This is the account information with the broker from where we are streaming market data i.e. Zerodha
account_info =[{'USER_ID': 'KL8793', 'PASS': '@Guru108', 'pin': 'EHEZIY6YV5KHL2BE7Y5DDAFJ43OPYXKC',
                'api_key': '8d15lh3maz9irlox', 'api_secret': 'dayfo77s5wvpbc54fwp471ldt85y0xx0'}]

# This is specifying the last entry in account_info to AC variable
AC = account_info[-1]

# This function returns current time
def time_now():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')

# This function opens the browser and logs into Zerodha and generates Request Token required for accessing Zerodha API
def get_request_token():
    url_ = "https://kite.trade/connect/login?api_key=" + AC['api_key'] + "&v=3"
    
    options = Options()
    options.set_headless(headless=True)
    driver = webdriver.Chrome(options = options, executable_path = "chromedriver.exe") 
    print ("Chrome Initialized") 
    driver.get(url_)

    print(driver.current_url)
    time.sleep(random.sample([5,6,7],1)[0])
    print('Title :: ',driver.title)
    print('Current URL :: ',driver.current_url)

    driver.find_element_by_css_selector("""div#container input[type="text"]""").send_keys(AC['USER_ID'])
    print("Login ID Submitted")
    time.sleep(random.sample([2,3,4],1)[0])
    driver.find_element_by_css_selector("""div#container input[type="password"]""").send_keys(AC['PASS'])
    print("Login Pass Submitted")
    time.sleep(random.sample([2,3,4],1)[0])
    driver.find_element_by_css_selector("""div#container button[type="submit"]""").click()
    print("Login ID Pass CLICK")
    time.sleep(random.sample([5,6,7],1)[0])

    totp=pyotp.TOTP(AC['pin']);current_pin=totp.now()
    while True:
        totp = pyotp.TOTP(AC['pin'])
        new_pin = totp.now()
        print("Getting new pin", time_now())
        if new_pin!=current_pin:break
        time.sleep(2)

    # driver.find_element_by_css_selector("""#totp""").send_keys(new_pin)
    driver.find_element_by_xpath("""//*[@id="container"]/div/div/div/form/div[2]/input""").send_keys(new_pin)
    print("TOPT Entered")
    time.sleep(random.sample([1, 2, 3], 1)[0])
    driver.find_element_by_css_selector("""div#container button[type="submit"]""").click()
    print("PIN Submitted")
    time.sleep(random.sample([1, 2, 3], 1)[0])

    URL = driver.current_url
    print(URL)
    parsed_url = urlparse(URL)
    url_elements = parse_qs(parsed_url.query)
    request_token = url_elements['request_token'][0]
    driver.quit()
    print("Request token generated Successfully")
    return request_token

# This function logs into the Zerodha API using the request token
def login_and_host(request_token):
    api_key = AC['api_key']
    api_secret = AC['api_secret']
    print("---------------------------------------------------")
    print("Generating Kite Session")
    kite = KiteConnect(api_key)
    tokens = kite.generate_session(request_token, api_secret)
    print('Kite session generated')
    kite.set_access_token( tokens["access_token"] )
    print('Initializing Kite access tokens')
    access_token = tokens["access_token"]
    public_token = tokens["public_token"]
    user_id = tokens["user_id"]
    auth = "&api_key="+api_key+"&access_token="+access_token
    print('All tokens generated')
    print('Zerodha -- Logged in Successfully at %s'%(time.strftime("%d-%b-%Y %A %H:%M:%S", time.localtime())))
    print("###########################################################")
    # These are the login credentials for the API
    login_credentials={'kite':kite,'access_token':access_token,'public_token':public_token,
                       'user_id':user_id,'auth':auth,'api_key':api_key,'api_secret':api_secret,
                       'update_time':str(datetime.datetime.now())}

    print(login_credentials['kite'].profile())
    print("###########################################################")
    print('Fetching all instrument list')
    instrument_id = kite.instruments()
    # This contains all the instrument id's 
    inst = pd.DataFrame(instrument_id)
    print('Intrument Ids Retrived Successfully')
    print("###########################################################")
    return (inst, login_credentials)

print("#####------------------------------#####")
print("STARTING NEW DATA STORAGE WS CODE")
print("#####------------------------------#####")

# -----------------------

while True:
    decision = market_hours()
    if decision=='OPEN':
        print('##### MARKET OPEN :: Logging in #####')
        telegram_msg("MARKET OPEN :: Logging in to Zerodha")
        break
    get_up_time=datetime.datetime.fromtimestamp(decision+time.time()).strftime('%H:%M:%S %A, %d-%b-%Y')
    print('Login Credentials will be updated again @ ',get_up_time)
    telegram_msg('Zerodha Login Credentials will be updated again @ '+ get_up_time)
    time.sleep(decision)

print("###########################################################")
request_token = get_request_token()
(inst, login_credentials)  = login_and_host(request_token)
print("###########################################################")
telegram_msg("Logged in successfully to Zerodha Account")

#----------------------
# nearest_monthly_expiry = min(list(set(inst[inst.name=='RELIANCE']['expiry'].tolist())))
# # nearest_weekly_expiry = min(list(set(inst[(inst.name=='NIFTY')]['expiry'].tolist())))
# nearest_monthly_expiry = min([d for d in list(set(inst[(inst.name=='RELIANCE')]['expiry'].tolist())) if d>=datetime.datetime.now().date()])
# nearest_weekly_expiry = min([d for d in list(set(inst[(inst.name=='NIFTY')]['expiry'].tolist())) if d>=datetime.datetime.now().date()])

inst_req = inst[(inst.tradingsymbol.isin(['NIFTY BANK'])) | (inst.tradingsymbol.isin(['NIFTY 50'])) | # Index
               ((inst.name.isin(['BANKNIFTY']))&(inst.segment=='NFO-FUT')) | ((inst.name.isin(['NIFTY']))&(inst.segment=='NFO-FUT')) |# Futures
               ((inst.name=='BANKNIFTY')&(inst.segment=='NFO-OPT')) | ((inst.name=='NIFTY')&(inst.segment=='NFO-OPT'))] # Bank Nifty OC

print("Required Instrument list retrieved :: ",inst_req.shape)

token_info_req = {x['instrument_token']:x for x in inst_req.to_dict('records')}
#----------------------
#----------------------
##############################################

req_instrument_token = inst_req.instrument_token.tolist()

###################### WEB SOCKET CONNECTION ######################

kws = KiteTicker(login_credentials['api_key'], login_credentials['access_token'])

parent_dir = 'C:\Market Data'
datepath = os.path.join(parent_dir, str(datetime.datetime.today().date()))    
file = Path(datepath)
if file.exists():
    pass
else:
    os.mkdir(datepath) 

def on_ticks(ws, ticks):
    t = datetime.datetime.time(datetime.datetime.now())
    t = str(t)
    t = t.replace(":","_")
    t = t.replace(".","_")
    path = datepath + "\Data_" + t + ".pkl"
    ticks = pd.DataFrame(ticks)
    if (Path(path).exists()):
       pass
    else:
       ticks.to_pickle(path)
    #print(ticks)
    print(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S'),sep='',end="\r",flush=True)
    if datetime.datetime.today().time() > datetime.time(15, 29, 55):
        print('Closing Connection')
        #######################
        ws.stop()

def on_connect(ws, response):
    ws.subscribe(req_instrument_token)
    ws.set_mode(ws.MODE_LTP, req_instrument_token)

kws.on_ticks = on_ticks

kws.on_connect = on_connect
#######################
print("Streaming and Storing Data from Zerodha")
telegram_msg("Streaming and Storing Data from Zerodha")
kws.connect()

print("#####------------------------------#####")
print("WS connection CLOSED Successfully")
telegram_msg("Streaming closed successfully")
print("#####------------------------------#####")
time.sleep(300)

#######################

print("#####------------------------------#####")
print("Done for the day, closing code successfully")
print("#####------------------------------#####")
