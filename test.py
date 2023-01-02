import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import generalconfigs as genconfig
import positionconfigs as posconfig
import directional as direc
import warnings
import TIconfigs
import numpy as np


path = r"D:\Work\Sykes and Ray\NIFTYOptionsData\OptionsData\Banknifty\2022\Data20220103.csv"
masterdf = atom.LoadDF(path)
premium = 100
time = datetime.time(9, 30)
startstrike = 30000
endstrike = 40000
optype = defs.CALL
OHLC = 'open'
symbol = defs.BN

spotdata = atom.GetSpotData(masterdf,symbol)
for s in range(len(spotdata)):
    currentcandle = spotdata.iloc[s]
    # Check Enter time Condition
    if currentcandle.name.time() == time:
        (beststrikeprice, minval) = direc.FindStrike(masterdf, premium, currentcandle.name, startstrike, endstrike, optype, OHLC, symbol)
print(beststrikeprice)
print(minval)