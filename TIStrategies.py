import definitions as defs
import datetime
import operator

def GetRSI2ConfigsPBSell(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2):
    positionconfig = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": defs.BEAR, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": defs.BULL, "SLPc": SLPc, "TargetPc": TargetPc}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    generalconfig = {"symbol": defs.BN, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                           "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased",
                           "TargetCond": "PremiumBased",
                           "Slippage": 0.5, "LotSize": defs.BNLOTSIZE}
    ticonfig = [
        {"TI": "RSI", "columnname": "RSI14", "ThreshBull": TBull1, "ThreshBear": TBear1, "Window": 14, "SL": defs.NO,
         "Target": defs.NO,
         "BullOperator": operator.lt, "BearOperator": operator.gt},
        {"TI": "RSI", "columnname": "RSI2", "Window": 2, "ThreshBull": TBull2, "ThreshBear": TBear2, "SL": defs.NO,
         "Target": defs.NO,
         "BullOperator": operator.lt, "BearOperator": operator.gt}]
    return (ticonfig, generalconfig, positionconfig)

positionconfigsinglebuydirec = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "NumLots":1,
                        "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40},
                        {"Type":defs.PUT,"Action":defs.BUY,"Delta":0, "NumLots":1,
                        "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40}]
generalconfigBNBB = {"name":"BNBB","symbol":defs.BN,"EnterTime": datetime.time(9,15), "ExitTime": datetime.time(15,15), "Resample": '3T', 
                    "StopLoss": True, "Target": True, "StopLossCond": "TIBased", "TargetCond": "TIBased", 
                    "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE}

def GetBBConfigsBBuy( period, Resample, TBull, TBear, SLBullDelta, SLBearDelta, TargetBullDelta, TargetBearDelta, Delta):
    positionconfig = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40},
                       {"Type":defs.PUT,"Action":defs.BUY,"Delta":Delta, "NumLots":1,
                       "SL": defs.NO, "Target": defs.NO, "Stance": defs.BEAR, "SLPc": 40}]
    SLBool = True
    TBool = True

    generalconfig = {"symbol": defs.BN, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                           "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "TIBased",
                           "TargetCond": "TIBased",
                           "Slippage": 0.5, "LotSize": defs.BNLOTSIZE}
    ticonfig = [
        {"TI": "BB", "columnname":"bbsignal", "ThreshBull": TBull, "ThreshBear": TBear, "period": period,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": TBull, "SLBear": SLBear, "TargetBull": TargetBull, "TargetBear": TargetBear, "BullOperator": operator.gt, "BearOperator": operator.lt,
               "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "TBullOperator": operator.gt, "TBearOperator": operator.lt}
            ]
    return (ticonfig, generalconfig, positionconfig)

