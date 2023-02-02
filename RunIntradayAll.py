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

user = "RI"

year = 2022
startmonth = 1
endmonth = 12
start_date = datetime.date(year, startmonth, 1)
end_date = datetime.date(year, endmonth, 31)

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/IND/" + str(year) + "/"

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

# Default Config
# config = opcon.ind_straddle_BN_2
configs = [defcon.ind_straddle_BN_OL1, defcon.ind_straddle_N_OL1, defcon.ind_straddle_BN_AL, defcon.ind_straddle_N_AL,
           defcon.ind_straddle_BN_OL_RE, defcon.ind_straddle_N_OL_RE, defcon.ind_straddle_BN_ALS, defcon.ind_straddle_N_ALS]
# Optimized Config
approachVec = ["INDOLBN", "INDOLN", "INDALBN", "INDALN", "INDOLREBN", "INDOLREN", "INDALSBN", "INDALSN"]
numStrategies = 8
for n in range(numStrategies):
    approach = approachVec[n]
    config = configs[n]
    trades = RunStrategy.RunIntradayStrategy(start_date, end_date, config, Banknifty_Path, Nifty_Path)
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
    monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
    print(monthlyreport)

    print("\n")
    dayofweek = rep.DayOfWeek(Daily_Chart)
    print(dayofweek)