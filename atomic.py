import pandas as pd
from pathlib import Path
import definitions as defs

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

def EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle):
    print("Entering Position!")
    exp = GetExpiry(masterdf, generalconfig["symbol"])
    cst = currentcandle['open']
    cst = int(round(cst / 100, 0) * 100)
    positionsNotPlaced = []
    for posc in positionconfig:
        price = GetOptionPrice(masterdf, generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"], currentcandle.name, "open")
        if (price != -1):
            position = {"EnterPrice": price, "PositionConfig": posc, "Expiry":exp, "StrikePrice": cst + posc["Delta"],
                  "OpSymbol": generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"],
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

def CheckStopLoss(masterdf, positions, currentcandle):
    positionstoExit = []
    for pos in positions:
        optionprice = GetOptionPrice(masterdf, pos["OpSymbol"], currentcandle.name, 'high')
        if (optionprice != -1):
            if (pos["PositionConfig"]["Action"] == defs.SELL):
                if optionprice >= pos['SLCond'] and pos['Active'] and (pos["PositionConfig"]["SL"] == defs.YES):
                    positionstoExit.append(pos)
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                if optionprice <= pos['SLCond'] and pos['Active'] and (pos["PositionConfig"]["SL"] == defs.YES):
                    positionstoExit.append(pos)
    return positionstoExit

def CheckTargetCondition(masterdf, positions, currentcandle):
    positionstoExit = []
    for pos in positions:
        optionprice = GetOptionPrice(masterdf, pos["OpSymbol"], currentcandle.name, 'high')
        if (optionprice != -1):
            if (pos["PositionConfig"]["Action"] == defs.SELL):
                if optionprice <= pos['TargetCond'] and pos['Active'] and (pos["PositionConfig"]["Target"] == defs.YES):
                    positionstoExit.append(pos)
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                if optionprice >= pos['TargetCond'] and pos['Active'] and (pos["PositionConfig"]["Target"] == defs.YES):
                    positionstoExit.append(pos)
    return positionstoExit

def ExitPosition(masterdf, positionstoExit, currentcandle, ExitReason):
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
            elif (ExitReason == defs.TARGET):
                exitprice = pos["TargetCond"]
            elif (ExitReason == defs.SQUAREOFF):
                exitprice = GetOptionPrice(masterdf, pos["OpSymbol"], currentcandle.name, 'close')

            enterprice = pos['EnterPrice']
            pos["trades"] = {'EnterPrice': enterprice, 'ExitPrice': exitprice, 'ExitTime': currentcandle.name.time(),
                     'Reason': "SL HIT", 'Trade Type': Str,
                     "pnl": (enterprice - exitprice) * pos["PositionConfig"]["Action"] * pos["Qty"],
                     "date": pos["date"], "symbol": pos["symbol"]}
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




