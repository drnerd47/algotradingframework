import definitions as defs
import datetime
import operator
import generalconfigs as genconfigs
import positionconfigs as posconfigs

def GetINDStraddles(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG, SLtoCost, REEvery,
                    SL, Target, SLPc, TargetPc, TrailSL, EnterTime, ExitTime):
    generalconfig = genconfigs.GetGeneralConfigIntraday(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG, SLtoCost, REEvery, TrailSL,
                                                        EnterTime, ExitTime)
    positionconfig = posconfigs.getStraddles(defs.SELL, SL, Target, SLPc, TargetPc)
    return (generalconfig, positionconfig)

def GetINDStraddlesConfig(config):
    SquareOffSL = config['SquareOffSL']
    SquareOffTG = config['SquareOffTG']
    symbol = config['symbol']
    ReEntrySL = config['ReEntrySL']
    ReEntryTG = config['ReEntryTG']
    MaxReEnterCounterSL = config['MaxReEnterCounterSL'] 
    MaxReEnterCounterTG = config['MaxReEnterCounterTG']
    SL = config['SL']
    Target = config['Target']
    SLPc = config['SLPc']
    TargetPc = config['TargetPc']
    SLtoCost = config['SLtoCost']
    REEvery = config['REEvery']
    TrailSL = config["TrailSL"]
    EnterTime = config["EnterTime"]
    ExitTime = config["ExitTime"]
    (generalconfig, positionconfig) = GetINDStraddles(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG,
                                                       SLtoCost, REEvery, SL, Target, SLPc, TargetPc, TrailSL, EnterTime, ExitTime)
                                                    
    return (generalconfig, positionconfig)
##############################################################################################################################
def GetINDStrangles(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG, SLtoCost, REEvery,
                    SL, Target, SLPc, TargetPc, Delta, TrailSL, EnterTime, ExitTime):
    generalconfig = genconfigs.GetGeneralConfigIntraday(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG, SLtoCost, REEvery, TrailSL,
                                                        EnterTime, ExitTime)
    positionconfig = posconfigs.getStrangles(defs.SELL, Delta, SL, Target, SLPc, TargetPc)
    return (generalconfig, positionconfig)

def GetINDStranglesConfig(config):
    SquareOffSL = config['SquareOffSL']
    SquareOffTG = config['SquareOffTG']
    symbol = config['symbol']
    ReEntrySL = config['ReEntrySL']
    ReEntryTG = config['ReEntryTG']
    MaxReEnterCounterSL = config['MaxReEnterCounterSL'] 
    MaxReEnterCounterTG = config['MaxReEnterCounterTG']
    SL = config['SL']
    Target = config['Target']
    SLPc = config['SLPc']
    TargetPc = config['TargetPc']
    SLtoCost = config['SLtoCost']
    REEvery = config['REEvery']
    Delta = config["Delta"]
    TrailSL = config["TrailSL"]
    EnterTime = config["EnterTime"]
    ExitTime = config["ExitTime"]
    (generalconfig, positionconfig) = GetINDStrangles(SquareOffSL, SquareOffTG, symbol, ReEntrySL, ReEntryTG, MaxReEnterCounterSL, MaxReEnterCounterTG,
                                                    SLtoCost, REEvery, SL, Target, SLPc, TargetPc, Delta, TrailSL, EnterTime, ExitTime)
    return (generalconfig, positionconfig)
##############################################################################################################################
def GetRSI2ConfigsPB(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2, symbol, action, rolling, reenter, Delta, window1, window2, SLTGContinuous, TrailSL, MaxReEnterCount):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":action,"Delta":-1*Delta, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": putstance, "SLPc": SLPc, "TargetPc": TargetPc}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE
    generalconfig = {"symbol": symbol, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                           "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased",
                           "TargetCond": "PremiumBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter,
                     "SLTGContinuous": SLTGContinuous, "TrailSL": TrailSL, 'MaxReEnterCounter':MaxReEnterCount}

    ticonfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": TBull1, "ThreshBear": TBear1, "Window": window1, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.lt, "BearOperator": operator.gt},
        {"TI": "RSI", "columnname": "RSI2", "Window": window2, "ThreshBull": TBull2, "ThreshBear": TBear2, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.lt, "BearOperator": operator.gt}]
    return (ticonfig, generalconfig, positionconfig)

def GetRSI2Config(config):
    SL = config["SL"]
    Target = config["Target"]
    SLPc = config["SLPc"]
    window1 = config['window1']
    window2 = config['window2']
    TargetPc = config["TargetPc"]
    Resample = config["Resample"]
    TBull1 = config["TBull1"]
    TBear1 = config["TBear1"]
    TBull2 = config["TBull2"]
    TBear2 = config["TBear2"]
    symbol = config["symbol"]
    action = config["action"]
    rolling = config["rolling"]
    reenter = config["reenter"]
    Delta = config["Delta"]
    SLTGContinuous = config["SLTGContinuous"]
    TrailSL = config["TrailSL"]
    MaxReEnterCount = config['MaxReEnterCounter']
    return GetRSI2ConfigsPB(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2, symbol, action, rolling, reenter, Delta, window1, window2, SLTGContinuous, TrailSL, MaxReEnterCount)
##############################################################################################################################
def GetRSIDualConfigsPB(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2, symbol, action, rolling, reenter, Delta, window1, window2, SLTGContinuous, TrailSL, MaxReEnterCount):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":action,"Delta":-1*Delta, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": putstance, "SLPc": SLPc, "TargetPc": TargetPc}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE
    generalconfig = {"symbol": symbol, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                           "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased",
                           "TargetCond": "PremiumBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter,
                     "SLTGContinuous": SLTGContinuous, "TrailSL": TrailSL, 'MaxReEnterCounter':MaxReEnterCount}

    ticonfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": TBull1, "ThreshBear": TBear1, "Window": window1, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.gt, "BearOperator": operator.lt},
        {"TI": "RSI", "columnname": "RSI2", "Window": window2, "ThreshBull": TBull2, "ThreshBear": TBear2, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.gt, "BearOperator": operator.lt}]
    return (ticonfig, generalconfig, positionconfig)

def GetRSIDualConfig(config):
    Resample = config['Resample']
    window1 = config['window1']
    window2 = config['window2']
    TBull1 = config['TBull1']
    TBear1 = config['TBear1']
    TBull2 = config['TBull2']
    TBear2 = config['TBear2']
    SLPc = config['SLPc']
    TargetPc = config['TargetPc']
    symbol = config["symbol"]
    action = config["action"]
    rolling = config['rolling']
    reenter = config['reenter']
    Delta = config["Delta"]
    SL = config['SL']
    Target = config['Target']
    SLTGContinuous = config["SLTGContinuous"]
    TrailSL = config["TrailSL"]
    MaxReEnterCount = config['MaxReEnterCounter']
    return GetRSIDualConfigsPB(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2, symbol, action, rolling, reenter, Delta, window1, window2, SLTGContinuous, TrailSL, MaxReEnterCount)
