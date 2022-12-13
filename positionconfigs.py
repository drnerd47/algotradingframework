import definitions as defs
# Short Straddle
positionconfigShortStraddle = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "SLPc":25, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"SLPc":25,"TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO}]

# Long Straddle
positionconfigLongStraddle = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "SLPc":25, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":0,"SLPc":25,"TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO}]

def getStraddles(action, SL, Target, SLPc, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":action, "Delta":0, "SLPc":SLPc, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SL, "Target":Target},
                      {"Type":defs.PUT,"Action":action,"Delta":0,"SLPc":SLPc,"TargetPc":TargetPc,"NumLots":1,
                       "SL": SL,"Target":Target}]
    return positionconfig

# Short Strangle
positionconfigShortStrangle = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":200, "SLPc":25, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":-200,"SLPc":25,"TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO}]

# Long Strangle
positionconfigLongStrangle = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":200, "SLPc":25, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-200,"SLPc":25,"TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO}]

def getStrangles(action, Delta, SL, Target, SLPc, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":action, "Delta":Delta, "SLPc":SLPc, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SL, "Target":Target},
                      {"Type":defs.PUT,"Action":action,"Delta":-1*Delta,"SLPc":SLPc,"TargetPc":TargetPc,"NumLots":1,
                       "SL": SL,"Target":Target}]
    return positionconfig

# Iron Butterfly
positionconfigIronButterfly = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":1000, "SLPc":25, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-1000,"SLPc":25,"TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO}]

def getIronButterfly(Delta, SLBuy, SLSell, Target, SLPcBuy, SLPcSell, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":Delta, "SLPc":SLPcBuy, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SLBuy, "Target":Target},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-1*Delta,"SLPc":SLPcBuy,"TargetPc":TargetPc,"NumLots":1,
                       "SL": SLBuy,"Target":Target},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": 0, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 0, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target}]
    
    return positionconfig

# Iron Condor
positionconfigIronCondor = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":200, "SLPc":25, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-200,"SLPc":25,"TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": -100, "SLPc": 25, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 100, "SLPc": 25, "TargetPc": 50,
                       "NumLots": 1, "SL": defs.YES, "Target": defs.NO}]

def getIronCondor(Delta1, Delta2, SLBuy, SLSell, Target, SLPcBuy, SLPcSell, TargetPc):
    positionconfig = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":Delta1 + Delta2, "SLPc":SLPcBuy, "TargetPc":TargetPc, "NumLots":1,
                       "SL": SLBuy, "Target":Target},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":-1*(Delta1 + Delta2),"SLPc":SLPcBuy,"TargetPc":TargetPc,"NumLots":1,
                       "SL": SLBuy,"Target":Target},
                      {"Type": defs.CALL, "Action": defs.SELL, "Delta": Delta1, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": -1*Delta1, "SLPc": SLPcSell, "TargetPc": TargetPc,
                       "NumLots": 1, "SL": SLSell, "Target": Target}]
    return positionconfig

positionconfitStatArbStraddle = [positionconfigShortStraddle, positionconfigLongStraddle]
positionconfitStatArbStrangle = [positionconfigShortStrangle, positionconfigLongStrangle]

def getStatArb(Delta1, Delta2, SL1, Target1, SLPc1, TargetPc1, SL2, Target2, SLPc2, TargetPc2):
    positionconfigShort = getStrangles(defs.SELL, Delta1, SL1, Target1, SLPc1, TargetPc1)
    positionconfigLong = getStrangles(defs.BUY, Delta2, SL2, Target2, SLPc2, TargetPc2)
    return [positionconfigShort, positionconfigLong]

def getStatArbDef():
    return [positionconfigShortStraddle, positionconfigLongStraddle]

# Position Configs for Directional Strategies

positionconfig21selldirec = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BULL}, 
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BULL},
                    {"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR},
                      {"Type":defs.CALL,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BEAR}, 
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"NumLots":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BEAR}]

positionconfigsingleselldire = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40}]

positionconfigsingleselldirecSL = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BEAR, "SLPc": 25, "TargetPc": 70},
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "NumLots":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BULL, "SLPc": 25, "TargetPc": 70}]

positionconfigsinglebuydirec = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "NumLots":1,
                        "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40},
                        {"Type":defs.PUT,"Action":defs.BUY,"Delta":0, "NumLots":1,
                        "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40}]

positionconfigsinglebuydirecSL = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "LotSize":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BEAR, "SLPc": 25, "TargetPc": 70},
                       {"Type":defs.PUT,"Action":defs.BUY,"Delta":0, "LotSize":1,
                       "SL": defs.YES, "Target":defs.YES, "Stance": defs.BULL, "SLPc": 25, "TargetPc": 70}]