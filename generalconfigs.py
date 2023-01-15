import definitions as defs
import datetime

def GetGeneralConfigIntraday(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG, SLtoCost, REEvery):
    if (symbol == defs.BN):
        lotsize = defs.BNLOTSIZE
    elif (symbol == defs.N):
        lotsize = defs.NLOTSIZE
    generalconfig = {"SquareOffSL": SquareOffSL, "SquareOffTG": SquareOffTG,
                       "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15), "symbol": symbol,
                       "ReEntrySL": ReEntrySL, "ReEntryTG": ReEntryTG, "MaxReEnterCounterSL": MaxReEnterCounterSL,
                        "MaxReEnterCounterTG": MaxReEnterCounterTG, "SLToCost": SLtoCost, "REEvery": REEvery,
                       "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":lotsize}
    return generalconfig

def GetGeneralConfigIntradayTime(SquareOffSL, SquareOffTG, symbol, ReEnterEvery, SLtoCost, REEvery):
    if (symbol == defs.BN):
        lotsize = defs.BNLOTSIZE
    elif (symbol == defs.N):
        lotsize = defs.NLOTSIZE
    generalconfig = {"SquareOffSL": SquareOffSL, "SquareOffTG": SquareOffTG,
                       "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15), "symbol": symbol,
                       "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5,
                        "MaxReEnterCounterTG": 5, "SLToCost": SLtoCost, "REEvery": REEvery,
                       "debug": defs.DEBUGTIME, "Timerenter": defs.YES, "ReEnterEvery": ReEnterEvery, "Slippage": defs.SLIPPAGE, "LotSize":lotsize}
    return generalconfig

def GetGeneralConfigExpiry(SquareOffSL, SquareOffTG, symbol, EnterDay, ExitDay):
    if (symbol == defs.BN):
        lotsize = defs.BNLOTSIZE
    elif (symbol == defs.N):
        lotsize = defs.NLOTSIZE
    generalconfig = {"SquareOffSL": SquareOffSL, "SquareOffTG": SquareOffTG, "EnterDay": EnterDay,
                             "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15),
                             "ExitDay": ExitDay, "symbol": symbol,
                             "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5,
                             "MaxReEnterCounterTG": 5,
                             "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5,
                             "Slippage": defs.SLIPPAGE, "LotSize": lotsize}
    return generalconfig

def GetGeneralConfigNextDay(SquareOffSL, SquareOffTG, symbol, EnterDay, ExitDay):
    if (symbol == defs.BN):
        lotsize = defs.BNLOTSIZE
    elif (symbol == defs.N):
        lotsize = defs.NLOTSIZE
    generalconfig = {"SquareOffSL":SquareOffSL,"SquareOffTG":SquareOffTG, "EnterDay": EnterDay,
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": ExitDay, "symbol":symbol,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE}
    return generalconfig




generalconfigNextDayBNMW = {"name":" NextdayBNMW", "SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.TUE, defs.WED, defs.THU], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE}

generalconfigNextDayBNF = {"name":"NextDayBNF" ,"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE}

generalconfigNextDayBNMF = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED,defs.THU,defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON,defs.TUE, defs.WED, defs.THU,defs.FRI], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":50}

generalconfigExpiryBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON],
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "ExitDay": [defs.THU], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE}

generalconfigIntradayBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": 5, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5, "SLToCost": defs.YES, "REEvery": 1,
                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE}

generalconfigIntradayREBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5, "SLToCost": defs.YES, "REEvery": 1,
                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE}

generalconfigNextDayNMW = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.TUE, defs.WED, defs.THU], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE}

generalconfigNextDayNF = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE}

generalconfigNextDayNMF = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED,defs.THU,defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON,defs.TUE, defs.WED, defs.THU,defs.FRI], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":50}

generalconfigExpiryN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON],
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "ExitDay": [defs.THU], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE}

generalconfigIntradayN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5, "SLToCost": defs.YES, "REEvery": 1,
                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE}

generalconfigIntradayREN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.N,
                     "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5, "SLToCost": defs.YES, "REEvery": 1,
                     "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE}

def GetGeneralConfigIntradaySA(symbol):
    if symbol == defs.BN :
        generalconfig = [generalconfigIntradayBN, generalconfigIntradayN]
    else :
        generalconfig = [generalconfigIntradayN, generalconfigIntradayBN]

    return generalconfig

# Directional Strategies config

generalconfigBNRSIADX = {"name":"BNRSIADX" , "symbol":defs.BN,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3,
                        "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}
generalconfigNRSIADX = {"name":"NRSIADX", "symbol":defs.N, "EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3,
                        "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}


generalconfigBNRSI2 = {"name":"NBNRSI2","symbol":defs.BN, "EnterTime": datetime.time(9,15) ,"ExitTime": datetime.time(15,15), "Resample": 10,
                    "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "Rolling": defs.YES, "Reenter": defs.YES, "SLTGContinuous": defs.NO}
generalconfigNRSI2 = {"name":"NRSI2","symbol":defs.N, "EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 10,
                    "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "Rolling": defs.YES, "Reenter": defs.YES, "SLTGContinuous": defs.NO}

generalconfigBNMA = {"name":"BNEMA","symbol":defs.BN, "EnterTime": datetime.time(9,15) ,"ExitTime": datetime.time(15,15), "Resample": 3,
                    "StopLoss": False, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}
generalconfigNMA = {"name":"NEMA","symbol":defs.N, "EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3,
                    "StopLoss": False, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}

generalconfigBNRSIDual = {"name":"BNRSIDual", "symbol":defs.BN, "EnterTime": datetime.time(9,30) ,"ExitTime": datetime.time(15,15), "Resample": 10,
                        "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}
generalconfigNRSIDual = {"name":"BNRSIDual", "symbol":defs.N, "EnterTime": datetime.time(9,30), "ExitTime": datetime.time(15,15), "Resample": 10, 
                        "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}

generalconfigBNBB2 = {"name":"BNBB","symbol":defs.BN,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 5,
                    "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}
generalconfigNBB2 = {"name":"NBB","symbol":defs.N,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3, 
                    "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}

generalconfigBNBB1 = {"name":"BNBB","symbol":defs.BN,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3, 
                    "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "Rolling": defs.YES, "Reenter": defs.YES, "SLTGContinuous": defs.NO}
generalconfigNBB1 = {"name":"NBB","symbol":defs.N,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3, 
                    "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "Rolling": defs.YES, "Reenter": defs.YES, "SLTGContinuous": defs.NO}

generalconfigBNST = {"name":"BNST","symbol":defs.BN,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3, 
                    "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased", 
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}
generalconfigNST = {"name":"NST","symbol":defs.N, "EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": 3, 
                    "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "Rolling": defs.NO, "Reenter": defs.YES, "SLTGContinuous": defs.NO}



