import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import positionconfigs as posconfigs
import generalconfigs as genconfigs

import warnings
warnings.filterwarnings("ignore")

user = "SD"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/Positional/"

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

year = 2023
delta = datetime.timedelta(days=1)

symbols = [defs.BN, defs.BN, defs.BN, defs.N, defs.N, defs.N, defs.BN, defs.BN, defs.BN, defs.N, defs.N, defs.N]
approach = ["ICPBNFri", "ICPBNMon", "ICPBNTue", "ICPNFri", "ICPNMon", "ICPNTue",
            "CSPBNFri", "CSPBNMon", "CSPBNTue", "CSPNFri", "CSPNMon", "CSPNTue"]
days = [defs.FRI, defs.MON, defs.TUE, defs.FRI, defs.MON, defs.TUE, defs.FRI, defs.MON, defs.TUE, defs.FRI, defs.MON, defs.TUE]
type = ["IC", "IC", "IC", "IC", "IC", "IC", "CS", "CS", "CS", "CS", "CS", "CS"]
numStrategies = 12

for i in range(numStrategies):
    print("Running " + approach[i])
    if (days[i] == defs.FRI):
      if (symbols[i] == defs.N):
        SL = 150
        Delta = 500
      else:
        SL = 150
        Delta = 1000
    elif (days[i] == defs.MON):
      if (symbols[i] == defs.N):
        SL = 120
        Delta = 500
      else:
        SL = 150
        Delta = 1000
    elif (days[i] == defs.TUE):
      if (symbols[i] == defs.N):
        SL = 150
        Delta = 300
      else:
        SL = 120
        Delta = 500

    if (symbols[i] == defs.N):
        generalconfig = genconfigs.GetGeneralConfigExpiry(defs.ONELEG, defs.ONELEG, defs.N, [days[i]], [defs.THU])
        if (type[i] == "CS"):
            positionconfig = posconfigs.getCallSpread(Delta, Delta + 1000, defs.NO, defs.YES, defs.NO, 35, SL, 50)
        else:
            positionconfig = posconfigs.getIronCondor(Delta, Delta + 1000, defs.NO, defs.YES, defs.NO, 35, SL, 50)
    else:
        generalconfig = genconfigs.GetGeneralConfigExpiry(defs.ONELEG, defs.ONELEG, defs.BN, [days[i]], [defs.THU])
        if (type[i] == "CS"):
            positionconfig = posconfigs.getCallSpread(Delta, Delta + 2000, defs.NO, defs.YES, defs.NO, 35, SL, 50)
        else:
            positionconfig = posconfigs.getIronCondor(Delta, Delta + 2000, defs.NO, defs.YES, defs.NO, 35, SL, 50)

    trade = pd.DataFrame()
    trades = pd.DataFrame()
    positions = []
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)

    while start_date <= end_date:
      date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
      BNPath = Banknifty_Path + date_string
      NPath = Nifty_Path + date_string
      my_fileN = Path(BNPath)
      my_fileBN = Path(NPath)
      if my_fileN.exists() and my_fileBN.exists():
        masterdfN = atom.LoadDF(NPath)
        masterdfBN = atom.LoadDF(BNPath)
        if (generalconfig["symbol"] == defs.BN):
          (trade, positions) = strategies.MultiDayStrategy(masterdfBN, positions, generalconfig, positionconfig)
        elif (generalconfig["symbol"] == defs.N):
          (trade, positions) = strategies.MultiDayStrategy(masterdfN, positions, generalconfig, positionconfig)
        elif (generalconfig["symbol"] == defs.BOTH):
          positionconfig = strategies.getStatArbDef()
          (trade1, positions) = strategies.MultiDayStrategy(masterdfBN, positions, generalconfig, positionconfig[0])
          (trade2, positions) = strategies.MultiDayStrategy(masterdfN, positions, generalconfig, positionconfig[1])
          trade.append(trade1)
          trade.append(trade2)
        if (len(trade) > 0):
            trades = trades.append(trade)
      start_date += delta

    trades['date'] = pd.to_datetime(trades["date"])
    trades = trades.reset_index()
    trades = trades.drop(["index"], axis = 1)

    print("\n")
    print(trades)
    trades.to_csv(Result_path + str(year) + "/" + approach[i] + "_trades.csv")

    print("\n")
    Daily_Chart = rep.GetDailyChart(trades)
    print(Daily_Chart)
    Daily_Chart.to_csv(Result_path + str(year) + "/" + approach[i] + "_DailyChart.csv")

    print("\n")
    report = rep.Report(trades, Daily_Chart)
    print(report)
    report.to_csv(Result_path + str(year) + "/" + approach[i] + "_Report.csv")

    print("\n")
    weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
    print(weeklyreport)
    weeklyreport.to_csv(Result_path + str(year) + "/" + approach[i] + "_WeeklyReport.csv")

    print("\n")
    monthlyreport = rep.MonthlyBreakDown(Daily_Chart)
    print(monthlyreport)

    print("\n")
    dayofweek = rep.DayOfWeek(Daily_Chart)
    print(dayofweek)