import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import time

import warnings
warnings.filterwarnings("ignore")

Banknifty_Path = '../NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = '../NIFTYOptionsData/OptionsData/nifty/'

start_date = datetime.date(2022, 1, 3)
end_date = datetime.date(2022, 1, 10)
delta = datetime.timedelta(days=1)


trade = pd.DataFrame()
trades = []
generalconfig = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":"BANKNIFTY",
                     "ReEntrySL": defs.YES, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5,
                 "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5}
positionconfig = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "SLPc":25, "TargetPc":50, "LotSize":1,
                       "SL": defs.YES, "Target":defs.NO},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"SLPc":25,"TargetPc":50,"LotSize":1,
                       "SL": defs.YES,"Target":defs.NO}]
trade = pd.DataFrame()
trades = pd.DataFrame()

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  currpath = Banknifty_Path + date_string
  print(currpath)
  my_file = Path(currpath)

  if my_file.exists():
    masterdf = atom.LoadDF(currpath)
    tic = time.perf_counter()
    trade = strategies.IntraDayStrategy(masterdf, generalconfig, positionconfig)
    toc = time.perf_counter()
    print(f"Time taken is {toc - tic:0.4f} seconds")
    if (len(trade) > 0):
        trades = trades.append(trade)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta

trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"],axis = 1)

print(trades)
Daily_Chart = rep.GetDailyChart(trades)
print(Daily_Chart)

report = rep.Report(trades, Daily_Chart)
print(report)

weeklybreakdown = rep.WeeklyBreakDown(Daily_Chart)
print(weeklybreakdown)

monthlybreakdown = rep.MonthlyBreakDown(Daily_Chart)
print(monthlybreakdown)

dayofweek = rep.DayOfWeek(Daily_Chart)
print(dayofweek)



