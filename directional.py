import pandas as pd
import ta
from pathlib import Path
import datetime
import atomic as atom
import definitions as defs
import supertrend as st
import numpy as np
import pandas_ta as pta
#from numba import jit_module

# This function resamples data to required frequency from 1 min data
def Resample(df, freq): # freq format,  for 2min freq='2T', for 3min freq='3T'
    f = str(freq)+"T" 
    resample_df = df.resample(f, origin='end').agg({
    'open':'first',
    'high':'max',
    'low':'min',
    'close':'last' 
    })#, engine='numba')
    return resample_df

def getRSI(spotdata, columnname, period=14):
    tempdf = spotdata
    tempdf[columnname] = ta.momentum.RSIIndicator(tempdf['close'], window=period).rsi()
    return tempdf

def getADX(spotdata, columnname, period=14):
    tempdf = spotdata
    try:
        tempdf[columnname] = ta.trend.ADXIndicator(tempdf['high'], tempdf['low'], tempdf['close'], window=period).adx()
    except:
        colname = 'ADX_' + str(period)
        tempdf[columnname] = pta.adx(high=tempdf['high'], low=tempdf['low'], close=tempdf['close'], length=period)[colname]
    return tempdf

def getMA(spotdata, columnname, period=14, type='simple'):
    tempdf = spotdata
    if (type == "SMA"):
        tempdf['MA'] = ta.trend.SMAIndicator(tempdf['close'], window=period).sma_indicator()
    elif (type == 'EMA'):
        tempdf['MA'] = ta.trend.EMAIndicator(tempdf['close'], window=period).ema_indicator()
    tempdf[columnname] = (tempdf['close'] - tempdf['MA'])
    return tempdf

def getBollingerBand(spotdata,columnname, period, stddev):
    tempdf = spotdata
    bb = ta.volatility.BollingerBands(tempdf.close, period, stddev)
    tempdf['upband'] = bb.bollinger_hband()
    tempdf['sma'] = bb.bollinger_mavg()
    tempdf['lowband'] = bb.bollinger_lband()
    tempdf['hsignal'] = bb.bollinger_hband_indicator()
    tempdf['lsignal'] = bb.bollinger_lband_indicator()
    tempdf[columnname] = (tempdf.close - bb.bollinger_lband())/(bb.bollinger_hband() - bb.bollinger_lband())
    return tempdf

def getMACD(spotdata, fastperiod, slowperiod):
    tempdf = spotdata
    macd = ta.trend.MACD(tempdf.close, slowperiod, fastperiod)
    tempdf['MACD'] = macd.macd()
    tempdf['MACD_signal'] = macd.macd_signal()
    return tempdf

def getSuperTrendIndicator(spotdata, period, multiplier, columnname):
    tempdf = spotdata
    df = st.SuperTrend(spotdata, period, multiplier)
    df[columnname] = np.where(df.STX == 'down', -1, np.where(df.STX == 'up', 1, 0))
    return df

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
        if t['TI'] == 'MA':
            data = getMA(spotdata, t['columnname'], t['period'], t['type'])
        if t['TI'] == 'RSI-Shifted':
            data = getRSI(spotdata, t['columnname'], t['Window'])
            data[t['columnname']] = data[t['columnname']].shift(1)
    data['EntrySignal'] = np.nan
    data['ExitSignal'] = np.nan
    return data

