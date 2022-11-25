import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies

Banknifty_Path = 'NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = 'NIFTYOptionsData/OptionsData/Nifty/'

start_date = datetime.date(2022, 1, 3)
end_date = datetime.date(2022, 2, 28)
delta = datetime.timedelta(days=1)

trades = pd.DataFrame()

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  currpath = Banknifty_Path + date_string
  print(currpath)
  my_file = Path(currpath)
  if my_file.exists():
    masterdf = atom.LoadDF(currpath)
    generalconfig = {"SL": defs.YES, "Target": defs.YES, "SquareOffSL":defs.ALLLEGS,"SquareOffTG":defs.EXITLEG,
                     "EnterDay":[defs.MON],"EnterTime":datetime.time(9,30),"ExitDay":defs.THU, "ExitTime":datetime.time(15,15),
                     "symbol":"BANKNIFTY", "ReEntrySL": defs.YES, "ReEntryTG": defs.YES}
    positionconfig = [{"Type": defs.CALL, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "TargetPc": 50, "LotSize": 1,
                       "SL": defs.YES, "Target": defs.YES},
                      {"Type": defs.PUT, "Action": defs.SELL, "Delta": 0, "SLPc": 25, "TargetPc": 50, "LotSize": 1,
                       "SL": defs.YES, "Target": defs.YES}]
    trades = strategies.MultidayStrategy(masterdf, generalconfig, positionconfig)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta



