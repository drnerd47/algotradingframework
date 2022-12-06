import pandas as pd
import ta
from pathlib import Path
import datetime
import time

# This function gets spot data of multiple days
def getMultipledayData(start_date, end_date, symbol):
        
    df_list = []
    delta = datetime.timedelta(days=1)

    if symbol == 'BANKNIFTY':
        path = Banknifty_Path
    elif symbol == 'NIFTY':
        path = Nifty_Path


    while start_date <= end_date:
        date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
        currpath = path + date_string
        my_file = Path(currpath)

        if my_file.exists():
            df = pd.read_csv(currpath)
            df = df.drop('datetime.1', axis=1)
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.set_index(df['datetime'])
            spotdata = df[df['symbol'] == symbol]
            df_list.append(spotdata)

        else:
            print("No data for " + start_date.strftime("%Y-%m-%d"))
        
        start_date += delta

    finaldf = pd.concat(df_list)
    return finaldf

# This function resamples data to required frequency from 1 min data
def Resample(df, freq): # freq format,  for 2min freq='2T', for 3min freq='3T' 
    resample_df = df.resample(freq, origin='start').agg({
    'open':'first',
    'high':'max',
    'low':'min',
    'close':'last' 
    })
    return resample_df


def getRSI(spotdata, period, freq):
    tempdf = Resample(spotdata, freq)
    tempdf['rsi'] = ta.momentum.RSIIndicator(tempdf['close'], window=period).rsi()
    return tempdf


def getADX(spotdata, period, freq):
    tempdf = Resample(spotdata, freq)
    tempdf['adx'] = ta.trend.ADXIndicator(tempdf['high'], tempdf['low'], tempdf['close'], window=period).adx()
    return tempdf



