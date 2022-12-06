import definitions as defs
import datetime

def GetGeneralConfigIntraday(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG):
    generalconfig = {"SquareOffSL": SquareOffSL, "SquareOffTG": SquareOffTG,
                       "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15), "symbol": symbol,
                       "ReEntrySL": ReEntrySL, "ReEntryTG": ReEntryTG, "MaxReEnterCounterSL": MaxReEnterCounterSL, "MaxReEnterCounterTG": MaxReEnterCounterTG,
                       "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}
    return generalconfig

def GetGeneralConfigIntradayTime(SquareOffSL, SquareOffTG, symbol, ReEnterEvery):
    generalconfig = {"SquareOffSL": SquareOffSL, "SquareOffTG": SquareOffTG,
                       "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15), "symbol": symbol,
                       "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                       "debug": defs.DEBUGTIME, "Timerenter": defs.YES, "ReEnterEvery": ReEnterEvery}
    return generalconfig

generalconfigNextDayBNMW = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.TUE, defs.WED, defs.THU], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME}

generalconfigNextDayBNF = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME}

generalconfigExpiryBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON],
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "ExitDay": [defs.THU], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}

generalconfigIntradayBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}

generalconfigIntradayREBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}

generalconfigNextDayNMW = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON, defs.TUE, defs.WED],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.TUE, defs.WED, defs.THU], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME}

generalconfigNextDayNF = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.FRI],
                     "EnterTime":datetime.time(15,15),"ExitTime":datetime.time(9,30), "ExitDay": [defs.MON], "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME}

generalconfigExpiryN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG, "EnterDay": [defs.MON],
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "ExitDay": [defs.THU], "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}

generalconfigIntradayN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}

generalconfigIntradayREN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}