def getTIIndicatorData(start_date, end_date, Nifty_Path, Banknifty_Path, Finnifty_Path, generalconfig, TIconfig):
    if (generalconfig["Rolling"] == defs.YES):
        if (generalconfig["symbol"] == defs.N):
            data = getRollingTIIndicatorData(start_date, end_date, generalconfig["EnterTime"], Nifty_Path, defs.N,
                                            generalconfig["Resample"], TIconfig)
        elif (generalconfig["symbol"] == defs.BN) :
            data = getRollingTIIndicatorData(start_date, end_date, generalconfig["EnterTime"], Banknifty_Path, defs.BN,
                                            generalconfig["Resample"], TIconfig)
        elif (generalconfig["symbol"] == defs.FN) :
            data = getRollingTIIndicatorData(start_date, end_date, generalconfig["EnterTime"], Finnifty_Path, defs.FN,
                                            generalconfig["Resample"], TIconfig)
    else:
        if (generalconfig["symbol"] == defs.N):
            data = getIntradayTIIndicatorData(start_date, end_date, generalconfig["EnterTime"], Nifty_Path, defs.N,
                                            generalconfig["Resample"], TIconfig)
        elif (generalconfig["symbol"] == defs.BN) :
            data = getIntradayTIIndicatorData(start_date, end_date, generalconfig["EnterTime"], Banknifty_Path, defs.BN,
                                            generalconfig["Resample"], TIconfig)
        elif (generalconfig["symbol"] == defs.FN) :
            data = getIntradayTIIndicatorData(start_date, end_date, generalconfig["EnterTime"], Finnifty_Path, defs.FN,
                                            generalconfig["Resample"], TIconfig)
    return data


# This function gets spot data of multiple days and resamples for required frequency on a rolling basis
def getRollingTIIndicatorData(start_date, end_date, entertime, path, symbol, freq, TIconfig):
    df_list = []
    # delta = datetime.timedelta(days=1)
    # print("Getting Data from "+ str(start_date) + " to "+ str(end_date)+ " for Directional Strategy.")
    totaldelta = end_date - start_date
    dates = pd.date_range(start_date, periods=totaldelta.days+1)
    for date in dates.tolist():
        csv_date_string = date.strftime("%Y/Data%Y%m%d.csv")
        pkl_date_string = date.strftime("%Y/Data%Y%m%d.pkl")
        csv_currpath = path + csv_date_string
        pkl_currpath = path + pkl_date_string
        csv_file = Path(csv_currpath)
        pkl_file = Path(pkl_currpath)
        
        if csv_file.exists():
            df = pd.read_csv(csv_currpath)
            try:
                try:
                    df = df.drop('datetime.1', axis=1)
                    df["datetime"] = pd.to_datetime(df["datetime"])
                except:
                    df['datetime'] = df['date'] + ' ' + df['time']
                    df["datetime"] = pd.to_datetime(df["datetime"])
            except: # THIS EXCEPTION OCCURS WHEN BACKTESTING ON LIVE STORED DATA
                df["datetime"] = pd.to_datetime(df["datetime"])

            df = df.set_index(df['datetime'])
            mask1 = df.index.time >= entertime
            mask2 = df['symbol'] == symbol           
            spotdata = df[mask1 & mask2]
            spotdata = spotdata.drop_duplicates(subset=['datetime'])
            resampled = Resample(spotdata, freq)
            resampled = resampled.apply(pd.to_numeric)
            resampled.dropna(inplace=True)
            df_list.append(resampled)

        elif pkl_file.exists():
            df = pd.read_pickle(pkl_currpath)
            try:
                try:
                    df = df.drop('datetime.1', axis=1)
                    df["datetime"] = pd.to_datetime(df["datetime"])
                except:
                    df['datetime'] = df['date'] + ' ' + df['time']
                    df["datetime"] = pd.to_datetime(df["datetime"])
            except: # THIS EXCEPTION OCCURS WHEN BACKTESTING ON LIVE STORED DATA
                df["datetime"] = pd.to_datetime(df["datetime"])

            df = df.set_index(df['datetime'])
            mask1 = df.index.time >= entertime
            mask2 = df['symbol'] == symbol           
            spotdata = df[mask1 & mask2]
            spotdata = spotdata.drop_duplicates(subset=['datetime'])
            resampled = Resample(spotdata, freq)
            resampled = resampled.apply(pd.to_numeric)
            resampled.dropna(inplace=True)
            df_list.append(resampled)
     
        # start_date += delta
    finaldf = pd.concat(df_list)
    finaldf = getTI(finaldf, TIconfig)
    return finaldf

