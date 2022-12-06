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

strategytypes = {"IntraDayN": 1, "IntraDayBN": 2, "IntradayNRE": 3, "IntradayBNRE": 4, "ExpiryBN": 5, "ExpiryN": 6, "NextDayBNMW": 7, "NextDayNMW": 8,
                 "NextDayBNMW": 9, "NextDayNMW": 10, "IntradaySA": 11, "ExpirySA": 12, "NextDaySA": 13}
def RunStrategy(strattypes):
    if (strattypes == strategytypes["IntraDayN"]):
        generalconfig = genconfig.generalconfigIntradayN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["IntraDayBN"]):
        generalconfig = genconfig.generalconfigIntradayBN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["IntradayNRE"]):
        generalconfig = genconfig.generalconfigIntradayREN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["IntradayBNRE"]):
        generalconfig = genconfig.generalconfigIntradayREBN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["ExpiryBN"]):
        generalconfig = genconfig.generalconfigExpiryBN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["ExpiryN"]):
        generalconfig = genconfig.generalconfigExpiryN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["NextDayBNMW"]):
        generalconfig = [genconfig.generalconfigNextDayBNMW, genconfig.generalconfigNextDayNMW]
        positionconfig = posconfigs.getStatArbDef()
    elif (strattypes == strategytypes["NextDayNMW"]):
        generalconfig = genconfig.generalconfigBN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["NextDayBNMW"]):
        generalconfig = [genconfig.generalconfigNextDayBNMW, genconfig.generalconfigNextDayNMW]
        positionconfig = posconfigs.getStatArbDef()
    elif (strattypes == strategytypes["NextDayNMW"]):
        generalconfig = genconfig.generalconfigBN
        positionconfig = posconfigs.positionconfigShortStraddle
    elif (strattypes == strategytypes["IntradaySA"]):
        generalconfig = [genconfigs.generalconfigBN, genconfigs.generalconfigN]
        positionconfig = st.positionconfitStatArbStraddle


    trade = pd.DataFrame()
    trades = []

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


