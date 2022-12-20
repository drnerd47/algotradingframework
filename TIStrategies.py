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

def GetRSI2ConfigsPBSell(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2):
    positionconfig = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": defs.BULL, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":defs.BUY,"Delta":0, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": defs.BEAR, "SLPc": SLPc, "TargetPc": TargetPc}]
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