# This function gets the TI indicator data everyday without rolling from previous day
def getIntradayTIIndicatorData(start_date, end_date, entertime, path, symbol, freq, TIconfig):    
    df_list = []
    # delta = datetime.timedelta(days=1)
    # print("Getting Data from "+ str(start_date) + " to "+ str(end_date)+ " for Directional Strategy.")
    totaldelta = end_date - start_date
    dates = pd.date_range(start_date, periods=totaldelta.days+1)
    
    for date in dates:
        csv_date_string = date.strftime("%Y/Data%Y%m%d.csv")
        pkl_date_string = date.strftime("%Y/Data%Y%m%d.pkl")
        csv_currpath = path + csv_date_string
        pkl_currpath = path + pkl_date_string
        csv_file = Path(csv_currpath)
        pkl_file = Path(pkl_currpath)
        if csv_file.exists():
            df = pd.read_csv(csv_currpath)
            try:
                try:
                    df = df.drop('datetime.1', axis=1)
                    df["datetime"] = pd.to_datetime(df["datetime"])
                except:
                    df['datetime'] = df['date'] + ' ' + df['time']
                    df["datetime"] = pd.to_datetime(df["datetime"])
            except: # THIS EXCEPTION OCCURS WHEN BACKTESTING ON LIVE STORED DATA
                df["datetime"] = pd.to_datetime(df["datetime"])

            df = df.set_index(df['datetime'])
            mask1 = df.index.time >= entertime
            mask2 = df['symbol'] == symbol
            spotdata = df[mask1 & mask2]
            spotdata.drop_duplicates(subset=['datetime'], inplace=True)
            resampled = Resample(spotdata, freq)
            resampled = resampled.apply(pd.to_numeric)
            resampled.dropna(inplace=True)
            resampled = getTI(resampled, TIconfig)
            df_list.append(resampled)
        elif pkl_file.exists():
            df = pd.read_pickle(pkl_currpath)
            try:
                try:
                    df = df.drop('datetime.1', axis=1)
                    df["datetime"] = pd.to_datetime(df["datetime"])
                except:
                    df['datetime'] = df['date'] + ' ' + df['time']
                    df["datetime"] = pd.to_datetime(df["datetime"])
            except: # THIS EXCEPTION OCCURS WHEN BACKTESTING ON LIVE STORED DATA
                df["datetime"] = pd.to_datetime(df["datetime"])
                
            df = df.set_index(df['datetime'])
            mask1 = df.index.time >= entertime
            mask2 = df['symbol'] == symbol
            spotdata = df[mask1 & mask2]
            spotdata.drop_duplicates(subset=['datetime'], inplace=True)
            resampled = Resample(spotdata, freq)
            resampled = resampled.apply(pd.to_numeric)
            resampled.dropna(inplace=True)
            resampled = getTI(resampled, TIconfig)
            df_list.append(resampled)
        # start_date += delta
    finaldf = pd.concat(df_list)
    return finaldf

# Check entry condition based on the TIconfig
def CheckEntryCondition(currentcandle, TIconfig):
    # Check bullish condition
    bull = True
    bear = True
    for t in TIconfig:
        bull = bull and t["BullOperator"](currentcandle[t["columnname"]], t["ThreshBull"])
        bear = bear and t["BearOperator"](currentcandle[t["columnname"]], t["ThreshBear"])    
    return (bull, bear)

def UpdatePosition(masterdf, positions):
    if (len(positions) > 0):
        for pos in positions:
            if (pos["Active"]):
                pos["OpData"] = masterdf[masterdf['symbol'] == pos["OpSymbol"]]
                pos["FutData"] = masterdf[masterdf['symbol'] == pos['symbol'] + "-I"]
    return positions

