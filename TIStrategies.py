import definitions as defs
import datetime
import operator

def GetRSI2Configs(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2, symbol, action, rolling, reenter):

    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":0, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": defs.BEAR, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":action,"Delta":0, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": defs.BULL, "SLPc": SLPc, "TargetPc": TargetPc}]
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
                           "TargetCond": "PremiumBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter}

    ticonfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": TBull1, "ThreshBear": TBear1, "Window": 14, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.lt, "BearOperator": operator.gt},
        {"TI": "RSI", "columnname": "RSI2", "Window": 2, "ThreshBull": TBull2, "ThreshBear": TBear2, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.lt, "BearOperator": operator.gt}]
    return (ticonfig, generalconfig, positionconfig)

def GetRSIDualConfigs(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2, symbol, action, rolling, reenter):

    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":0, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": defs.BEAR, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":action,"Delta":0, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": defs.BULL, "SLPc": SLPc, "TargetPc": TargetPc}]
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
                           "TargetCond": "PremiumBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter}

    ticonfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": TBull1, "ThreshBear": TBear1, "Window": 14, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.gt, "BearOperator": operator.lt},
        {"TI": "RSI", "columnname": "RSI2", "Window": 2, "ThreshBull": TBull2, "ThreshBear": TBear2, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.gt, "BearOperator": operator.lt}]
    return (ticonfig, generalconfig, positionconfig)


def GetBB1Configs(period, Resample, TBull, TBear, SLBullDelta, SLBearDelta, TargetBullDelta, TargetBearDelta, Delta, symbol, action, rolling, reenter):

    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40},
                       {"Type":defs.PUT,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target": defs.NO, "Stance": defs.BEAR, "SLPc": 40}]
    SLBool = True
    TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    generalconfig = {"symbol": symbol, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                           "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "TIBased",
                           "TargetCond": "TIBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter}

    ticonfig = [{"TI": "BB", "columnname":"bbsignal", "ThreshBull": TBull, "ThreshBear": TBear, "period": period,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": TBull + SLBullDelta, "SLBear": TBear + SLBearDelta, "TargetBull": TBull + TargetBullDelta, "TargetBear": TBear + TargetBearDelta,
                "BullOperator": operator.lt, "BearOperator": operator.gt, "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "TBullOperator": operator.gt, "TBearOperator": operator.lt}]
    return (ticonfig, generalconfig, positionconfig)

def GetBB2Configs(period, Resample, TBull, TBear, SLBullDelta, SLBearDelta, TargetBullDelta, TargetBearDelta, Delta, symbol, action, rolling, reenter):
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40},
                       {"Type":defs.PUT,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target": defs.NO, "Stance": defs.BEAR, "SLPc": 40}]
    SLBool = True
    TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    generalconfig = {"symbol": symbol, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                           "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "TIBased",
                           "TargetCond": "TIBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter}

    ticonfig = [{"TI": "BB", "columnname":"bbsignal", "ThreshBull": TBull, "ThreshBear": TBear, "period": period,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": TBull + SLBullDelta, "SLBear": TBear + SLBearDelta, "TargetBull": TBull + TargetBullDelta, "TargetBear": TBear + TargetBearDelta,
                "BullOperator": operator.lt, "BearOperator": operator.gt,
               "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "TBullOperator": operator.gt, "TBearOperator": operator.lt}]
    return (ticonfig, generalconfig, positionconfig)

def GetRSIADXconfigs(action, symbol, Delta, Resample, TBull, TBear, window, SLBullDelta, SLBearDelta, TargetBullDelta, TargetBearDelta, ADXTBull, ADXTBear,rolling, reenter):
    
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40, "Id": 1, "HedgeId": 0},
                       {"Type":defs.PUT,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40, "Id": 2, "HedgeId": 0}]
    SLBool = True
    TBool = False
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    generalconfig = { "symbol":symbol,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": Resample,
                    "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":lotsize, "Rolling": rolling, "Reenter": reenter}


    ticonfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": TBull, "ThreshBear": TBear, "Window": window, "SL": defs.YES, "Target": defs.YES, 
            "SLBull": TBull + SLBullDelta, "SLBear": TBear + SLBearDelta, "TargetBull": TBull + TargetBullDelta, "TargetBear": TBear + TargetBearDelta,
             "BullOperator": operator.gt, "BearOperator": operator.lt, "SLBullOperator": operator.lt, "SLBearOperator": operator.gt,"TBullOperator": operator.gt, "TBearOperator": operator.lt},
			{"TI": "ADX","columnname":"ADX14", "Window": window, "ThreshBull": ADXTBull, "ThreshBear": ADXTBear, "SL": defs.NO, "Target": defs.NO, 
           "BullOperator": operator.gt, "BearOperator": operator.gt}]

    return (ticonfig, generalconfig, positionconfig)

def GetEMAconfigs(symbol, action, Delta, TBull, TBear, period, SLBullDelta, SLBearDelta, Resample, rolling, reenter):
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40, "Id": 1, "HedgeId": 0},
                       {"Type":defs.PUT,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40, "Id": 2, "HedgeId": 0}]
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE
    generalconfig = {"symbol":symbol, "EnterTime": datetime.time(9,30) ,"ExitTime": datetime.time(15,15), "Resample": Resample, 
                    "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased",
                        "Slippage": defs.SLIPPAGE, "LotSize":lotsize, "Rolling": rolling, "Reenter": reenter}

    ticonfig = [{"TI": "MA", "columnname":"EMA", "ThreshBull": TBull, "ThreshBear": TBear, "period": period, "SL": defs.YES, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt, "SLBull":TBull + SLBullDelta , "SLBear": TBear + SLBearDelta,
                "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "type": "EMA"}]

    return (ticonfig, generalconfig, positionconfig)

def GetSTconfigs(action, Delta, symbol, period, multiplier, Resample, rolling, reenter):
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BEAR, "SLPc": 20, "TargetPc": 70},
                       {"Type":defs.PUT,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BULL, "SLPc": 20, "TargetPc": 70}]
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE

    ticonfig = [{"TI": "ST", "columnname":"ST", "ThreshBull": 0, "ThreshBear": 0, "period": period,"multiplier":multiplier, "SL": defs.NO, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt}]

    generalconfig = {"name":"BNST","symbol":symbol,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": Resample, 
                    "StopLoss": True, "Target": True, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased", 
                    "Slippage": defs.SLIPPAGE, "LotSize":lotsize, "Rolling": rolling, "Reenter": reenter}
    return ( ticonfig, generalconfig, positionconfig)


