import operator
import definitions as defs

TIconfigRSI_ADX = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 60, "ThreshBear": 40, "Window": 14, "SL": defs.NO, "Target": defs.NO,
            "SLBull": 40, "SLBear": 60,
           "TargetBull": 77, "TargetBear": 18, "BullOperator": operator.gt, "BearOperator": operator.lt,
                    "SLBullOperator": operator.lt, "SLBearOperator": operator.gt,"TBullOperator": operator.gt, "TBearOperator": operator.lt},
			{"TI": "ADX","columnname":"ADX14", "Window": 14, "ThreshBull": 20, "ThreshBear": 20, "SL": defs.NO, "Target": defs.NO,
           "BullOperator": operator.gt, "BearOperator": operator.gt}]

TIconfigRSI_ADX_shifted = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 60, "ThreshBear": 40, "Window": 14, "SL": defs.YES, "Target": defs.YES, "SLBull": 40, "SLBear": 60,
           "TargetBull": 77, "TargetBear": 18, "BullOperator": operator.gt, "BearOperator": operator.lt,
                    "SLBullOperator": operator.lt, "SLBearOperator": operator.gt,"TBullOperator": operator.gt, "TBearOperator": operator.lt},
                    {"TI": "RSI-Shifted", "columnname": "RSI14_shifted", "ThreshBull": 60, "ThreshBear": 40, "Window": 14, "SL": defs.NO, "Target": defs.NO, 
                    "BullOperator": operator.lt, "BearOperator": operator.gt},
			{"TI": "ADX","columnname":"ADX14", "Window": 14, "ThreshBull": 20, "ThreshBear": 20, "SL": defs.NO, "Target": defs.NO, 
           "BullOperator": operator.gt, "BearOperator": operator.gt}]

TIconfig2_RSI = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 40, "ThreshBear": 60, "Window": 14, "SL": defs.NO, "Target": defs.NO,  
            "BullOperator": operator.lt, "BearOperator": operator.gt, "SLTGContinuous": defs.YES},
			{"TI": "RSI","columnname":"RSI2", "Window": 2, "ThreshBull": 10, "ThreshBear": 90, "SL": defs.NO, "Target": defs.NO, 
            "BullOperator": operator.lt, "BearOperator": operator.gt, "SLTGContinuous": defs.YES}]

TIconfig_RSIDual = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 60, "ThreshBear": 40, "Window": 14, "SL": defs.NO, "Target": defs.NO,
            "BullOperator": operator.gt, "BearOperator": operator.lt},
			{"TI": "RSI","columnname":"RSI2", "Window": 2, "ThreshBull": 90, "ThreshBear": 20, "SL": defs.NO, "Target": defs.NO,
            "BullOperator": operator.gt, "BearOperator": operator.lt}]

TIconfigBB1 = [{"TI": "BB", "columnname":"bbsignal", "ThreshBull": 0, "ThreshBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, "BullOperator": operator.lt, "BearOperator": operator.gt,
               "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "TBullOperator": operator.gt, "TBearOperator": operator.lt}]

TIconfigBB2 = [{"TI": "BB", "columnname":"bbsignal", "ThreshBull": 1, "ThreshBear": 0, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": 0.7, "SLBear": 0.3, "TargetBull": 2, "TargetBear": -1, "BullOperator": operator.gt, "BearOperator": operator.lt,
               "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "TBullOperator": operator.gt, "TBearOperator": operator.lt}]

TIconfigST = [{"TI": "ST", "columnname":"ST", "ThreshBull": 0, "ThreshBear": 0, "period": 10,"multiplier":2, "SL": defs.NO, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt}]

TIconfigEMA = [{"TI": "MA", "columnname":"EMA", "ThreshBull": 35, "ThreshBear": -65, "period": 14, "SL": defs.NO, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt, "SLBull":-50, "SLBear": 50,
                "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "type": "EMA"}]

TIconfigSMA = [{"TI": "MA", "columnname":"SMA", "ThreshBull": 50, "ThreshBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt, "SLBull":-50, "SLBear": 50,
                "SLBullOperator": operator.lt, "SLBearOperator": operator.gt, "type": "SMA"}]