def EnterPosition(generalconfig, positionconfig, masterdf, positions, nextcandle, OHLC, stance):
    positionsNotPlaced = []
    for posc in positionconfig:
        if (posc["Stance"] == stance):
            exp = atom.GetExpiry(masterdf, generalconfig["symbol"])
            if generalconfig['symbol'] == defs.N :
                cst = nextcandle[OHLC]
                cst = int(round(cst / 50, 0) * 50)
            elif generalconfig['symbol'] == defs.BN :
                cst = nextcandle[OHLC]
                cst = int(round(cst / 100, 0) * 100)
            elif generalconfig['symbol'] == defs.FN :
                cst = nextcandle[OHLC]
                cst = int(round(cst / 50, 0)*50)
            opdf = masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]]
            futdf = masterdf[masterdf['symbol'] == generalconfig['symbol'] + "-I"]
            #spotdf = masterdf[masterdf['symbol'] == generalconfig['symbol']]
            # print(config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"])
            if nextcandle.name in opdf.index : # and nextcandle.name in opdf.index :
                price = opdf.loc[nextcandle.name][OHLC]
                futprice = futdf.loc[nextcandle.name][OHLC] #* (1 + generalconfig["Slippage"] * posc["Action"] / 100)
                enterprice = price * (1 + generalconfig["Slippage"] * posc["Action"] / 100)
                enterspotprice = nextcandle[OHLC] #*(1 + generalconfig["Slippage"] * posc["Action"] / 100)
                position = {"EnterPrice": enterprice, "PositionConfig": posc, "Expiry":exp, "StrikePrice": cst + posc["Delta"],
                    "OpSymbol": generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"],
                    "OpData": masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]],
                    "FutData": futdf, 
                    "Entertime": nextcandle.name.time(), "Qty": generalconfig["LotSize"] * posc["NumLots"],
                    "date": nextcandle.name.date(),                    
                    "EnterSpotPrice": enterspotprice,
                    "Active": True, "Strike": cst + posc["Delta"],
                    "symbol": generalconfig['symbol'], "trades":{}, "stance": stance, "Slippage": generalconfig['Slippage'],
                    "FutEnterPrice":futprice, "TrailMul": 1}
                if (posc["SL"] == defs.YES):
                    position["SLCond"] = enterprice - posc["Action"]*enterprice*posc["SLPc"]/100
                if (posc["Target"] == defs.YES):
                    position["TargetCond"] = enterprice + posc["Action"]*enterprice*posc["TargetPc"]/100
                positions.append(position)
            else:
                positionsNotPlaced.append(posc)
    return (positions, positionsNotPlaced)

def EnterPositionStrike(generalconfig, positionconfig, masterdf, positions, nextcandle, OHLC, stance, strike):
    positionsNotPlaced = []
    for posc in positionconfig:
        if (posc["Stance"] == stance):
            exp = atom.GetExpiry(masterdf, generalconfig["symbol"])
            opdf = masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(strike) + posc["Type"]]
            futdf = masterdf[masterdf['symbol'] == generalconfig['symbol'] + "-I"]
            #spotdf = masterdf[masterdf['symbol'] == generalconfig['symbol']]
            # print(config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"])
            if nextcandle.name in opdf.index : # and nextcandle.name in opdf.index :
                price = opdf.loc[nextcandle.name][OHLC]
                futprice = futdf.loc[nextcandle.name][OHLC] #* (1 + generalconfig["Slippage"] * posc["Action"] / 100)
                enterprice = price * (1 + generalconfig["Slippage"] * posc["Action"] / 100)
                enterspotprice = nextcandle[OHLC] #*(1 + generalconfig["Slippage"] * posc["Action"] / 100)
                position = {"EnterPrice": enterprice, "PositionConfig": posc, "Expiry":exp, "StrikePrice": strike,
                    "OpSymbol": generalconfig["symbol"] + exp + str(strike) + posc["Type"],
                    "OpData": masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(strike) + posc["Type"]],
                    "FutData": futdf, 
                    "Entertime": nextcandle.name.time(), "Qty": generalconfig["LotSize"] * posc["NumLots"],
                    "date": nextcandle.name.date(),                    
                    "EnterSpotPrice": enterspotprice,
                    "Active": True, "Strike": strike,
                    "symbol": masterdf.iloc[0]['symbol'], "trades":{}, "stance": stance, "Slippage": generalconfig['Slippage'],
                    "FutEnterPrice":futprice }
                if (posc["SL"] == defs.YES):
                    position["SLCond"] = enterprice - posc["Action"]*enterprice*posc["SLPc"]/100
                if (posc["Target"] == defs.YES):
                    position["TargetCond"] = enterprice + posc["Action"]*enterprice*posc["TargetPc"]/100
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
         
def CheckStopLossTI(positions, currentcandle, nextcandle, TIconfig):
    positionstoExit = []
    for pos in positions:
        if currentcandle.name in pos['OpData'].index and nextcandle.name.time() != pos['Entertime']: #and nextcandle.name in pos['OpData'].index :
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

def CheckTargetConditionTI(positions, currentcandle, nextcandle, TIconfig):
    positionstoExit = []
    for pos in positions:
        if currentcandle.name in pos['OpData'].index and nextcandle.name.time() != pos['Entertime']: #and nextcandle.name in pos['OpData'].index :
            (TargetCondBull, TargetCondBear) = CheckTargetConditionStance(pos["stance"], currentcandle, TIconfig)          
            if (TargetCondBull and pos["Active"]):
                positionstoExit.append(pos)
            if (TargetCondBear and pos["Active"]):
                positionstoExit.append(pos)
    return positionstoExit

def CheckActivePositions(positions):
    Active = False
    for pos in positions:
        if pos['Active'] :
            Active = True
    return Active

def ExitPosition(positionstoExit, currentcandle, ExitReason, OHLC):
    for pos in positionstoExit:
        if (pos["Active"]):
            Str = ""
            if (pos["PositionConfig"]["Action"] == defs.BUY):
                Str = "Buy "
            elif (pos["PositionConfig"]["Action"] == defs.SELL):
                Str = "Sell "
            Str = Str + pos["PositionConfig"]["Type"]
            if (ExitReason == defs.SL):
                if currentcandle.name in pos["OpData"].index:
                # OHLC = close
                    exitprice = pos["OpData"].loc[currentcandle.name][OHLC]
                    exitReason = "SL HIT"
            elif (ExitReason == defs.TARGET):
                if currentcandle.name in pos["OpData"].index:
                # OHLC = close
                    exitprice = pos["OpData"].loc[currentcandle.name][OHLC]
                    exitReason = "Target Hit"
            elif (ExitReason == defs.SQUAREOFF):
                if currentcandle.name in pos["OpData"].index:
                    # OHLC = close
                    exitprice = pos["OpData"].loc[currentcandle.name][OHLC]
                    exitReason = "Square Off"
                else:
                    idx = pos["OpData"].index[pos["OpData"].index.get_loc(currentcandle.name, method='nearest')]
                    exitprice = pos["OpData"][idx]

            elif (ExitReason == defs.SQUAREOFFEOD):
                if currentcandle.name in pos["OpData"].index:
                    # OHLC = open
                    exitprice = pos["OpData"].loc[currentcandle.name][OHLC]
                    exitReason = "Square Off EOD"
                else:
                    if pos["OpData"].empty:
                        return
                    else:
                        idx = pos["OpData"].index[pos["OpData"].index.get_loc(currentcandle.name, method='nearest')]
                        exitprice = pos["OpData"].loc[idx][OHLC]                      
                        exitReason = "Square Off EOD"
            enterprice = pos['EnterPrice']
            futenterprice = pos['FutEnterPrice']
            if currentcandle.name in pos["OpData"].index:
                futexitprice = pos['FutData'].loc[currentcandle.name][OHLC]
            else:
                idx = pos["FutData"].index[pos["FutData"].index.get_loc(currentcandle.name, method='nearest')]
                futexitprice = pos["FutData"].loc[idx][OHLC]
            exitprice = exitprice*(1 - pos["Slippage"]*pos["PositionConfig"]["Action"]/100)
            pos["trades"] = {'EnterPrice': enterprice, 'ExitPrice': exitprice,
                            'EnterTime': pos['Entertime'], 'ExitTime': currentcandle.name.time(),
                            'Reason': exitReason, 'Trade Type': Str, 'EnterSpotPrice': pos["EnterSpotPrice"], "ExitSpotPrice": currentcandle['close'],
                            "Spotpnl":(currentcandle['close'] - pos['EnterSpotPrice']) * pos['stance'] ,
                            "EnterFutPrice":futenterprice, "ExitFutPrice": futexitprice,
                            "Futpnl": (futexitprice-futenterprice) * pos['stance'] ,
                            "pnl": (exitprice - enterprice) * pos["PositionConfig"]["Action"] * pos["Qty"],
                            "date": pos["date"], "symbol": pos["OpSymbol"], "Expiry": pos['Expiry']}
            pos["Active"] = False

