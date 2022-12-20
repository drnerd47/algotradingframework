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
import warnings
import TIconfigs
import numpy as np

warnings.filterwarnings("ignore")

start_date = datetime.date(2021, 2, 1)
end_date = datetime.date(2021, 2, 28)
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

#generalconfig = genconfig.generalconfigNRSIDual
#positionconfig = posconfig.positionconfigsinglebuydirecSL
#TIconfig = TIconfigs.TIconfig_RSIDual
generalconfig = genconfig.generalconfigBNBB
positionconfig = posconfig.positionconfigsinglebuydirec
TIconfig = TIconfigs.TIconfigBB2
approach = "BB2"
#generalconfig = genconfig.generalconfigBNRSIADX
#positionconfig = posconfig.positionconfigsinglebuydirec
#TIconfig = TIconfigs.TIconfigRSI_ADX

if (generalconfig["symbol"] == defs.N):
    dataorig = direc.getMultipledayData(start_date, end_date, generalconfig["EnterTime"], Nifty_Path, defs.N, generalconfig["Resample"])
else:
    dataorig = direc.getMultipledayData(start_date, end_date, generalconfig["EnterTime"], Banknifty_Path, defs.BN, generalconfig["Resample"])
data = direc.getTI(dataorig, TIconfig)
data['Signal'] = np.nan

trade = pd.DataFrame()
trades = pd.DataFrame()

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(NPath)
  my_fileBN = Path(BNPath)
  print("Working on file - "+date_string)
  if my_fileN.exists() and my_fileBN.exists():
    masterdfN = atom.LoadDF(NPath)
    masterdfBN = atom.LoadDF(BNPath)
    if (generalconfig["symbol"] == defs.BN):
      trade = strategies.DirectionalStrategy(data, masterdfBN, generalconfig, positionconfig, TIconfig, start_date)
    elif (generalconfig["symbol"] == defs.N):
      trade = strategies.DirectionalStrategy(data, masterdfN, generalconfig, positionconfig, TIconfig, start_date)
    #print(trade)
    if (len(trade) > 0):
      trades = trades.append(trade)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))  
  start_date += delta

data.to_csv(Result_path + "Data_" + approach + ".csv")
trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"], axis = 1)

print("\n")
print(trades)
trades.to_csv(Result_path + approach + "trades.csv")

print("\n")
Daily_Chart = rep.GetDailyChart(trades)
print(Daily_Chart)
Daily_Chart.to_csv(Result_path + approach + "DailyChart.csv")

print("\n")
report = rep.Report(trades, Daily_Chart)
print(report)
report.to_csv(Result_path + approach + "Report.csv")

print("\n")
weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
print(weeklyreport)
weeklyreport.to_csv(Result_path + approach + "WeeklyReport.csv")

print("\n")
monthlyreport = rep.MonthlyBreakDown(Daily_Chart,filename = Result_path + approach + "MonthlyBreakDown.txt")
print(monthlyreport)

print("\n")
dayofweek = rep.DayOfWeek(Daily_Chart,filename = Result_path + approach + "DayOfWeek.txt")
print(dayofweek)

