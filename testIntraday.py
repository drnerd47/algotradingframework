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

year = 2022

start_date = datetime.date(year, 1, 1)
end_date = datetime.date(year, 12, 31 )
delta = datetime.timedelta(days=1)

generalconfig = genconfigs.GetGeneralConfigIntraday(defs.ONELEG, defs.ONELEG, defs.BN, defs.NO, defs.NO, 1, 6, defs.NO)
#generalconfig = genconfigs.generalconfigIntradayREBN
#positionconfig = posconfings.getIronButterfly(1500, 0, 1, 0, 30, 35, 70)
#ositionconfig = posconfings.getIronCondor(400, 500, 0, 0, 1, 20, 35, 30)
positionconfig = posconfings.getStraddles(defs.SELL, defs.YES, defs.NO, 50, 50)
#positionconfig = posconfings.positionconfigShortStraddle
trade = pd.DataFrame()
trades = pd.DataFrame()

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(NPath)
  my_fileBN = Path(BNPath)
  print(date_string)
  if my_fileN.exists() and my_fileBN.exists():
    masterdfN = atom.LoadDF(NPath)
    masterdfBN = atom.LoadDF(BNPath)
    if (generalconfig["symbol"] == defs.BN):
      trade = strategies.IntraDayStrategy(masterdfBN, generalconfig, positionconfig)
    elif (generalconfig["symbol"] == defs.N):
      trade = strategies.IntraDayStrategy(masterdfN, generalconfig, positionconfig)
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