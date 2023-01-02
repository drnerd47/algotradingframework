from kiteconnect import KiteConnect
# Step 1: Get Access token
# get the api key from the app dashboard
api_key = ""
client_id = ""

obtained_request_token = ""

# get api secret from app dashboard
api_secret = ""

try:
    kite = KiteConnect(api_key)
    print( kite.login_url())
except Exception as e :
    print(e)

try :
    user = kite.request_access_token(request_token= obtained_request_token, secret= api_secret)
    print(user['access_token'])
except Exception as e:
    print("Authentication Failed", str(e))
    raise