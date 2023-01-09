import definitions as defs

# INTRADAY STRANGLE SEARCH BANKNIFTY
ind_strangle_BN_1 = {"SquareOffSL":defs.ONELEG, "SquareOffTG": defs.ONELEG, "symbol": defs.BN, "ReEntrySL": defs.YES, "ReEntryTG": defs.YES, "SLEvery":13, "SLPcFar":100,
            "MaxReEnterCounterSL": 2, "MaxReEnterCounterTG": 7, "SLtoCost":defs.NO, "SL":defs.YES, "Target":defs.YES, "SLPc":25, "TargetPc":70, "Delta":1100}

