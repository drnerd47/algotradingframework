import definitions as defs

# INTRADAY STRADDLE BANKNIFTY
ind_straddle_BN = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "SLEvery":5, "SLPcFar":100,
                "MaxReEnterCounterSL": 1, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":50, "TargetPc":50}

# INTRADAY STRADDLE NIFTY
ind_straddle_N = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.N, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "SLEvery":5, "SLPcFar":100,
                "MaxReEnterCounterSL": 1, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":50, "TargetPc":50}

# INTRADAY STRANGLE BANKNIFTY
ind_strangle_BN = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "SLEvery":5, "SLPcFar":100,
                "MaxReEnterCounterSL": 1, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":50, "TargetPc":50, "Delta":0}

# INTRADAY STRANGLE NIFTY
ind_strangle_N = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.N, "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "SLEvery":5, "SLPcFar":100,
                "MaxReEnterCounterSL": 1, "MaxReEnterCounterTG": 6, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.NO, "SLPc":50, "TargetPc":50, "Delta":0}

# RSI-ADX BANKNIFTY BUY SIDE
rsiadx_BNb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 20, 'TargetPc': 70 ,
                'TBull': 60, 'TBear': 40, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 14, 'symbol': defs.BN, 'action': defs.BUY,
                 "SLTGContinuous": defs.NO}

# RSI-ADX NIFTY BUY SIDE
rsiadx_Nb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 20, 'TargetPc': 70,
                'TBull': 60, 'TBear': 40, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 14, 'symbol': defs.N, 'action': defs.BUY,
                 "SLTGContinuous": defs.NO}

# RSI-ADX BANKNIFTY SELL SIDE
rsiadx_BNs = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 20, 'TargetPc': 70,
                'TBull': 60, 'TBear': 40, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 14, 'symbol': defs.BN, 'action': defs.SELL, 
                "SLTGContinuous": defs.NO}

# RSI-ADX NIFTY SELL SIDE
rsiadx_Ns = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.NO, 'SLPc': 20, 'TargetPc': 70,
                'TBull': 60, 'TBear': 40, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 14, 'symbol': defs.N, 'action': defs.SELL, 
                "SLTGContinuous": defs.NO}

# RSI-2 BANKNIFTY BUY SIDE
rsi2_BNb = {"TBull1": 40, "TBear1": 60, "window1": 14, "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO, 'Delta': 0}

# RSI-2 NIFTY BUY SIDE
rsi2_Nb = {"TBull1": 40, "TBear1": 60, "window1": 14,  "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO, 'Delta': 0}

# RSI-2 BANKNIFTY SELL SIDE
rsi2_BNs = {"TBull1": 40, "TBear1": 60, "window1": 14,  "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO, 'Delta': 0}

# RSI-2 NIFTY SELL SIDE
rsi2_Ns = {"TBull1": 40, "TBear1": 60, "window1": 14,  "TBull2": 10, "TBear2": 90, "window2":2,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO, 'Delta': 0}

# RSI-Dual BANKNIFTY BUY SIDE
rsidual_BNb = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 2, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# RSI-Dual NIFTY BUY SIDE
rsidual_Nb = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 2, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# RSI-Dual BANKNIFTY SELL SIDE
rsidual_BNs = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 2, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# RSI-Dual NIFTY SELL SIDE
rsidual_Ns = {"TBull1": 60, "TBear1": 40, "window1": 14, "window2": 2, "TBull2": 90, "TBear2": 10,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# BB1 BANKNIFTY BUY SIDE
bb1_BNb = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70, 
            'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO, 'Resample': 3}

# BB1 NIFTY BUY SIDE
bb1_Nb = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO, 'Resample': 3}

# BB1 BANKNIFTY SELL SIDE
bb1_BNs = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO, 'Resample': 3}

# BB1 NIFTY SELL SIDE
bb1_Ns = {"TBull": 0, "TBear": 1, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO, 'Resample': 3}

# BB2 BANKNIFTY BUY SIDE
bb2_BNb = {"TBull": 1, "TBear": 0, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO, 'Resample': 3}

# BB2 NIFTY BUY SIDE
bb2_Nb = {"TBull": 1, "TBear": 0, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO, 'Resample': 3}

# BB2 BANKNIFTY SELL SIDE
bb2_BNs = {"TBull": 1, "TBear": 0, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO, 'Resample': 3}

# BB2 NIFTY SELL SIDE
bb2_Ns = {"TBull": 1, "TBear": 0, "period": 20, "stddev":2, "Delta": 0, "SL": defs.YES, "Target": defs.YES, 'SLPc': 20, 'TargetPc': 70,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO, 'Resample': 3}

# EMA BANKNIFTY BUY SIDE
ema_BNb = {"TBull": 35, "TBear": -65, "period": 14, "SL": defs.NO, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# EMA NIFTY BUY SIDE
ema_Nb = {"TBull": 35, "TBear": -65, "period": 14, "SL": defs.NO, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO}

# EMA BANKNIFTY SELL SIDE
ema_BNs = {"TBull": 35, "TBear": -65, "period": 14, "SL": defs.NO, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# EMA NIFTY SELL SIDE
ema_Ns = {"TBull": 35, "TBear": -65, "period": 14, "SL": defs.NO, "Delta": 0, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70, 'Resample': 3,
            'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO}
