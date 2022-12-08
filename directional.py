import pandas as pd
import ta
from pathlib import Path
import datetime
import time
import atomic as atom
import definitions as defs

Banknifty_Path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Banknifty/"

# This function resamples data to required frequency from 1 min data
def Resample(df, freq='1T'): # freq format,  for 2min freq='2T', for 3min freq='3T' 
    resample_df = df.resample(freq, origin='start').agg({
    'open':'first',
    'high':'max',
    'low':'min',
    'close':'last' 
    })
    return resample_df

# This function gets spot data of multiple days
def getMultipledayData(start_date, end_date, symbol, freq):
        
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
            resampled = Resample(spotdata, freq)
            resampled.dropna(inplace=True)
            df_list.append(resampled)

        else:
            print("No data for " + start_date.strftime("%Y-%m-%d"))
        
        start_date += delta

    finaldf = pd.concat(df_list)
    return finaldf




def getRSI(spotdata, period=14):
    tempdf = spotdata.copy()
    tempdf['rsi'] = ta.momentum.RSIIndicator(tempdf['close'], window=period).rsi()
    return tempdf


def getADX(spotdata, period=14):
    tempdf = spotdata.copy()
    tempdf['adx'] = ta.trend.ADXIndicator(tempdf['high'], tempdf['low'], tempdf['close'], window=period).adx()
    return tempdf

# def EnterPosition(masterdf, positionconfig, generalconfig):


def EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, OHLC):
    positionsNotPlaced = []
    for posc in positionconfig:
        exp = atom.GetExpiry(masterdf, generalconfig["symbol"])
        cst = currentcandle[OHLC]
        cst = int(round(cst / 100, 0) * 100)
        opdf = masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]]
        # print(config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"])
        if currentcandle.name in opdf.index:
            price = opdf.loc[currentcandle.name][OHLC]
            position = {"EnterPrice": price, "PositionConfig": posc, "Expiry":exp, "StrikePrice": cst + posc["Delta"],
                  "OpSymbol": generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"],
                "OpData": masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]],
                  "Entertime": currentcandle.name.time(), "Qty": 25 * posc["LotSize"],
                   "date": currentcandle.name.date(),
                  "SLCond": posc["SLPc"],
                  "TargetCond": posc["TargetPc"] ,
                  "Active": True, "Strike": cst + posc["Delta"],
                  "symbol": masterdf.iloc[0]['symbol'], "trades":{}}
            positions.append(position)
        else:
            positionsNotPlaced.append(posc)
    return (positions, positionsNotPlaced)

def CheckStopLoss(positions, currentcandle):
    positionstoExit = []
    posconfigtoExit = []
    for pos in positions:
        if currentcandle.name in pos['OpData'].index :
            if (pos["PositionConfig"]["Action"] == defs.SELL):
                
                if currentcandle.rsi <= pos['SLCond'] and pos['Active'] and (pos["PositionConfig"]["SL"] == defs.YES):
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                
                if currentcandle.rsi >= pos['SLCond'] and pos['Active'] and (pos["PositionConfig"]["SL"] == defs.YES):
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
    return (positionstoExit, posconfigtoExit)

def CheckTargetCondition(positions, currentcandle):
    positionstoExit = []
    posconfigtoExit = []
    for pos in positions:
        if currentcandle.name in pos['OpData'].index:
            optionprice = pos["OpData"].loc[currentcandle.name]['high']
            if (pos["PositionConfig"]["Action"] == defs.SELL):
                if currentcandle.rsi >= pos['TargetCond'] and pos['Active'] and (pos["PositionConfig"]["Target"] == defs.YES):
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                if currentcandle.rsi <= pos['TargetCond'] and pos['Active'] and (pos["PositionConfig"]["Target"] == defs.YES):
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
    return (positionstoExit, posconfigtoExit)


def ExitPosition(positionstoExit, currentcandle, ExitReason):
    for pos in positionstoExit:
        if (pos["Active"]):
            Str = ""
            if (pos["PositionConfig"]["Action"] == defs.BUY):
                Str = "Buy "
            elif (pos["PositionConfig"]["Action"] == defs.SELL):
                Str = "Sell "
            Str = Str + pos["PositionConfig"]["Type"]
            if (ExitReason == defs.SL):
                exitprice = pos["OpData"].loc[currentcandle.name]['close']
                exitReason = "SL HIT"
            elif (ExitReason == defs.TARGET):
                exitprice = pos["OpData"].loc[currentcandle.name]['close']
                exitReason = "Target Hit"
            elif (ExitReason == defs.SQUAREOFF):
                if currentcandle.name in pos["OpData"].index:
                    exitprice = pos["OpData"].loc[currentcandle.name]['close']
                    exitReason = "Square Off"
                else:
                    idx = pos["OpData"].index[pos["OpData"].index.get_loc(currentcandle.name, method='nearest')]
                    exitprice = pos["OpData"][idx]
            elif (ExitReason == defs.SQUAREOFFEOD):
                if currentcandle.name in pos["OpData"].index:
                    exitprice = pos["OpData"].loc[currentcandle.name]['open']
                    exitReason = "Square Off EOD"
                else:
                    if pos["OpData"].empty:
                        return
                    else:
                        idx = pos["OpData"].index[pos["OpData"].index.get_loc(currentcandle.name, method='nearest')]
                        exitprice = pos["OpData"][idx]

            enterprice = pos['EnterPrice']
            pos["trades"] = {'EnterPrice': enterprice, 'ExitPrice': exitprice, 'EnterTime': pos['Entertime'], 'ExitTime': currentcandle.name.time(),
                     'Reason': exitReason, 'Trade Type': Str,
                     "pnl": (exitprice - enterprice) * pos["PositionConfig"]["Action"] * pos["Qty"],
                     "date": pos["date"], "symbol": pos["OpSymbol"]}
            pos["Active"] = False


