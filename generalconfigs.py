import definitions as defs
import datetime

def GetGeneralConfigIntraday(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG, slippage, lotsize):
    generalconfig = {"SquareOffSL": SquareOffSL, "SquareOffTG": SquareOffTG,
                       "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15), "symbol": symbol,
                       "ReEntrySL": ReEntrySL, "ReEntryTG": ReEntryTG, "MaxReEnterCounterSL": MaxReEnterCounterSL, "MaxReEnterCounterTG": MaxReEnterCounterTG,
                       "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": slippage, "LotSize":lotsize}
    return generalconfig

def GetGeneralConfigIntradayTime(SquareOffSL, SquareOffTG, symbol, ReEnterEvery, slippage, lotsize):
    generalconfig = {"SquareOffSL": SquareOffSL, "SquareOffTG": SquareOffTG,
                       "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15), "symbol": symbol,
                       "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                       "debug": defs.DEBUGTIME, "Timerenter": defs.YES, "ReEnterEvery": ReEnterEvery, "Slippage": slippage, "LotSize":lotsize}
    return generalconfig

generalconfigNextDayBNMW = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.TUE, defs.WED, defs.THU], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}

generalconfigNextDayBNF = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}

generalconfigExpiryBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON],
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "ExitDay": [defs.THU], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}

generalconfigIntradayBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}

generalconfigIntradayREBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}

generalconfigNextDayNMW = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.TUE, defs.WED, defs.THU], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigNextDayNF = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigExpiryN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON],
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "ExitDay": [defs.THU], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigIntradayN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigIntradayREN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.N,
                     "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigBNRSIADX = {"symbol":defs.BN, "ExitTime": datetime.time(15,15), "Resample": '3T', "StopLoss": True, "Target": False, "StopLossCond": "TIBased", "TargetCond": "TIBased", 
                        "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}
generalconfigNRSIADX = {"symbol":defs.N, "ExitTime": datetime.time(15,15), "Resample": '3T', "StopLoss": True, "Target": False, "StopLossCond": "TIBased", "TargetCond": "TIBased", 
                        "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigBNRSI2 = {"symbol":defs.BN, "ExitTime": datetime.time(15,15), "Resample": '10T', "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased", 
                        "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}
generalconfigNRSI2 = {"symbol":defs.N, "ExitTime": datetime.time(15,15), "Resample": '10T', "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased", 
                        "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigBNBB = {"symbol":defs.BN, "ExitTime": datetime.time(15,15), "Resample": '3T', "StopLoss": True, "Target": True, "StopLossCond": "TIBased", "TargetCond": "TIBased", 
                    "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}
generalconfigNBB = {"symbol":defs.N, "ExitTime": datetime.time(15,15), "Resample": '3T', "StopLoss": True, "Target": True, "StopLossCond": "TIBased", "TargetCond": "TIBased", 
                    "Slippage": 0.5, "LotSize":defs.NLOTSIZE}

generalconfigBNST = {"symbol":defs.BN, "ExitTime": datetime.time(15,15), "Resample": '3T', "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased", 
                    "Slippage": 0.5, "LotSize":defs.BNLOTSIZE}
generalconfigNST = {"symbol":defs.N, "ExitTime": datetime.time(15,15), "Resample": '3T', "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased", 
                    "Slippage": 0.5, "LotSize":defs.NLOTSIZE}



