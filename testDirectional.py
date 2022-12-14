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
import operator
import warnings
import TIconfigs

warnings.filterwarnings("ignore")

start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2021, 1, 10)
delta = datetime.timedelta(days=1)

user = "SD"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/"
elif user == "MS":
  Root = "Moulik's File path"
  Result_path = " Moulik's result path"

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"



generalconfig = genconfig.generalconfigBNRSI2
positionconfig = posconfig.positionconfigsingleselldirecSL
TIconfig = TIconfigs.TIconfig2_RSI  




if (generalconfig["symbol"] == defs.N):
    data = direc.getMultipledayData(start_date, end_date, Nifty_Path, defs.N, generalconfig["Resample"])
else:
    data = direc.getMultipledayData(start_date, end_date, Banknifty_Path, defs.BN, generalconfig["Resample"])
print("\n")
data = direc.getTI(data, TIconfig)
print("\n")
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
      trade = strategies.DirectionalStrategy(data, masterdfBN, generalconfig, positionconfig, TIconfig, start_date)
    elif (generalconfig["symbol"] == defs.N):
      trade = strategies.DirectionalStrategy(data, masterdfN, generalconfig, positionconfig, TIconfig, start_date)
    print(trade)
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

