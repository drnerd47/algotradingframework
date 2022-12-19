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
        # masterdf['low'] = masterdf['low'].astype(float)
        # masterdf['open'] = masterdf['open'].astype(float)
        # masterdf['high'] = masterdf['high'].astype(float)
        # masterdf['close'] = masterdf['close'].astype(float)
    return masterdf

def GetOptionPriceAtomic(masterdf, symbol, type, strikeprice, time, HLOC, generalconfig):
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
    elif (symbol == defs.N):
        return masterdf.iloc[0]['symbol'][5:12]
    else:
        print("Unknown Symbol")
        return 0

def GetSpotData(masterdf, symbol):
    return masterdf[masterdf['symbol'] == symbol]

def UpdatePosition(masterdf, positions):
    if (len(positions) > 0):
        for pos in positions:
            if (pos["Active"]):
                pos["OpData"] = masterdf[masterdf['symbol'] == pos["OpSymbol"]]
    return positions
    
def EnterPosition(generalconfig, positionconfig, masterdf, positions, currentcandle, OHLC):
    positionsNotPlaced = []
    for posc in positionconfig:
        exp = GetExpiry(masterdf, generalconfig["symbol"])
        if generalconfig['symbol'] == defs.N :
            cst = currentcandle[OHLC]
            cst = int(round(cst / 50, 0)*50)
        elif generalconfig['symbol'] == defs.BN :
            cst = currentcandle[OHLC]
            cst = int(round(cst / 100, 0) * 100)
        opdf = masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]]
        # print(config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"])
        if currentcandle.name in opdf.index:
            price = opdf.loc[currentcandle.name][OHLC]
            enterprice = price * (1 + generalconfig["Slippage"] * posc["Action"] / 100)
            position = {"EnterPrice": enterprice, "PositionConfig": posc, "Expiry":exp, "StrikePrice": cst + posc["Delta"],
                  "OpSymbol": generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"],
                "OpData": masterdf[masterdf['symbol'] == generalconfig["symbol"] + exp + str(cst + posc["Delta"]) + posc["Type"]],
                  "Entertime": currentcandle.name.time(), "Qty": generalconfig["LotSize"] * posc["NumLots"],
                   "date": currentcandle.name.date(), 
                  "SLCond": enterprice - posc["Action"] * enterprice * posc["SLPc"] / 100,
                  "TargetCond": enterprice + posc["Action"] * enterprice * posc["TargetPc"] / 100,
                  "Active": True, "Strike": cst + posc["Delta"],
                  "symbol": masterdf.iloc[0]['symbol'], "trades":{}, "Slippage": generalconfig['Slippage'] }
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
                optionprice = pos["OpData"].loc[currentcandle.name]['high']
                if (pos["PositionConfig"]["SL"] == defs.YES) and optionprice >= pos['SLCond'] and pos['Active']:
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                optionprice = pos["OpData"].loc[currentcandle.name]['low']
                optionprice = pd.to_numeric(optionprice)
                if (pos["PositionConfig"]["SL"] == defs.YES) and optionprice <= pos['SLCond'] and pos['Active']:
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
                if (pos["PositionConfig"]["Target"] == defs.YES) and optionprice <= pos['TargetCond'] and pos['Active']:
                    positionstoExit.append(pos)
                    posconfigtoExit.append(pos["PositionConfig"])
            elif (pos["PositionConfig"]["Action"] == defs.BUY):
                if (pos["PositionConfig"]["Target"] == defs.YES) and optionprice >= pos['TargetCond'] and pos['Active']:
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
            #enterprice = enterprice*(1 + pos["Slippage"]*pos["PositionConfig"]["Action"]/100)
            exitprice = exitprice*(1 - pos["Slippage"]*pos["PositionConfig"]["Action"]/100)
            pos["trades"] = {'EnterPrice': enterprice , 'ExitPrice': exitprice,
                            'EnterTime': pos['Entertime'], 'ExitTime': currentcandle.name.time(),
                            'Reason': exitReason, 'Trade Type': Str,
                            "pnl": (exitprice - enterprice) * pos["PositionConfig"]["Action"] * pos["Qty"],
                            "date": pos["date"], "symbol": pos["OpSymbol"], "Expiry" : pos["Expiry"] }
                        
            pos["Active"] = False

def GetFinalTrades(positions):
    trades = pd.DataFrame()
    for pos in positions:
        trades = trades.append(pos["trades"], ignore_index=True)
    #trades = trades.append(trades, ignore_index=True)
    return trades











