import definitions as defs

# RSI-ADX BANKNIFTY BUY SIDE
rsiadx_BNb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 90, 'reenter': 1, 'rolling': defs.NO, 'window': 14, 'symbol': defs.BN, 'action': defs.BUY, "SLTGContinuous": defs.NO}

# RSI-ADX NIFTY BUY SIDE
rsiadx_Nb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 70, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 14, 'symbol': defs.N, 'action': defs.BUY, "SLTGContinuous": defs.NO}

# RSI-ADX BANKNIFTY SELL SIDE
rsiadx_BNs = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 90, 'reenter': 1, 'rolling': defs.NO, 'window': 14, 'symbol': defs.BN, 'action': defs.SELL, "SLTGContinuous": defs.NO}

# RSI-ADX NIFTY SELL SIDE
rsiadx_Ns = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 70, 'reenter': defs.YES, 'rolling': defs.NO, 'window': 14, 'symbol': defs.N, 'action': defs.SELL, "SLTGContinuous": defs.NO}

# RSI-2 BANKNIFTY BUY SIDE
rsi2_BNb = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO}

# RSI-2 NIFTY BUY SIDE
rsi2_Nb = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO}

# RSI-2 BANKNIFTY SELL SIDE
rsi2_BNs = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO}

# RSI-2 NIFTY SELL SIDE
rsi2_Ns = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL,
            'rolling': defs.YES, 'Resample': 10, 'reenter': defs.YES, "SLTGContinuous": defs.NO}

# RSI-Dual BANKNIFTY BUY SIDE
rsidual_BNb = {"TBull1": 60, "TBear1": 40, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 90, "TBear2": 20,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# RSI-Dual NIFTY BUY SIDE
rsidual_Nb = {"TBull1": 60, "TBear1": 40, "Window1": 14, "Window2": 2, "TBull2": 90, "TBear2": 20,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# RSI-Dual BANKNIFTY SELL SIDE
rsidual_BNs = {"TBull1": 60, "TBear1": 40, "Window1": 14, "Window2": 2, "TBull2": 90, "TBear2": 20,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# RSI-Dual NIFTY SELL SIDE
rsidual_Ns = {"TBull1": 60, "TBear1": 40, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 90, "TBear2": 20,
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL,
            'rolling': defs.NO, 'Resample': 10, 'reenter': defs.YES, "Delta": 0, "SLTGContinuous": defs.NO}

# BB1 BANKNIFTY BUY SIDE
bb1_BNb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# BB1 NIFTY BUY SIDE
bb1_Nb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO}

# BB1 BANKNIFTY SELL SIDE
bb1_BNs = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# BB1 NIFTY SELL SIDE
bb1_Ns = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO}

# BB2 BANKNIFTY BUY SIDE
bb2_BNb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# BB2 NIFTY BUY SIDE
bb2_Nb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO}

# BB2 BANKNIFTY SELL SIDE
bb2_BNS = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# BB2 NIFTY SELL SIDE
bb2_NS = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'rolling': defs.YES, 'reenter': defs.YES, 'symbol': defs.N, "SLTGContinuous": defs.NO}

# EMA BANKNIFTY BUY SIDE
ema_BNb = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.NO, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# EMA NIFTY BUY SIDE
ema_Nb = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.BUY, 'rolling': defs.NO, 'reenter': defs.NO, 'symbol': defs.N, "SLTGContinuous": defs.NO}

# EMA BANKNIFTY SELL SIDE
ema_BNs = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.NO, 'symbol': defs.BN, "SLTGContinuous": defs.NO}

# EMA NIFTY SELL SIDE
ema_Ns = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.SELL, 'rolling': defs.NO, 'reenter': defs.NO, 'symbol': defs.N, "SLTGContinuous": defs.NO}
