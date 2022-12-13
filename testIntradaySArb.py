import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import generalconfigs as genconfigs
import positionconfigs as st

import warnings
warnings.filterwarnings("ignore")

user = "MS"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/"
elif user == "MS":
  Root = "C:/Users/shahm/(8)Work/SRE/"
  Result_path = "C:/Users/shahm/(8)Work/SRE/NIFTYOptionsData/OptionsData/Results/test/"

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 8, 31)
delta = datetime.timedelta(days=1)


trade = pd.DataFrame()
trades = []
generalconfigBN = genconfigs.generalconfigIntradayBN
generalconfigN = genconfigs.generalconfigIntradayN
positionconfig = st.positionconfitStatArbStraddle

trades = pd.DataFrame()

while start_date <= end_date:
  trade = pd.DataFrame()
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(NPath)
  my_fileBN = Path(BNPath)
  print(date_string)
  if my_fileN.exists() and my_fileBN.exists():
    masterdfN = atom.LoadDF(NPath)
    masterdfBN = atom.LoadDF(BNPath)
    generalconfigBN["symbol"] = defs.BN
    trade1 = strategies.IntraDayStrategy(masterdfBN, generalconfigBN, positionconfig[0])
    generalconfigN["symbol"] = defs.N
    trade2 = strategies.IntraDayStrategy(masterdfN, generalconfigN, positionconfig[1])
    trade = trade.append(trade1)
    trade = trade.append(trade2)
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
Daily_Chart.to_csv("Results/trades.csv")

report = rep.Report(trades, Daily_Chart)
print(report)
report.to_csv("Results/report.csv")

weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
print(weeklyreport)

monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
print(monthlyreport)

dayofweek = rep.DayOfWeek(Daily_Chart)
print(dayofweek)


