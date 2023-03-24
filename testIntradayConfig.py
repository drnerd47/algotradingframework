import datetime

import RunStrategy
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import warnings
import GetConfigs
import time
import DefaultConfigs as defcon
import OptimizedConfigs as opcon

warnings.filterwarnings("ignore")

user = "SD"

year = 2023
startmonth = 1
endmonth = 3
start_date = datetime.date(year, startmonth, 16)
end_date = datetime.date(year, endmonth, 16)

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/IND/Test/"

# Banknifty_Path = Root + "NIFTYOptionsData/Resampled Data/Banknifty/"
# Nifty_Path = Root + "NIFTYOptionsData/Resampled Data/Nifty/"
# Finnifty_Path = Root + "NIFTYOptionsData/Resampled Data/Finnifty/"

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"
Finnifty_Path = Root + "NIFTYOptionsData/OptionsData/Finnifty/"

# Default Config
config = defcon.ind_straddle_BN_OL

# config.update({ 'EnterTime':datetime.time(10, 30), 'Delta':0, 'DeltaThu':0}) # , 'ExitTime': datetime.time(14, 30)

# config.update({ 'Delta':1000, 'DeltaThu':1000 }) 
# config.update({ 'EnterTime':datetime.time(10, 30), 'ExitTime': datetime.time(14, 30) }) 
#configs = [defcon.ind_straddle_BN_OL1, defcon.ind_straddle_N_OL1, defcon.ind_straddle_BN_AL, defcon.ind_straddle_N_AL,
#           defcon.ind_straddle_BN_OL_RE, defcon.ind_straddle_N_OL_RE, defcon.ind_straddle_BN_ALS, defcon.ind_straddle_N_ALS]
approach = "INDOLBN"
#approachVec = ["INDOLBN", "INDOLN", "INDALBN", "INDALN", "INDOLREBN", "INDOLREN", "INDALSBN", "INDALSN"]
trades, PnL = RunStrategy.RunIntradayStrategy(start_date, end_date, config, Banknifty_Path, Nifty_Path, Finnifty_Path)
print("\n")
# print(trades)
# trades.to_csv(Result_path + approach + "trades.csv")

print("\n")
Daily_Chart = rep.GetDailyChart(trades)
# print(Daily_Chart)
# Daily_Chart.to_csv(Result_path + approach + "DailyChart.csv")

print("\n")
report = rep.Report(trades, Daily_Chart)
print(report)
# report.to_csv(Result_path + approach + "Report.csv")

print("\n")
weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
print(weeklyreport)
# weeklyreport.to_csv(Result_path + approach + "WeeklyReport.csv")

print("\n")
monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
print(monthlyreport)

print("\n")
dayofweek = rep.DayOfWeek(Daily_Chart)
print(dayofweek)

# print(PnL)