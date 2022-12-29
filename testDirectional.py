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

year = 2022
startmonth = 1
endmonth = 12
start_date = datetime.date(year, startmonth, 1)
end_date = datetime.date(year, endmonth, 31)

delta = datetime.timedelta(days=1)

user = "RI"

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

approach = "EMA"

if (approach == "RSI-Dual"):
  generalconfig = genconfig.generalconfigBNRSIDual
  positionconfig = posconfig.positionconfigsinglebuydirecSL
  TIconfig = TIconfigs.TIconfig_RSIDual
elif (approach == "ST"):
  generalconfig = genconfig.generalconfigNST
  positionconfig = posconfig.positionconfigsingleselldirecSL
  TIconfig = TIconfigs.TIconfigST
elif (approach == "BB2"):
  generalconfig = genconfig.generalconfigBNBB
  positionconfig = posconfig.positionconfigsingleselldirecSL
  TIconfig = TIconfigs.TIconfigBB2
elif (approach == "BB1"):
  generalconfig = genconfig.generalconfigBNBB
  positionconfig = posconfig.positionconfigsingleselldirecSL
  TIconfig = TIconfigs.TIconfigBB1
elif (approach == "RSI-ADX"):
  generalconfig = genconfig.generalconfigBNRSIADX
  positionconfig = posconfig.positionconfigsinglebuydirecSL
  TIconfig = TIconfigs.TIconfigRSI_ADX
elif (approach == "RSI2"):
  generalconfig = genconfig.generalconfigBNRSI2
  positionconfig = posconfig.positionconfigsingleselldirecSL
  TIconfig = TIconfigs.TIconfig2_RSI
elif (approach == "EMA"):
  generalconfig = genconfig.generalconfigBNMA
  positionconfig = posconfig.positionconfigsingleselldirecSL
  TIconfig = TIconfigs.TIconfigEMA
elif (approach == "SMA"):
  generalconfig = genconfig.generalconfigBNMA
  positionconfig = posconfig.positionconfigsingleselldirec
  TIconfig = TIconfigs.TIconfigSMA

data = direc.getTIIndicatorData(start_date, end_date, Nifty_Path, Banknifty_Path, generalconfig, TIconfig)

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
# print(trades)
trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"], axis = 1)

print("\n")
print(trades)
trades.to_csv(Result_path + approach + "trades.csv")

print("\n")
Daily_Chart = rep.GetDailyChartTI(trades)
print(Daily_Chart)
Daily_Chart.to_csv(Result_path + approach + "DailyChart.csv")

print("\n")
report = rep.ReportTI(trades, Daily_Chart)
print(report)
report.to_csv(Result_path + approach + "Report.csv")

print("\n")
weeklyreport = rep.WeeklyBreakDownTI(Daily_Chart)
print(weeklyreport)
weeklyreport.to_csv(Result_path + approach + "WeeklyReport.csv")

print("\n")
monthlyreport = rep.MonthlyBreakDownTI(Daily_Chart)
print(monthlyreport)

print("\n")
dayofweek = rep.DayOfWeekTI(Daily_Chart)
print(dayofweek)

