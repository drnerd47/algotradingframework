import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import generalconfigs as genconfigs
import positionconfigs as st

import warnings
warnings.filterwarnings("ignore")

user = "RI"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/"

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
delta = datetime.timedelta(days=1)


trade = pd.DataFrame()
trades = []
generalconfigBN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                     "ReEntrySL": 5, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5, "SLToCost": defs.YES, "REEvery": 1,
                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "TrailSL": defs.NO}
generalconfigN = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.N,
                     "ReEntrySL": defs.NO, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5, "SLToCost": defs.YES, "REEvery": 1,
                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.NLOTSIZE, "TrailSL": defs.NO}

positionconfigShortStraddle = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "SLPc":15, "SLPcFar":100, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"SLPc":15, "SLPcFar":100, "TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0}]

# Long Straddle
positionconfigLongStraddle = [{"Type":defs.CALL,"Action":defs.BUY,"Delta":0, "SLPc":25, "SLPcFar":100, "TargetPc":50, "NumLots":1,
                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
                      {"Type":defs.PUT,"Action":defs.BUY,"Delta":0,"SLPc":25, "SLPcFar":100, "TargetPc":50,"NumLots":1,
                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0}]

positionconfig = [positionconfigShortStraddle, positionconfigLongStraddle]
#positionconfig = positionconfigShortStraddle
trades = pd.DataFrame()

while start_date <= end_date:
  trade = pd.DataFrame()
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(NPath)
  my_fileBN = Path(BNPath)
  print(date_string)
  if my_fileN.exists() and my_fileBN.exists():
    masterdfN = atom.LoadDF(NPath)
    masterdfBN = atom.LoadDF(BNPath)
    generalconfigBN["symbol"] = defs.BN
    trade1 = strategies.IntraDayStrategy(masterdfBN, generalconfigBN, positionconfig[0])
    generalconfigN["symbol"] = defs.N
    trade2 = strategies.IntraDayStrategy(masterdfN, generalconfigN, positionconfig[1])
    trade = trade.append(trade1)
    trade = trade.append(trade2)
    if (len(trade) > 0):
        trades = trades.append(trade)
    else:
        print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta

trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"],axis = 1)

print(trades)
trades.to_csv("Results/trades.csv")

Daily_Chart = rep.GetDailyChart(trades)
print(Daily_Chart)
Daily_Chart.to_csv("Results/DailyChart.csv")

report = rep.Report(trades, Daily_Chart)
print(report)
report.to_csv("Results/report.csv")

weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
print(weeklyreport)

monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
print(monthlyreport)

dayofweek = rep.DayOfWeek(Daily_Chart)
print(dayofweek)


