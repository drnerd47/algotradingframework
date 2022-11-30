import pandas as pd
from pathlib import Path
import definitions as defs
import time

def LoadDF(currpath):
    my_file = Path(currpath)
    if my_file.exists():
        masterdf = pd.read_csv(currpath)
        masterdf = masterdf.drop('datetime.1', axis=1)
        masterdf["datetime"] = pd.to_datetime(masterdf["datetime"])
        masterdf = masterdf.set_index(masterdf['datetime'])
    return masterdf

def GetOptionPriceAtomic(masterdf, symbol, type, strikeprice, time, HLOC):
    exp = GetExpiry(masterdf, generalconfig["symbol"])
    cst = strikeprice
    cst = int(round(cst / 100, 0) * 100)
    price = masterdf[masterdf['symbol'] == symbol + exp + str(cst) + type].loc[time][
        HLOC]
    return price

def GetOptionPrice(masterdf, opsymbol, time, HLOC):
    opdf = masterdf[masterdf['symbol'] == opsymbol]
    if time in opdf.index:
        price = masterdf[masterdf['symbol'] == opsymbol].loc[time][HLOC]
    else:
        price = -1
    return price

def GetExpiry(masterdf, symbol):
    if (symbol == defs.BN):
        return masterdf.iloc[0]['symbol'][9:16]
    elif (symbol == defs.NIFTY):
        return masterdf.iloc[0]['symbol'][5:12]
    else:
        print("Get Expiry: Come to the Else part")
        return 0

def GetSpotData(masterdf, symbol):
    return masterdf[masterdf['symbol'] == symbol]

def EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, OHLC):
    print("Entering Position!")
    exp = GetExpiry(masterdf, generalconfig["symbol"])
    cst = currentcandle[OHLC]
    cst = int(round(cst / 100, 0) * 100)
    positionsNotPlaced = []
    for posc in positionconfig:
        opdf = masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]]
        # print(config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"])
        if currentcandle.name in opdf.index:
            price = opdf.loc[currentcandle.name][OHLC]
            position = {"EnterPrice": price, "PositionConfig": posc, "Expiry":exp, "StrikePrice": cst + posc["Delta"],
                  "OpSymbol": generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"],
                "OpData": masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]],
                  "Entertime": currentcandle.name.time(), "Qty": 25 * posc["LotSize"],
                   "date": currentcandle.name.date(),
                  "SLCond": price - posc["Action"] * price * posc["SLPc"] / 100,
                  "TargetCond": price + posc["Action"] * price * posc["TargetPc"] / 100,
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
            optionprice = pos["OpData"].loc[currentcandle.name]['high']
            if (pos["PositionConfig"]["Action"] == defs.SELL):
                if optionprice >= pos['SLCond'] and pos['Active'] and (pos["PositionConfig"]["SL"] == defs.YES):
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                if optionprice <= pos['SLCond'] and pos['Active'] and (pos["PositionConfig"]["SL"] == defs.YES):
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
                if optionprice <= pos['TargetCond'] and pos['Active'] and (pos["PositionConfig"]["Target"] == defs.YES):
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                if optionprice >= pos['TargetCond'] and pos['Active'] and (pos["PositionConfig"]["Target"] == defs.YES):
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
                exitprice = pos["SLCond"]
                exitReason = "SL HIT"
            elif (ExitReason == defs.TARGET):
                exitprice = pos["TargetCond"]
                exitReason = "Target Hit"
            elif (ExitReason == defs.SQUAREOFF):
                if currentcandle.name in pos["OpData"].index:
                    exitprice = pos["OpData"].loc[currentcandle.name]['close']
                    exitReason = "Square Off"
            elif (ExitReason == defs.SQUAREOFFEOD):
                if currentcandle.name in pos["OpData"].index:
                    exitprice = pos["OpData"].loc[currentcandle.name]['open']
                    exitReason = "Square Off"
            enterprice = pos['EnterPrice']
            pos["trades"] = {'EnterPrice': enterprice, 'ExitPrice': exitprice, 'EnterTime': pos['Entertime'], 'ExitTime': currentcandle.name.time(),
                     'Reason': exitReason, 'Trade Type': Str,
                     "pnl": (exitprice - enterprice) * pos["PositionConfig"]["Action"] * pos["Qty"],
                     "date": pos["date"], "symbol": pos["OpSymbol"]}
            pos["Active"] = False

def GetFinalTrades(positions):
    trades = pd.DataFrame()
    for pos in positions:
        trades = trades.append(pos["trades"], ignore_index=True)
    #trades = trades.append(trades, ignore_index=True)
    trades["Cummulative pnl"] = trades['pnl'].cumsum()
    trades["Daily pnl"] = trades.groupby("date")["pnl"].cumsum()
    trades["Daily Cummulative pnl"] = trades['pnl'].cumsum()
    trades["Daily pnl"][0::2] = 0
    return trades


# def GetMultipledayData(start_date, end_date, currpath):
#     df = LoadDF(currpath)






