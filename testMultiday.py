import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import positionconfigs as posconfigs
import generalconfigs as genconfigs

import warnings
warnings.filterwarnings("ignore")

user = "RI"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/"

PUTSPREADND = 1
ICND = 2
ICPos = 3

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
delta = datetime.timedelta(days=1)

StratType = ICPos
Symbol = defs.N
approach = "PosFN"
if (StratType == PUTSPREADND):
  # Next Day Put Spread
  if (Symbol == defs.N):
    generalconfig = genconfigs.generalconfigNextDayNMW
    positionconfig = posconfigs.positionconfigPutSpreadN
  else:
    generalconfig = genconfigs.generalconfigNextDayBNMW
    positionconfig = posconfigs.positionconfigPutSpreadBN
elif (StratType == ICND):
  # Next Day Iron Condor
  if (Symbol == defs.N):
    generalconfig = genconfigs.generalconfigNextDayNMW
    positionconfig = posconfigs.getIronCondor(200, 1000, defs.NO, defs.NO, defs.NO, 35, 200, 50)
  else:
    generalconfig = genconfigs.generalconfigNextDayBNMW
    positionconfig = posconfigs.getIronCondor(500, 2000, defs.NO, defs.NO, defs.NO, 35, 120, 50)
elif (StratType == ICPos):
  # Positional Iron Condor
  if (Symbol == defs.N):
    generalconfig = genconfigs.GetGeneralConfigExpiry(defs.ONELEG, defs.ONELEG, defs.N, [defs.MON], [defs.THU])
    positionconfig = posconfigs.getIronCondor(200, 1000, defs.NO, defs.YES, defs.NO, 35, 80, 50)
  else:
    generalconfig = genconfigs.GetGeneralConfigExpiry(defs.ONELEG, defs.ONELEG, defs.BN, [defs.MON], [defs.THU])
    positionconfig = posconfigs.getIronCondor(500, 2000, defs.NO, defs.YES, defs.NO, 35, 150, 50)


trade = pd.DataFrame()
trades = pd.DataFrame()
positions = []

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(BNPath)
  my_fileBN = Path(NPath)
  print(date_string)
  if my_fileN.exists() and my_fileBN.exists():
    masterdfN = atom.LoadDF(NPath)
    masterdfBN = atom.LoadDF(BNPath)
    if (generalconfig["symbol"] == defs.BN):
      (trade, positions) = strategies.MultiDayStrategy(masterdfBN, positions, generalconfig, positionconfig)
    elif (generalconfig["symbol"] == defs.N):
      (trade, positions) = strategies.MultiDayStrategy(masterdfN, positions, generalconfig, positionconfig)
    elif (generalconfig["symbol"] == defs.BOTH):
      positionconfig = strategies.getStatArbDef()
      (trade1, positions) = strategies.MultiDayStrategy(masterdfBN, positions, generalconfig, positionconfig[0])
      (trade2, positions) = strategies.MultiDayStrategy(masterdfN, positions, generalconfig, positionconfig[1])
      trade.append(trade1)
      trade.append(trade2)
    if (len(trade) > 0):
        trades = trades.append(trade)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta

trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"],axis = 1)

print("\n")
print(trades)
trades.to_csv(Result_path + approach + "_trades.csv")

print("\n")
Daily_Chart = rep.GetDailyChart(trades)
print(Daily_Chart)
Daily_Chart.to_csv(Result_path + approach + "_DailyChart.csv")

print("\n")
report = rep.Report(trades, Daily_Chart)
print(report)
report.to_csv(Result_path + approach + "_Report.csv")

print("\n")
weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
print(weeklyreport)
weeklyreport.to_csv(Result_path + approach + "_WeeklyReport.csv")


print("\n")
monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
print(monthlyreport)

print("\n")
dayofweek = rep.DayOfWeek(Daily_Chart)
print(dayofweek)