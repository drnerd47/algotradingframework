import definitions as defs
import datetime

# INTRADAY STRADDLE OL BANKNIFTY
ind_straddle_BN_OL_RE = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "REEvery":10, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 6, "SLtoCost":defs.YES, "SL":defs.YES, "Target":defs.NO, "SLPc":25, "TargetPc":50, "Delta":1000, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 17), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE OL NIFTY
ind_straddle_N_OL_RE = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.N, "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "REEvery":10, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 6, "SLtoCost":defs.YES, "SL":defs.YES, "Target":defs.NO, "SLPc":25, "TargetPc":50, "Delta":300, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 17), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE OL BANKNIFTY
ind_straddle_BN_OL = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "REEvery":14, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":90, "TargetPc":50, "Delta":500, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE OL NIFTY
ind_straddle_N_OL = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.N, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "REEvery":14, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 3, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":60, "TargetPc":50, "Delta":200, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 20), "ExitTime": datetime.time(15, 20)}

# INTRADAY STRADDLE OL BANKNIFTY
ind_straddle_BN_OLS = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "REEvery":14, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 3, "MaxReEnterCounterTG": 6, "SLtoCost":defs.YES, "SL":defs.YES, "Target":defs.NO, "SLPc":15, "TargetPc":75, "Delta":500, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE OL NIFTY
ind_straddle_N_OLS = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.N, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "REEvery":14, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 6, "SLtoCost":defs.YES, "SL":defs.YES, "Target":defs.NO, "SLPc":15, "TargetPc":50, "Delta":200, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE OL NIFTY
ind_straddle_FN_OLS = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.FN, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "REEvery":14, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 6, "SLtoCost":defs.YES, "SL":defs.YES, "Target":defs.NO, "SLPc":15, "TargetPc":50, "Delta":200, "DeltaTue":0, "OnlyTue": False,
                         "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE AL BANKNIFTY
ind_straddle_BN_AL = {"SquareOffSL":defs.ALLLEGS, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "REEvery":1, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":45, "TargetPc":50, "Delta":1000, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 16), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE AL NIFTY
ind_straddle_N_AL = {"SquareOffSL":defs.ALLLEGS, "SquareOffTG": defs.ONELEG, "symbol": defs.N, "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "REEvery":1, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc": 55, "TargetPc":50, "Delta":300, "DeltaThu":0, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 16), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE OL Reentry on Closing Both Legs BANKNIFTY
ind_straddle_BN_ALS = {"SquareOffSL":defs.ONELEGSL, "SquareOffTG": defs.ONELEGSL, "symbol": defs.BN, "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "REEvery":1, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 4, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":25, "TargetPc":50, "Delta":500, "DeltaThu":500, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 30), "ExitTime": datetime.time(15, 15)}

# INTRADAY STRADDLE OL Reentry on Closing Both Legs NIFTY
ind_straddle_N_ALS = {"SquareOffSL":defs.ONELEGSL, "SquareOffTG": defs.ONELEGSL, "symbol": defs.N, "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "REEvery":1, "TrailSL": defs.NO,
                "MaxReEnterCounterSL": 4, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":35, "TargetPc":50, "Delta":100, "DeltaThu":100, "OnlyThu": False,
                         "EnterTime": datetime.time(9, 16), "ExitTime": datetime.time(15, 15)}

# RSI-ADX BANKNIFTY BUY SIDE
rsiadx_BNb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 20, 'TargetPc': 70 ,
                'TBull': 60, 'TBear': 40, 'reenter': defs.NO, 'rolling': defs.NO, 'window': 14, 'symbol': defs.BN, 'action': defs.BUY,
                 "SLTGContinuous": defs.YES, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-ADX NIFTY BUY SIDE
rsiadx_Nb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 9, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 35, 'TargetPc': 70,
                'TBull': 60, 'TBear': 40, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 18, 'symbol': defs.N, 'action': defs.BUY,
                 "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-ADX BANKNIFTY SELL SIDE
rsiadx_BNs = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 2, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 20, 'TargetPc': 70,
                'TBull': 60, 'TBear': 40, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 10, 'symbol': defs.BN, 'action': defs.SELL,
                "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-ADX NIFTY SELL SIDE
rsiadx_Ns = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 4, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 15, 'TargetPc': 70,
                'TBull': 60, 'TBear': 40, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 16, 'symbol': defs.N, 'action': defs.SELL,
                "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-2 BANKNIFTY BUY SIDE
rsi2_BNb = {"TBull1": 40, "TBear1": 60, "window1": 14, "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.YES, 'Delta': 0, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
             "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-2 NIFTY BUY SIDE
rsi2_Nb = {"TBull1": 40, "TBear1": 60, "window1": 14,  "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.YES, 'Delta': 0, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
             "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-2 BANKNIFTY SELL SIDE
rsi2_BNs = {"TBull1": 40, "TBear1": 60, "window1": 14,  "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.YES, 'Delta': 0, "TrailSL": defs.NO, 'MaxBullReEnterCounter':5, 'MaxBearReEnterCounter':5,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-2 NIFTY SELL SIDE
rsi2_Ns = {"TBull1": 40, "TBear1": 60, "window1": 14,  "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.YES, 'Delta': 0, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-2 FINNIFTY SELL SIDE
rsi2_FNs = {"TBull1": 40, "TBear1": 60, "window1": 14,  "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.FN, 'action': defs.SELL,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.YES, 'Delta': 0, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-Dual BANKNIFTY BUY SIDE
rsidual_BNb = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 2, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-Dual NIFTY BUY SIDE
#rsidual_Nb = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 2, "TBull2": 90, "TBear2": 10,
#            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY,
#            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.YES, "TrailSL": defs.NO}
rsidual_Nb = {"TBull1": 60, "TBear1": 40, "window1": 12, "window2": 6, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 25, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY,
            'rolling': defs.NO, 'Resample': 9, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
             "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15) }

# RSI-Dual BANKNIFTY SELL SIDE
rsidual_BNs = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 2, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL,
            'rolling': defs.NO, 'Resample': 19, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# RSI-Dual NIFTY SELL SIDE
rsidual_Ns = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 5, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL,
            'rolling': defs.NO, 'Resample': 3, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB1 BANKNIFTY BUY SIDE
bb1_BNb = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.YES, 'Resample': 3, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB1 NIFTY BUY SIDE
bb1_Nb = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.YES, 'Resample': 3, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB1 BANKNIFTY SELL SIDE
bb1_BNs = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.YES, 'Resample': 7, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB1 NIFTY SELL SIDE
bb1_Ns = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.YES, 'Resample': 3, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB2 BANKNIFTY BUY SIDE
bb2_BNb = {"TBull": 1, "TBear": 0, "period": 20, "stddev":1, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.YES, 'Resample': 3, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB2 NIFTY BUY SIDE
bb2_Nb = {"TBull": 1, "TBear": 0, "period": 20, "stddev":1, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.YES, 'Resample': 3, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB2 BANKNIFTY SELL SIDE
bb2_BNs = {"TBull": 1, "TBear": 0, "period": 20, "stddev":1, "Delta": 0, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.YES, 'Resample': 3, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# BB2 NIFTY SELL SIDE
bb2_Ns = {"TBull": 1, "TBear": 0, "period": 20, "stddev":1, "Delta": 0, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.YES, 'Resample': 3, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# EMA BANKNIFTY BUY SIDE
ema_BNb = {"TBull": 35, "TBear": -65, "period": 14, "SL": defs.YES, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# EMA NIFTY BUY SIDE
ema_Nb = {"TBull": 20, "TBear": -30, "period": 14, "SL": defs.YES, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'TrailSLPc': 10, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# EMA BANKNIFTY SELL SIDE
ema_BNs = {"TBull": 35, "TBear": -65, "period": 14, "SL": defs.YES, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# EMA NIFTY SELL SIDE
ema_Ns = {"TBull": 20, "TBear": -20, "period": 14, "SL": defs.YES, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

# EMA NIFTY SELL SIDE
ema_FNs = {"TBull": 20, "TBear": -20, "period": 14, "SL": defs.YES, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.FN, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
            "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

st_BNs = {"action": defs.SELL, "Delta": 0, "symbol": defs.BN, "period": 10, "multiplier": 2, "Resample": 3, "rolling": defs.NO, "reenter": defs.YES,
          "SL": defs.YES, "SLPc": 20, "Target": defs.YES, "TargetPc": 70, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
          "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

st_Ns = {"action": defs.SELL, "Delta": 0, "symbol": defs.N, "period": 10, "multiplier": 2, "Resample": 3, "rolling": defs.NO, "reenter": defs.YES,
          "SL": defs.YES, "SLPc": 20, "Target": defs.YES, "TargetPc": 70, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
          "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

st_BNb = {"action": defs.BUY, "Delta": 0, "symbol": defs.BN, "period": 10, "multiplier": 2, "Resample": 3, "rolling": defs.NO, "reenter": defs.YES,
          "SL": defs.YES, "SLPc": 20, "Target": defs.NO, "TargetPc": 70, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
          "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}

st_Nb = {"action": defs.BUY, "Delta": 0, "symbol": defs.N, "period": 10, "multiplier": 2, "Resample": 3, "rolling": defs.NO, "reenter": defs.YES,
          "SL": defs.YES, "SLPc": 20, "Target": defs.NO, "TargetPc": 70, "SLTGContinuous": defs.YES, "TrailSL": defs.NO, 'MaxBullReEnterCounter':4, 'MaxBearReEnterCounter':4,
          "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15)}