def ExitPositionPremium(positionstoExit, currentcandle, ExitReason, OHLC):
    for pos in positionstoExit:
        if (pos["Active"]):
            Str = ""
            if (pos["PositionConfig"]["Action"] == defs.BUY):
                Str = "Buy "
            elif (pos["PositionConfig"]["Action"] == defs.SELL):
                Str = "Sell "
            Str = Str + pos["PositionConfig"]["Type"]
            if (ExitReason == defs.SL):
                exitprice = pos["SLCond"]
                exitReason = "SL HIT"
            elif (ExitReason == defs.TARGET):
                exitprice = pos["TargetCond"]
                exitReason = "Target Hit"
            elif (ExitReason == defs.SQUAREOFF):
                if currentcandle.name in pos["OpData"].index:
                    # OHLC = close
                    exitprice = pos["OpData"].loc[currentcandle.name][OHLC]
                    exitReason = "Square Off"
                else:
                    idx = pos["OpData"].index[pos["OpData"].index.get_loc(currentcandle.name, method='nearest')]
                    exitprice = pos["OpData"][idx]
            elif (ExitReason == defs.SQUAREOFFEOD):
                if currentcandle.name in pos["OpData"].index:
                    # OHLC = open
                    exitprice = pos["OpData"].loc[currentcandle.name][OHLC]
                    exitReason = "Square Off EOD"
                else:
                    if pos["OpData"].empty:
                        return
                    else:
                        idx = pos["OpData"].index[pos["OpData"].index.get_loc(currentcandle.name, method='nearest')]
                        exitprice = pos["OpData"].loc[idx][OHLC]
                        exitReason = "Square Off EOD"
            enterprice = pos['EnterPrice']
            futenterprice = pos['FutEnterPrice']
            spotenterprice = pos['EnterSpotPrice']
            if currentcandle.name in pos["OpData"].index :
                futexitprice = pos['FutData'].loc[currentcandle.name][OHLC]
            else:
                idx = pos["FutData"].index[pos["FutData"].index.get_loc(currentcandle.name, method='nearest')]
                futexitprice = pos["FutData"].loc[idx][OHLC]
            exitprice = exitprice*(1 - pos["Slippage"]*pos["PositionConfig"]["Action"]/100)
            futexitprice = futexitprice #*(1 - pos["Slippage"]*pos["PositionConfig"]["Action"]/100)
            spotexitprice = currentcandle[OHLC] #*(1 - pos["Slippage"]*pos["PositionConfig"]["Action"]/100)
            pos["trades"] = {'EnterPrice': enterprice, 'ExitPrice': exitprice,
                             'EnterTime': pos['Entertime'], 'ExitTime': currentcandle.name.time(),
                             'Reason': exitReason, 'Trade Type': Str, 'EnterSpotPrice': pos["EnterSpotPrice"],
                             "ExitSpotPrice": spotexitprice,
                             "Spotpnl": (spotexitprice - spotenterprice) * pos['stance'],
                             "EnterFutPrice": futenterprice, "ExitFutPrice": futexitprice,
                             "Futpnl": (futexitprice - futenterprice) * pos['stance'],
                             "pnl": (exitprice - enterprice) * pos["PositionConfig"]["Action"] * pos["Qty"],
                             "date": pos["date"], "symbol": pos["OpSymbol"], "Expiry": pos['Expiry']}
            pos["Active"] = False

def FindStrike(masterdf, premium, time, startstrike, endstrike, optype, OHLC, symbol):
    if symbol == defs.N :
        inc = 50
    elif symbol == defs.BN :
        inc = 100
    elif symbol == defs.FN :
        inc = 50
    minval = 1000
    #print(optype)
    for s in range(startstrike, endstrike, inc):
        exp = atom.GetExpiry(masterdf, symbol)
        opsymbol = symbol + exp + str(s) + optype       
        currprice = atom.GetOptionPrice(masterdf, opsymbol, time, OHLC)
        if abs(currprice - premium) < minval:
            minval = abs(currprice - premium)
            currbeststrike = s
            #print(minval)
            #print(currprice)
            #print(s)
    return (currbeststrike, minval)

# jit_module()
        
