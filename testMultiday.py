import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies

import warnings
warnings.filterwarnings("ignore")

Banknifty_Path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = 'NIFTYOptionsData/OptionsData/Nifty/'

start_date = datetime.date(2022, 1, 3)
end_date = datetime.date(2022, 1, 17)
delta = datetime.timedelta(days=1)

trade = pd.DataFrame()
trades = []

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  currpath = Banknifty_Path + date_string
  print(currpath)
  
  generalconfig = {"SL": defs.YES, "Target": defs.NO, "SquareOffSL":defs.ALLLEGS,"SquareOffTG":defs.EXITLEG,
                     "EnterDay":defs.MON,"EnterTime":datetime.time(9,30),"ExitDay":defs.THU,
                     "ExitTime":datetime.time(15,15), "symbol":"BANKNIFTY", "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "debug": defs.DEBUGTIME}
  positionconfig = [{"Type": defs.CALL, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "TargetPc": 50, "LotSize": 1,
                       "SL": defs.YES, "Target": defs.YES},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "TargetPc": 50, "LotSize": 1,
                       "SL": defs.YES, "Target": defs.YES}]
  my_file = Path(currpath)
  if my_file.exists():
  
    masterdf = atom.LoadDF(currpath)
    trade = strategies.MultidayStrategy(masterdf, generalconfig, positionconfig)
    trades.append(trade)
    print(trade)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta

trades = pd.concat(trades)
print(trades)

