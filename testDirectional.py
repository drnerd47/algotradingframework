import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import generalconfigs as genconfigs
import positionconfigs as posconfigs
import directional as direc
import operator
import warnings

warnings.filterwarnings("ignore")

start_date = datetime.date(2022,1,1)
end_date = datetime.date(2022, 8, 30)
delta = datetime.timedelta(days=1)


Banknifty_Path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Nifty/"


generalconfig = {"symbol":defs.BN, "ExitTime": datetime.time(15,15), "Resample": '3T', "StopLoss": True, "Target": False, "StopLossCond": "TIBased", "TargetCond": "TIBased"}
#generalconfig = {"symbol":defs.BN, "ExitTime": datetime.time(15,15), "Resample": '10T', "StopLoss": True, "Target": False, "StopLossCond": "PremiumBased", "TargetCond": "PremiumBased"}

positionconfig = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "LotSize":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BULL},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"LotSize":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BULL}, 
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"LotSize":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BULL},
                    {"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "LotSize":1,
                       "SL": defs.NO, "Target":defs.NO, "Stance": defs.BEAR},
                      {"Type":defs.CALL,"Action":defs.SELL,"Delta":0,"LotSize":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BEAR}, 
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"LotSize":1,
                       "SL": defs.NO,"Target":defs.NO, "Stance": defs.BEAR}]

# positionconfig = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "LotSize":1,
#                        "SL": defs.YES, "Target":defs.NO, "Stance": defs.BEAR, "SLPc": 40}, 
#                        {"Type":defs.PUT,"Action":defs.SELL,"Delta":0, "LotSize":1,
#                        "SL": defs.YES, "Target":defs.NO, "Stance": defs.BULL, "SLPc": 40}]

TIconfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 60, "ThreshBear": 40, "Window": 14, "SL": defs.YES, "Target": defs.YES, "SLBull": 40, "SLBear": 60, 
           "TargetBull": 70, "TargetBear": 18, "BullOperator": operator.gt, "BearOperator": operator.lt}, 
			{"TI": "ADX","columnname":"ADX14", "Window": 14, "ThreshBull": 20, "ThreshBear": 20, "SL": defs.NO, "Target": defs.NO, 
           "BullOperator": operator.gt, "BearOperator": operator.gt}]

# TIconfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": 40, "ThreshBear": 60, "Window": 14, "SL": defs.NO, "Target": defs.NO,  
#             "BullOperator": operator.lt, "BearOperator": operator.gt}, 
# 			{"TI": "RSI","columnname":"RSI2", "Window": 2, "ThreshBull": 10, "ThreshBear": 90, "SL": defs.NO, "Target": defs.NO, 
#             "BullOperator": operator.gt, "BearOperator": operator.gt}]

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
      trade = strategies.IntraDayStrategy(masterdfN, generalconfig, positionconfig)
    print(trade)
    if (len(trade) > 0):
      trades = trades.append(trade)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta

trades['date'] = pd.to_datetime(trades["date"])
trades = trades.reset_index()
trades = trades.drop(["index"],axis = 1)

print("trades is ", trades)
Daily_Chart = rep.GetDailyChart(trades)
print("daily chart is ",Daily_Chart)
Daily_Chart.to_csv("D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/dailychart.csv")

report = rep.Report(trades, Daily_Chart)
print("report is ",report)
report.to_csv("D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/report.csv")

weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
weeklyreport.to_csv("D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/weeklyreport.csv")
print(weeklyreport)

print(report["Overall Profit"])
print(report["Max Drawdown(MDD)"])
monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
#monthlyreport.to_csv("D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/monthlyreport.csv")
print("monthly report is ",monthlyreport)

dayofweek = rep.DayOfWeek(Daily_Chart)
#dayofweek.to_csv("D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/dayofweekreport.csv")
print("day of week is ",dayofweek)




