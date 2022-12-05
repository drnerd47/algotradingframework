import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import positionconfigs as posconfigs
import generalconfigs as genconfig

import warnings
warnings.filterwarnings("ignore")

Banknifty_Path = '../NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = '../NIFTYOptionsData/OptionsData/nifty/'

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 8, 31)
delta = datetime.timedelta(days=1)

strategytypes = {"IntraDayN": 1, "IntraDayBN": 2, "IntradayNRE": 3, "IntradayBNRE": 4, "ExpiryBN": 5, "ExpiryN": 6, "NextDayBN": 7, "NextDayN": 8}

def RunStrategy(strattypes):
    if (strattypes == strategytypes["IntraDayN"]):
      generalconfig = genconfig.generalconfigN
    elif (strattypes == strategytypes["IntraDayBN"])
      generalconfig = genconfig.generalconfigBN
    elif (strattypes == strategytypes["IntradayNRE"])
      generalconfig = genconfig.generalconfigREN
    elif (strattypes == strategytypes["IntradayBNRE"])
      generalconfig = genconfig.generalconfigREBN
    elif (strattypes == strategytypes["ExpiryBN"])
      generalconfig = genconfig.generalconfigExpiryBN
    elif (strattypes == strategytypes["ExpiryN"])
      generalconfig = genconfig.generalconfigExpiryN
    elif (strattypes == strategytypes["NextDayBN"])
      generalconfig = genconfig.generalconfigBN
    elif (strattypes == strategytypes["NextDayN"])
      generalconfig = genconfig.generalconfigBN

trade = pd.DataFrame()
trades = []


positionconfigSS = posconfigs.getStraddles(defs.SELL, defs.NO, defs.NO, 35, 50)
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
      positionconfigArr = posconfigs.getStatArbDef()
      (trade1, positions) = strategies.MultiDayStrategy(masterdfBN, positions, generalconfig, positionconfigArr[0])
      (trade2, positions) = strategies.MultiDayStrategy(masterdfN, positions, generalconfig, positionconfigArr[1])
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

print(trades)
trades.to_csv("Results/trades.csv")

Daily_Chart = rep.GetDailyChart(trades)
print(Daily_Chart)
Daily_Chart.to_csv("Results/dailychart.csv")

report = rep.Report(trades, Daily_Chart)
print(report)
report.to_csv("Results/report.csv")

weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
print(weeklyreport)

monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
print(monthlyreport)

dayofweek = rep.DayOfWeek(Daily_Chart)
print(dayofweek)


