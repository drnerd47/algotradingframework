import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import generalconfigs as genconfigs
import positionconfigs as posconfings
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

year = 2020

start_date = datetime.date(year, 1, 1)
end_date = datetime.date(year, 12, 31)
delta = datetime.timedelta(days=1)
EnterTimes = [datetime.time(9, 20), datetime.time(10, 30), datetime.time(11, 15), datetime.time(13, 15), datetime.time(14, 15)]
#EnterTimes = [datetime.time(9, 30), datetime.time(10, 30), datetime.time(11, 15), datetime.time(12, 15)]#, datetime.time(12, 15)]
#generalconfig = genconfigs.GetGeneralConfigIntraday(defs.ONELEG, defs.ONELEG, defs.BN, defs.NO, defs.NO, 1, 6, defs.NO, 5)
generalconfig = genconfigs.GetGeneralConfigIntradayTime(EnterTimes, datetime.time(15, 20), defs.ONELEG, defs.ONELEG, defs.BN, 60, defs.YES)
#generalconfig = genconfigs.generalconfigIntradayREBN
#positionconfig = posconfings.getIronButterfly(1500, 0, 1, 0, 30, 35, 70)
#ositionconfig = posconfings.getIronCondor(400, 500, 0, 0, 1, 20, 35, 30)
SLArrN = [60,60,30,100,20]
SLArrBN = [90,100,90,90,60]
#SLArrBN2 = [15,15,15,15]
if (generalconfig["symbol"] == defs.BN):
  SLArr = SLArrBN
  Delta = 500
else:
  SLArr = SLArrN
  Delta = 200
positionconfigsOther = []
for SL in SLArr:
  positionconfig = posconfings.getStrangles(defs.SELL, Delta, defs.YES, defs.NO, SL, 50)
  positionconfigsOther.append(positionconfig)
positionconfigsThu = []
for SL in SLArr:
  positionconfig = posconfings.getStraddles(defs.SELL, defs.YES, defs.NO, SL, 50)
  positionconfigsThu.append(positionconfig)

#positionconfig = posconfings.positionconfigShortStraddle
#generalconfig = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
#                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
#                     "ReEntrySL": 5, "ReEntryTG": defs.NO, "MaxReEnterCounterSL": 5, "MaxReEnterCounterTG": 5, "SLToCost": defs.YES, "REEvery": 1,
#                    "debug": defs.DEBUGTIME, "Timerenter": defs.NO, "ReEnterEvery": 5, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE, "TrailSL": defs.NO}

#positionconfig = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "SLPc":15, "SLPcFar":100, "TargetPc":50, "NumLots":1,
#                       "SL": defs.YES, "Target":defs.NO, "Id": 1, "HedgeId": 0},
#                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"SLPc":15, "SLPcFar":100, "TargetPc":50,"NumLots":1,
#                       "SL": defs.YES,"Target":defs.NO, "Id": 2, "HedgeId": 0}]

trade = pd.DataFrame()
trades = pd.DataFrame()

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(NPath)
  my_fileBN = Path(BNPath)
  print(date_string)
  if start_date.weekday() == defs.THU:
    positionconfigs = positionconfigsThu
  else:
    positionconfigs = positionconfigsOther
  if my_fileN.exists() and my_fileBN.exists():
    masterdfN = atom.LoadDF(NPath)
    masterdfBN = atom.LoadDF(BNPath)
    if (generalconfig["symbol"] == defs.BN):
      (trade, PNLTracker, PNLTrackerSumm) = strategies.IntradayTimeReEntry(masterdfBN, generalconfig, positionconfigs)
    elif (generalconfig["symbol"] == defs.N):
      (trade, PNLTracker, PNLTrackerSumm) = strategies.IntradayTimeReEntry(masterdfN, generalconfig, positionconfigs)
    if (len(trade) > 0):
      trades = trades.append(trade)
    print("MinPNL = " + str(PNLTrackerSumm["MinPNL"]) + ", MaxPNL = " + str(
      PNLTrackerSumm["MaxPNL"]) + ", FinalPNL = " + str(PNLTrackerSumm["FinalPNL"]))
  start_date += delta

trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"],axis = 1)

print("\n")
print(trades)
trades.to_csv(Result_path + "trades.csv")

print("\n")
Daily_Chart = rep.GetDailyChart(trades)
print(Daily_Chart)
Daily_Chart.to_csv(Result_path + "DailyChart.csv")

print("\n")
report = rep.Report(trades, Daily_Chart)
print(report)
report.to_csv(Result_path + "Report.csv")

print("\n")
weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
print(weeklyreport)
weeklyreport.to_csv(Result_path + "WeeklyReport.csv")

print("\n")
monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
print(monthlyreport)

print("\n")
dayofweek = rep.DayOfWeek(Daily_Chart)
print(dayofweek)