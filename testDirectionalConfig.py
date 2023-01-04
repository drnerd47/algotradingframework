import definitions as defs

# RSI-ADX BANKNIFTY BUY SIDE
rsiadx_BNb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 90, 'reenter': 1, 'rolling': 1, 'window': 14, 'symbol': defs.BN, 'action': defs.BUY}

# RSI-ADX NIFTY BUY SIDE
rsiadx_Nb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 70, 'reenter': defs.YES, 'rolling': defs.YES, 'window': 14, 'symbol': defs.N, 'action': defs.BUY}

# RSI-ADX BANKNIFTY SELL SIDE
rsiadx_BNb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 90, 'reenter': 1, 'rolling': 1, 'window': 14, 'symbol': defs.BN, 'action': defs.SELL}

# RSI-ADX NIFTY SELL SIDE
rsiadx_Nb = {'ADXTBear': 20, 'ADXTBull': 20, 'Delta': 0, 'Resample': 3, 'SL': defs.YES, 'Target': defs.YES, 'SLPc': 20, 'TBear': 40,
                'TBull': 60, 'TargetPc': 70, 'reenter': defs.YES, 'rolling': defs.YES, 'window': 14, 'symbol': defs.N, 'action': defs.SELL}

# RSI-2 BANKNIFTY BUY SIDE
rsi2_BNb = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# RSI-2 NIFTY BUY SIDE
rsi2_Nb = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# RSI-2 BANKNIFTY SELL SIDE
rsi2_BNs = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# RSI-2 NIFTY SELL SIDE
rsi2_Ns = {"TBull1": 40, "TBear1": 60, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 10, "TBear2": 90, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# RSI-Dual BANKNIFTY BUY SIDE
rsidual_BNb = {"TBull1": 60, "TBear1": 40, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 90, "TBear2": 20, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.BUY, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# RSI-Dual NIFTY BUY SIDE
rsidual_Nb = {"TBull1": 60, "TBear1": 40, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 90, "TBear2": 20, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.BUY, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# RSI-Dual BANKNIFTY SELL SIDE
rsidual_BNs = {"TBull1": 60, "TBear1": 40, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 90, "TBear2": 20, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.BN, 'action': defs.SELL, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# RSI-Dual NIFTY SELL SIDE
rsidual_Ns = {"TBull1": 60, "TBear1": 40, "Window1": 14, "SL": defs.YES, "Target": defs.NO, "Window2": 2, "TBull2": 90, "TBear2": 20, 
            "SL": defs.YES, "Target": defs.NO, "SLPc": 20, "TargetPc": 70, 'symbol': defs.N, 'action': defs.SELL, 
            'Rolling': defs.YES, 'Resample': defs.YES, 'Reenter': defs.YES}

# BB1 BANKNIFTY BUY SIDE
bb1_BNb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.BN}

# BB1 NIFTY BUY SIDE
bb1_Nb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.N}

# BB1 BANKNIFTY SELL SIDE
bb1_BNs = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.BN}

# BB1 NIFTY SELL SIDE
bb1_Ns = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.N}

# BB2 BANKNIFTY BUY SIDE
bb2_BNb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.BN}

# BB2 NIFTY BUY SIDE
bb2_Nb = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.BUY, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.N}

# BB2 BANKNIFTY SELL SIDE
bb2_BNS = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.BN}

# BB2 NIFTY SELL SIDE
bb2_NS = {"TBull": 0, "TBear": 1, "period": 20,"stddev":2, "SL": defs.YES, "Target": defs.YES,
                "SLBull": -0.3, "SLBear": 1.3, "TargetBull": 0.7, "TargetBear": 0.3, 'SLPc': 20, 'TargetPc': 70,
                'action': defs.SELL, 'Rolling': defs.YES, 'Reenter': defs.YES, 'symbol': defs.N}

# EMA BANKNIFTY BUY SIDE
ema_BNb = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.BUY, 'Rolling': defs.NO, 'Reenter': defs.NO, 'symbol': defs.BN} 

# EMA NIFTY BUY SIDE
ema_Nb = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.BUY, 'Rolling': defs.NO, 'Reenter': defs.NO, 'symbol': defs.N} 

# EMA BANKNIFTY SELL SIDE
ema_BNs = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.SELL, 'Rolling': defs.NO, 'Reenter': defs.NO, 'symbol': defs.BN} 

# EMA NIFTY SELL SIDE
ema_Ns = {"TBull": 50, "TBear": -50, "period": 14, "SL": defs.YES, "Target": defs.NO, 'SLPc': 20, 'TargetPc': 70,
                "SLBull":-50, "SLBear": 50, 'action': defs.SELL, 'Rolling': defs.NO, 'Reenter': defs.NO, 'symbol': defs.N} 