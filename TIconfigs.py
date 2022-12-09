import operator
import definitions as defs

TIconfigRSI_ADX = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 60, "ThreshBear": 40, "Window": 14, "SL": defs.YES, "Target": defs.YES, "SLBull": 40, "SLBear": 60, 
           "TargetBull": 70, "TargetBear": 18, "BullOperator": operator.gt, "BearOperator": operator.lt}, 
			{"TI": "ADX","columnname":"ADX14", "Window": 14, "ThreshBull": 20, "ThreshBear": 20, "SL": defs.NO, "Target": defs.NO, 
           "BullOperator": operator.gt, "BearOperator": operator.gt}]

TIconfig2_RSI = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 40, "ThreshBear": 60, "Window": 14, "SL": defs.NO, "Target": defs.NO,  
            "BullOperator": operator.lt, "BearOperator": operator.gt}, 
			{"TI": "RSI","columnname":"RSI2", "Window": 2, "ThreshBull": 10, "ThreshBear": 90, "SL": defs.NO, "Target": defs.NO, 
            "BullOperator": operator.gt, "BearOperator": operator.gt}]

TIconfigBB = [{"TI": "BB", "columnname":"bbsignal", "ThreshBull": 0, "ThreshBear": 0, "period": 14,"stddev":3, "SL": defs.NO, "Target": defs.NO,
                "BullOperator": operator.gt, "BearOperator": operator.lt}]