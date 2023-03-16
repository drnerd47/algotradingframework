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

approach = "ODN"
Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 12, 31)
delta = datetime.timedelta(days=1)

generalconfig = genconfigs.generalconfigOverNightDirBNMW
#positionconfig = posconfigs.positionconfigsingleselldirec
positionconfig = posconfigs.positionconfigsingleselldirecHedged
#positionconfig = posconfigs.positionconfigsinglebuydirec
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
      (trade, positions) = strategies.OverNightDirectional(masterdfBN, positions, generalconfig, positionconfig)
    elif (generalconfig["symbol"] == defs.N):
      (trade, positions) = strategies.OverNightDirectional(masterdfN, positions, generalconfig, positionconfig)
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