##############################################################################################################################
def GetBB1ConfigsPB(period, Resample, TBull, TBear, SL, SLPc, Target, TargetPc, Delta, symbol, action, rolling, reenter, stddev, TrailSL, MaxReEnterCount):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc": TargetPc },
                       {"Type":defs.PUT,"Action":action,"Delta":-1*Delta, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": putstance, "SLPc": SLPc, "TargetPc": TargetPc }]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    generalconfig = {"symbol": symbol, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                    "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased",
                    "TargetCond": "PremiumBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter,
                    "SLTGContinuous": defs.NO, "TrailSL": TrailSL, 'MaxReEnterCounter':MaxReEnterCount}

    ticonfig = [{"TI": "BB", "columnname" : "bbsignal", "ThreshBull": TBull, "ThreshBear": TBear, "period": period,"stddev": stddev, "SL": defs.NO, "Target": defs.NO,
                "SLBull": 0, "SLBear": 0, "TargetBull": 0, "TargetBear": 0,
                "BullOperator": operator.lt, "BearOperator": operator.gt, "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "TBullOperator": operator.gt, "TBearOperator": operator.lt}]
    return (ticonfig, generalconfig, positionconfig)

def GetBB1Config(config):
    Resample = config['Resample']
    period = config['period']
    TBull = config['TBull']
    TBear = config['TBear']
    SL = config['SL']
    Target = config['Target']
    SLPc = config['SLPc']
    TargetPc = config['TargetPc']
    symbol = config['symbol']
    action = config['action']
    rolling = config['rolling']
    reenter = config['reenter']
    Delta = config["Delta"]
    stddev = config["stddev"]
    TrailSL = config["TrailSL"]
    MaxReEnterCount = config['MaxReEnterCounter']
    (TIconfig, generalconfig, positionconfig) = GetBB1ConfigsPB(period, Resample, TBull, TBear, SL, SLPc, Target,
                                                    TargetPc, Delta, symbol, action, rolling, reenter, stddev, TrailSL, MaxReEnterCount)
    return (TIconfig, generalconfig, positionconfig)
##############################################################################################################################
def GetBB2ConfigsPB(period, Resample, TBull, TBear, SL, SLPc, Target, TargetPc, Delta, symbol, action, rolling, reenter, stddev, SLTGContinuous, TrailSL, MaxReEnterCount):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc":TargetPc},
                       {"Type":defs.PUT,"Action":action,"Delta":-1*Delta, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": putstance, "SLPc": SLPc, "TargetPc":TargetPc}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    generalconfig = {"symbol": symbol, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                    "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased",
                    "TargetCond": "PremiumBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter,
                    "SLTGContinuous": SLTGContinuous, "TrailSL": TrailSL, 'MaxReEnterCounter':MaxReEnterCount}

    ticonfig = [{"TI": "BB", "columnname":"bbsignal", "ThreshBull": TBull, "ThreshBear": TBear, "period": period,"stddev": stddev, "SL": defs.NO, "Target": defs.NO,
                "SLBull": 0, "SLBear":0, "TargetBull": 0, "TargetBear": 0,
                "BullOperator": operator.gt, "BearOperator": operator.lt,
                "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "TBullOperator": operator.gt, "TBearOperator": operator.lt}]
    return (ticonfig, generalconfig, positionconfig)

def GetBB2Config(config):
    Resample = config['Resample']
    period = config['period']
    TBull = config['TBull']
    TBear = config['TBear']
    SL = config['SL']
    Target = config['Target']
    SLPc = config['SLPc']
    TargetPc = config['TargetPc']
    symbol = config['symbol']
    action = config['action']
    rolling = config['rolling']
    reenter = config['reenter']
    Delta = config["Delta"]
    stddev = config["stddev"]
    SLTGContinuous = config["SLTGContinuous"]
    TrailSL = config["TrailSL"]
    MaxReEnterCount = config['MaxReEnterCounter']
    (TIconfig, generalconfig, positionconfig) = GetBB2ConfigsPB(period, Resample, TBull, TBear, SL, SLPc, Target,
                                                    TargetPc, Delta, symbol, action, rolling, reenter, stddev, SLTGContinuous, TrailSL, MaxReEnterCount)
    return (TIconfig, generalconfig, positionconfig)
##############################################################################################################################
def GetRSIADXconfigsPB(action, symbol, Delta, Resample, TBull, TBear, SL, SLPc, Target, TargetPc, ADXTBull, ADXTBear, rolling, reenter, window, SLTGContinuous, TrailSL, MaxReEnterCount):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc": TargetPc, "Id": 1, "HedgeId": 0},
                       {"Type":defs.PUT,"Action":action,"Delta":-1*Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": putstance, "SLPc": SLPc, "TargetPc": TargetPc, "Id": 2, "HedgeId": 0}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    generalconfig = { "symbol":symbol,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": Resample,
                    "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":lotsize, "Rolling": rolling, "Reenter": reenter,
                      "SLTGContinuous": SLTGContinuous, "TrailSL": TrailSL, 'MaxReEnterCounter':MaxReEnterCount}

    ticonfig = [{"TI": "RSI", "columnname": "RSI", "ThreshBull": TBull, "ThreshBear": TBear, "Window": window, "SL": defs.NO, "Target": defs.NO,
            "SLBull": 0, "SLBear": 0, "TargetBull": 0, "TargetBear": 0,
             "BullOperator": operator.gt, "BearOperator": operator.lt, "SLBullOperator": operator.lt, "SLBearOperator": operator.gt,"TBullOperator": operator.gt, "TBearOperator": operator.lt},
			{"TI": "ADX","columnname":"ADX", "Window": window, "ThreshBull": ADXTBull, "ThreshBear": ADXTBear, "SL": defs.NO, "Target": defs.NO,
           "BullOperator": operator.gt, "BearOperator": operator.gt}]

    return (ticonfig, generalconfig, positionconfig)

def GetRSIADXconfig(config):
    Resample = config['Resample']
    window = config['window']
    TBull = config['TBull']
    TBear = config['TBear']
    SL = config['SL']
    Target = config['Target']
    SLPc = config['SLPc']
    TargetPc = config['TargetPc']
    ADXTBull = config['ADXTBull']
    ADXTBear = config['ADXTBear']
    symbol = config['symbol']
    action = config['action']
    rolling = config['rolling']
    reenter = config['reenter']
    Delta = config["Delta"]
    SLTGContinuous = config["SLTGContinuous"]
    TrailSL = config["TrailSL"]
    MaxReEnterCount = config['MaxReEnterCounter']
    (TIconfig, generalconfig, positionconfig) = GetRSIADXconfigsPB(action, symbol, Delta, Resample, TBull, TBear,
                                                SL, SLPc, Target, TargetPc, ADXTBull, ADXTBear, rolling, reenter, window, SLTGContinuous, TrailSL, MaxReEnterCount)
    return (TIconfig, generalconfig, positionconfig)
##############################################################################################################################
def GetEMAconfigsPB(symbol, action, Delta, TBull, TBear, period, SL, SLPc, Target, TargetPc, Resample, rolling, reenter, TrailSL, MaxReEnterCount):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc":TargetPc, "Id": 1},
                       {"Type":defs.PUT,"Action":action,"Delta":-1*Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": putstance, "SLPc": SLPc, "TargetPc":TargetPc, "Id": 2}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE
    generalconfig = {"symbol":symbol, "EnterTime": datetime.time(9,15) ,"ExitTime": datetime.time(15,15), "Resample": Resample, 
                    "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":lotsize, "Rolling": rolling, "Reenter": reenter, "SLTGContinuous": defs.YES,
                     "TrailSL": TrailSL, 'MaxReEnterCounter':MaxReEnterCount}

    ticonfig = [{"TI": "MA", "columnname":"EMA", "ThreshBull": TBull, "ThreshBear": TBear, "period": period, "SL": defs.NO, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt, "SLBull":0 , "SLBear": 0,
                "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "type": "EMA"}]

    return (ticonfig, generalconfig, positionconfig)

def GetEMAconfig(config):
    Resample = config['Resample']
    period = config['period']
    TBull = config['TBull']
    TBear = config['TBear']
    SL = config['SL']
    SLPc = config['SLPc']
    Target = config['Target']
    TargetPc = config['TargetPc']
    symbol = config['symbol']
    action = config['action']
    rolling = config['rolling']
    reenter = config['reenter']
    Delta = config["Delta"]
    TrailSL = config["TrailSL"]
    MaxReEnterCount = config['MaxReEnterCounter']
    return GetEMAconfigsPB(symbol, action, Delta, TBull, TBear, period, SL, SLPc, Target, TargetPc, Resample, rolling, reenter, TrailSL, MaxReEnterCount)
##############################################################################################################################
def GetSTconfigsPB(action, Delta, symbol, period, multiplier, Resample, rolling, reenter, SL, SLPc, Target, TargetPc, SLTGContinuous, TrailSL, MaxReEnterCount):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": putstance, "SLPc": SLPc, "TargetPc": TargetPc}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    ticonfig = [{"TI": "ST", "columnname":"ST", "ThreshBull": 0, "ThreshBear": 0, "period": period,"multiplier":multiplier, "SL": defs.NO, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt}]

    generalconfig = {"name":"BNST","symbol":symbol,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": Resample, 
                    "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased", 
                    "Slippage": defs.SLIPPAGE, "LotSize":lotsize, "Rolling": rolling, "Reenter": reenter, "SLTGContinuous": SLTGContinuous, "TrailSL": TrailSL,
                    'MaxReEnterCounter':MaxReEnterCount}
    return ( ticonfig, generalconfig, positionconfig)

def GetSTconfig(config):
    action = config["action"]
    Delta = config["Delta"]
    symbol = config["symbol"]
    period = config["period"]
    multiplier = config["multiplier"]
    Resample = config["Resample"]
    rolling = config["rolling"]
    reenter = config["reenter"]
    SL = config["SL"]
    SLPc = config["SLPc"]
    Target = config["Target"]
    TargetPc = config["TargetPc"]
    SLTGContinuous = config["SLTGContinuous"]
    TrailSL = config["TrailSL"]
    MaxReEnterCount = config['MaxReEnterCounter']
    return GetSTconfigsPB(action, Delta, symbol, period, multiplier, Resample, rolling, reenter, SL, SLPc, Target, TargetPc, SLTGContinuous, TrailSL, MaxReEnterCount)