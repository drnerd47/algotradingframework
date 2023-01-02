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

import utils

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

approach = "ORB"

generalconfig = {"SquareOffSL":defs.ONELEG,"SquareOffTG":defs.ONELEG,
                     "EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":defs.BN,
                    "debug": defs.DEBUGTIME, "Slippage": defs.SLIPPAGE, "LotSize":defs.BNLOTSIZE,
                    "Premium": 50, "StartStrike": 30000, "EndStrikeStrike":40000, "BreakoutFactor":0, "Until":datetime.time(11,00)}


positionconfig = posconfig.positionconfigsinglebuydirecSL

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
      trade = strategies.OpeningRangeBreakout(masterdfBN, generalconfig, positionconfig)
    elif (generalconfig["symbol"] == defs.N):
      trade = strategies.OpeningRangeBreakout(masterdfN, generalconfig, positionconfig)
    print(trade)
    if (len(trade) > 0):
      trades = trades.append(trade)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))  
  start_date += delta

# print(trades)
trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"], axis = 1)
margin = utils.BuyMarginCalculator(trades, generalconfig["symbol"])
print("Margin Required is " + str(margin))
print("\n")
print(trades)
trades.to_csv(Result_path + approach + "trades.csv")

print("\n")
Daily_Chart = rep.GetDailyChartTI(trades)
# print(Daily_Chart)
Daily_Chart.to_csv(Result_path + approach + "DailyChart.csv")

print("\n")
report = rep.ReportTI(trades, Daily_Chart)
print(report)
report.to_csv(Result_path + approach + "Report.csv")

print("\n")
weeklyreport = rep.WeeklyBreakDownTI(Daily_Chart)
# print(weeklyreport)
weeklyreport.to_csv(Result_path + approach + "WeeklyReport.csv")

print("\n")
monthlyreport = rep.MonthlyBreakDownTI(Daily_Chart)
# print(monthlyreport)

print("\n")
dayofweek = rep.DayOfWeekTI(Daily_Chart)
# print(dayofweek)

