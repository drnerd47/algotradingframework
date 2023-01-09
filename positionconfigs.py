import definitions as defs
# Short Straddle
positionconfigShortStraddle = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "SLPc":25, "SLPcFar":100, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"SLPc":25, "SLPcFar":100, "TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0}]

# Long Straddle
positionconfigLongStraddle = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "SLPc":25, "SLPcFar":100, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":0,"SLPc":25, "SLPcFar":100, "TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0}]

def getStraddles(action, SL, Target, SLPc, SLPcFar, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":action, "Delta":0, "SLPc":SLPc, "SLPcFar":SLPcFar, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SL, "Target":Target, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":action,"Delta":0,"SLPc":SLPc, "SLPcFar":SLPcFar, "TargetPc":TargetPc,"NumLots":1,
                       "SL": SL,"Target":Target, "Id": 2, "HedgeId": 0}]
    return positionconfig

# Short Strangle
positionconfigShortStrangle = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":200, "SLPc":25, "SLPcFar":100, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":-200,"SLPc":25, "SLPcFar":100, "TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0}]

# Long Strangle
positionconfigLongStrangle = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":200, "SLPc":25, "SLPcFar":100, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-200,"SLPc":25, "SLPcFar":100, "TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0}]

def getStrangles(action, Delta, SL, Target, SLPc, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":action, "Delta":Delta, "SLPc":SLPc, "SLPcFar":100, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SL, "Target":Target, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":action,"Delta":-1*Delta,"SLPc":SLPc, "SLPcFar":100, "TargetPc":TargetPc,"NumLots":1,
                       "SL": SL,"Target":Target, "Id": 2, "HedgeId": 0}]
    return positionconfig

# Iron Butterfly
positionconfigIronButterfly = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":1000, "SLPc":25, "SLPcFar":100, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-1000,"SLPc":25, "SLPcFar":100, "TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "SLPcFar":100, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO, "Id": 3, "HedgeId": 1},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "SLPcFar":100, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO, "Id": 4, "HedgeId": 2}]

def getIronButterfly(Delta, SLBuy, SLSell, Target, SLPcBuy, SLPcSell, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":Delta, "SLPc":SLPcBuy, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SLBuy, "Target":Target, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-1*Delta,"SLPc":SLPcBuy,"TargetPc":TargetPc,"NumLots":1,
                       "SL": SLBuy,"Target":Target, "Id": 2, "HedgeId": 0},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": 0, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target, "Id": 3, "HedgeId": 1},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 0, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target, "Id": 4, "HedgeId": 2}]
    
    return positionconfig

# Iron Condor
positionconfigIronCondor = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":1000, "SLPc":25, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-1000,"SLPc":25,"TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": -200, "SLPc": 25, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO, "Id": 3, "HedgeId": 1},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 200, "SLPc": 25, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO, "Id": 4, "HedgeId": 2}]

def getIronCondor(Delta1, Delta2, SLBuy, SLSell, Target, SLPcBuy, SLPcSell, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":Delta1 + Delta2, "SLPc":SLPcBuy, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SLBuy, "Target":Target, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-1*(Delta1 + Delta2),"SLPc":SLPcBuy,"TargetPc":TargetPc,"NumLots":1,
                       "SL": SLBuy,"Target":Target, "Id": 2, "HedgeId": 0},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": Delta1, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target, "Id": 3, "HedgeId": 1},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": -1*Delta1, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target, "Id": 4, "HedgeId": 2}]
    return positionconfig

positionconfigStatArbStraddle = [positionconfigShortStraddle, positionconfigLongStraddle]

positionconfigStatArbStrangle = [positionconfigShortStrangle, positionconfigLongStrangle]

def getStatArb(Delta1, Delta2, SL1, Target1, SLPc1, TargetPc1, SL2, Target2, SLPc2, TargetPc2):
    positionconfigShort = getStrangles(defs.SELL, Delta1, SL1, Target1, SLPc1, TargetPc1)
    positionconfigLong = getStrangles(defs.BUY, Delta2, SL2, Target2, SLPc2, TargetPc2)
    return [positionconfigShort, positionconfigLong]

def getStatArbDef():
    return [positionconfigShortStraddle, positionconfigLongStraddle]

# Position Configs for Directional Strategies

positionconfig21selldirec = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BULL, "Id": 2, "HedgeId": 0},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BULL, "Id": 3, "HedgeId": 0},
                    {"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "Id": 4, "HedgeId": 0},
                      {"Type":defs.CALL,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BEAR, "Id": 5, "HedgeId": 0},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BEAR, "Id": 6, "HedgeId": 0}]

positionconfigsingleselldirec = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40, "Id": 1, "HedgeId": 0},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40, "Id": 2, "HedgeId": 0}]

positionconfigsingleselldirecHedged = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40, "Id": 1, "HedgeId": 3},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40, "Id": 2, "HedgeId": 4},
                        {"Type": defs.CALL, "Action": defs.BUY, "Delta": 1000, "NumLots": 1,
                        "SL": defs.NO, "Target": defs.NO, "Stance": defs.BEAR, "SLPc": 40, "Id": 3, "HedgeId": 0},
                        {"Type": defs.PUT, "Action": defs.BUY, "Delta": -1000, "NumLots": 1,
                        "SL": defs.NO, "Target": defs.NO, "Stance": defs.BULL, "SLPc": 40, "Id": 4, "HedgeId": 0}]

positionconfigsingleselldirecSL = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BEAR, "SLPc": 20, "TargetPc": 70},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BULL, "SLPc": 20, "TargetPc": 70}]

positionconfigsingleselldirecSL1 = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BEAR, "SLPc": 5, "TargetPc": 90},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BULL, "SLPc": 5, "TargetPc": 90}]

positionconfigsinglebuydirec = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "NumLots":1,
                        "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40},
                        {"Type":defs.PUT,"Action":defs.BUY,"Delta":0, "NumLots":1,
                        "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40}]

positionconfigsinglebuydirecSL = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BULL, "SLPc": 20, "TargetPc": 70},
                       {"Type":defs.PUT,"Action":defs.BUY,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BEAR, "SLPc": 20, "TargetPc": 70}]