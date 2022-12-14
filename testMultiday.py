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

user = "MS"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/"
elif user == "MS":
  Root = "C:/Users/shahm/(8)Work/SRE/"
  Result_path = "C:/Users/shahm/(8)Work/SRE/NIFTYOptionsData/OptionsData/Results/Intraday_BankNifty/Short_Straddle/One_Leg/With_Slippage"


Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 8, 31)
delta = datetime.timedelta(days=1)

generalconfig = genconfigs.generalconfigExpiryBN

positionconfigSS = posconfigs.getStraddles(defs.SELL, defs.YES, defs.NO, 25, 50)
positionconfigIB = posconfigs.getIronButterfly(1000, defs.NO, defs.NO, defs.NO, 35, 35, 50)
positionconfig = positionconfigSS
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
monthlyreport = rep.MonthlyBreakDown(Daily_Chart,filename = Result_path + "MonthlyBreakDown.txt")
print(monthlyreport)

print("\n")
dayofweek = rep.DayOfWeek(Daily_Chart,filename = Result_path + "DayOfWeek.txt")
print(dayofweek)