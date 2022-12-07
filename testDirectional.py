import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import generalconfigs as genconfigs
import positionconfigs as st
import directional as direc

import warnings
warnings.filterwarnings("ignore")

start_date = datetime.date(2022,1,1)
end_date = datetime.date(2022, 8, 30)
delta = datetime.timedelta(days=1)

data = direc.getMultipledayData(start_date, end_date, 'BANKNIFTY', '3T')
data = direc.getRSI(data, 14)
data = direc.getADX(data, 14)

Banknifty_Path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = '../NIFTYOptionsData/OptionsData/nifty/'


generalconfig = genconfigs.generalconfigIntradayBN
positionconfig = [{"Type":defs.CALL,"Action":defs.SELL,"Delta":0, "SLPc":40, "TargetPc":77, "LotSize":1,
                       "SL": defs.YES, "Target":defs.YES},
                      {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"SLPc":40,"TargetPc":77,"LotSize":1,
                       "SL": defs.YES,"Target":defs.YES}, 
                       {"Type":defs.PUT,"Action":defs.SELL,"Delta":0,"SLPc":40,"TargetPc":77,"LotSize":1,
                       "SL": defs.YES,"Target":defs.YES}]


trade = pd.DataFrame()
trades = pd.DataFrame()

while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  my_fileBN = Path(BNPath)
  print(date_string)
  if my_fileBN.exists():
    masterdfBN = atom.LoadDF(BNPath)
    if (generalconfig["symbol"] == defs.BN):
      trade = strategies.RSIStrategy(data, masterdfBN, generalconfig, positionconfig, start_date)
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
print(weeklyreport)

print(report["Overall Profit"])
print(report["Max Drawdown(MDD)"])
monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
print("monthly report is ",monthlyreport)

dayofweek = rep.DayOfWeek(Daily_Chart)
print("day of week is ",dayofweek)




