import pandas as pd
import ta
from pathlib import Path
import datetime
import time
import atomic as atom
import definitions as defs
import supertrend as st
import numpy as np

# This function resamples data to required frequency from 1 min data
def Resample(df, freq='1T'): # freq format,  for 2min freq='2T', for 3min freq='3T' 
    resample_df = df.resample(freq, origin='start').agg({
    'open':'first',
    'high':'max',
    'low':'min',
    'close':'last' 
    })
    return resample_df

# This function gets spot data of multiple days and resamples for required frequency
def getMultipledayData(start_date, end_date, path, symbol, freq):        
    df_list = []
    delta = datetime.timedelta(days=1)
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
     
        start_date += delta
    finaldf = pd.concat(df_list)
    finaldf = finaldf.apply(pd.to_numeric)
    return finaldf

def getRSI(spotdata, columnname, period=14):
    tempdf = spotdata
    tempdf[columnname] = ta.momentum.RSIIndicator(tempdf['close'], window=period).rsi()
    return tempdf

def getADX(spotdata, columnname, period=14):
    tempdf = spotdata
    tempdf[columnname] = ta.trend.ADXIndicator(tempdf['high'], tempdf['low'], tempdf['close'], window=period).adx()
    return tempdf

def getBollingerBand(spotdata,columnname, period, stddev):
    tempdf = spotdata
    bb = ta.volatility.BollingerBands(tempdf.close, period, stddev)
    tempdf['upband'] = bb.bollinger_hband()
    #tempdf['sma'] = bb.bollinger_mavg()
    tempdf['lowband'] = bb.bollinger_lband()
    #tempdf['hsignal'] = bb.bollinger_hband_indicator()
    #tempdf['lsignal'] = bb.bollinger_lband_indicator()
    tempdf[columnname] = (tempdf.close - bb.bollinger_lband())/(bb.bollinger_hband() - bb.bollinger_lband())
    return tempdf

def getMACD(spotdata, fastperiod, slowperiod):
    tempdf = spotdata
    macd = ta.trend.MACD(tempdf.close, slowperiod, fastperiod)
    tempdf['MACD'] = macd.macd()
    tempdf['MACD_signal'] = macd.macd_signal()
    return tempdf

def getTI(spotdata, TIconfig):
    for t in TIconfig:
        if t['TI'] == "RSI":
            data = getRSI(spotdata, t['columnname'], t['Window'])
        if t['TI'] == "ADX":
            data = getADX(spotdata, t['columnname'], t['Window'])
        if t['TI'] == 'BB':
            data = getBollingerBand(spotdata,t['columnname'], t['period'], t['stddev'])
        if t['TI'] == 'MACD':
            data = getMACD(spotdata, t['fastperiod'], t['slowperiod'])
        if t['TI'] == 'ST':
            data = getSuperTrendIndicator(spotdata, t['period'], t['multiplier'], t['columnname'])
    return data

def getSuperTrendIndicator(spotdata, period, multiplier, columnname):
    tempdf = spotdata
    df = st.SuperTrend(tempdf, period, multiplier)
    df[columnname] = np.where(df.STX == 'down', -1, np.where(df.STX == 'up', 1, 0))
    return df

# Check entry condition based on the TIconfig
def CheckEntryCondition(currentcandle, TIconfig):
    # Check bullish condition
    bull = True
    bear = True
    for t in TIconfig:
        bull = bull and t["BullOperator"](currentcandle[t["columnname"]], t["ThreshBull"])
        bear = bear and t["BearOperator"](currentcandle[t["columnname"]], t["ThreshBear"])    
    return (bull, bear)

def EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, OHLC, stance):
    positionsNotPlaced = []
    for posc in positionconfig:
        if (posc["Stance"] == stance):
            exp = atom.GetExpiry(masterdf, generalconfig["symbol"])
            if generalconfig['symbol'] == defs.N :
                cst = currentcandle[OHLC]
                cst = int(round(cst / 50, 0) * 50)
            elif generalconfig['symbol'] == defs.BN :
                cst = currentcandle[OHLC]
                cst = int(round(cst / 100, 0) * 100)
            opdf = masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]]
            # print(config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"])
            if currentcandle.name in opdf.index:
                price = opdf.loc[currentcandle.name][OHLC]
                position = {"EnterPrice": price, "PositionConfig": posc, "Expiry":exp, "StrikePrice": cst + posc["Delta"],
                    "OpSymbol": generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"],
                    "OpData": masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]],
                    "Entertime": currentcandle.name.time(), "Qty": generalconfig["LotSize"] * posc["NumLots"],
                    "date": currentcandle.name.date(),                    
                    "TargetCond": posc["Target"], "EnterSpotPrice": currentcandle[OHLC],
                    "Active": True, "Strike": cst + posc["Delta"],
                    "symbol": masterdf.iloc[0]['symbol'], "trades":{}, "stance": stance, "Slippage": generalconfig['Slippage']}
                if (posc["SL"] == defs.YES):
                    position["SLCond"] = price - posc["Action"]*price*posc["SLPc"]/100
                if (posc["Target"] == defs.YES):
                    position["TargetCond"] = price + posc["Action"]*price*posc["TargetPc"]/100
                positions.append(position)
            else:
                positionsNotPlaced.append(posc)
    return (positions, positionsNotPlaced)

def CheckStopLossConditionStance(stance, currentcandle, TIconfig):
    SLCondBull = False
    SLCondBear = False
    if (stance == defs.BULL):
        for t in TIconfig:
            if (t["SL"]):
                SLCondBull = SLCondBull or (t["SLBullOperator"](currentcandle[t["columnname"]], t["SLBull"]))
    if (stance == defs.BEAR):
        for t in TIconfig:
            if (t["SL"]):
                SLCondBear = SLCondBear or (t["SLBearOperator"](currentcandle[t["columnname"]], t["SLBear"]))
    return (SLCondBull, SLCondBear)      
         
def CheckStopLossTI(positions, currentcandle, TIconfig):
    positionstoExit = []
    for pos in positions:
        if currentcandle.name in pos['OpData'].index :
            (SLCondBull, SLCondBear) = CheckStopLossConditionStance(pos["stance"], currentcandle, TIconfig)
            if (SLCondBull and pos["Active"]):
                positionstoExit.append(pos)
            if (SLCondBear and pos["Active"]):
                positionstoExit.append(pos)
    return positionstoExit

def CheckTargetConditionStance(stance, currentcandle, TIconfig):
        TargetCondBull = False
        TargetCondBear = False
        if (stance == defs.BULL):
            for t in TIconfig:
                if (t["Target"]):
                    TargetCondBull = TargetCondBull or (t["TBullOperator"](currentcandle[t["columnname"]], t["TargetBull"]))
        if (stance == defs.BEAR):
            for t in TIconfig:
                if (t["Target"]):
                    TargetCondBear = TargetCondBear or (t["TBearOperator"](currentcandle[t["columnname"]], t["TargetBear"]))
        return (TargetCondBull, TargetCondBear)

def CheckTargetConditionTI(positions, currentcandle, TIconfig):
    positionstoExit = []
    for pos in positions:
        if currentcandle.name in pos['OpData'].index :
            (TargetCondBull, TargetCondBear) = CheckTargetConditionStance(pos["stance"], currentcandle, TIconfig)          
            if (TargetCondBull and pos["Active"]):
                positionstoExit.append(pos)
            if (TargetCondBear and pos["Active"]):
                positionstoExit.append(pos)
    return positionstoExit


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
                        exitprice = pos["OpData"].loc[idx]['open']
                        exitReason = "Square Off EOD"
            enterprice = pos['EnterPrice']
            pos["trades"] = {'EnterPrice': enterprice*(1 + pos["Slippage"]/100*pos["PositionConfig"]["Action"]), 'ExitPrice': exitprice*(1 + pos["Slippage"]/100*pos["PositionConfig"]["Action"]), 
                            'EnterTime': pos['Entertime'], 'ExitTime': currentcandle.name.time(),
                            'Reason': exitReason, 'Trade Type': Str, 'EnterSpotPrice': pos["EnterSpotPrice"], "ExitSpotPrice": currentcandle['close'],
                            "pnl": (exitprice - enterprice) * pos["PositionConfig"]["Action"] * pos["Qty"],
                            "date": pos["date"], "symbol": pos["OpSymbol"] }
            pos["Active"] = False


