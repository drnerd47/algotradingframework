import datetime
import reporting as rep
import warnings
import DefaultConfigs as defconfigs
import time
import RunStrategy
warnings.filterwarnings("ignore")
import utils
import definitions as defs
import OptimizedConfigs as opconfigs
year = 2023
startmonth = 2
endmonth = 2
start_date = datetime.date(year, startmonth, 28)
end_date = datetime.date(year, endmonth, 28)

user = "SD"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/"

print("Test Directional Config")

Banknifty_Path = Root + "NIFTYOptionsData/Resampled Data/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/Resampled Data/Nifty/"
Finnifty_Path = Root + "NIFTYOptionsData/Resampled Data/Finnifty/"

#approach = "BB2"
#config = defconfigs.bb2_Nb
#approach = "RSI-Dual"
#config = defconfigs.rsidual_BNs
#approach = "RSI-ADX"
#config = defconfigs.rsiadx_BNs
# approach = "EMA"
# config = defconfigs.ema_Ns
#approach = "ST"
#config = defconfigs.st_BNs
approach = "RSI2"
config = defconfigs.rsi2_FNs
#config = opconfigs.rsi2Nb1

print(approach)
print(config)
(data, trades) = RunStrategy.RunDirectionalStrategy(start_date, end_date, approach, config, Banknifty_Path, Nifty_Path, Finnifty_Path)
if (config["action"] == defs.BUY):
  margin = utils.BuyMarginCalculator(trades, config["symbol"])
else:
  margin = utils.SellMarginCalculator("Naked", 1, 1, config["symbol"])
print("Margin is ", margin)
data.to_csv(Result_path + "Data_" + approach + ".csv")

# print("\n")
# print(trades)
trades.to_csv(Result_path + approach + "_trades.csv")

# print("\n")
Daily_Chart = rep.GetDailyChartTI(trades)
print(Daily_Chart)
print('\n')
print(Daily_Chart.describe())
print('\n')
print('Max Profit was on %s -> %s'% (Daily_Chart[Daily_Chart['Daily pnl'] == Daily_Chart['Daily pnl'].max()].index, Daily_Chart['Daily pnl'].max()))
print('\n')
print('Max Loss on %s -> %s'% (Daily_Chart[Daily_Chart['Daily pnl'] == Daily_Chart['Daily pnl'].min()].index, Daily_Chart['Daily pnl'].min()))
Daily_Chart.to_csv(Result_path + approach + "DailyChart.csv")

# print("\n")
report = rep.ReportTI(trades, Daily_Chart)
print(report)
report.to_csv(Result_path + approach + "Report.csv")

# print("\n")
weeklyreport = rep.WeeklyBreakDownTI(Daily_Chart)
# print(weeklyreport)
weeklyreport.to_csv(Result_path + approach + "WeeklyReport.csv")

# print("\n")
monthlyreport = rep.MonthlyBreakDownTI(Daily_Chart)
print(monthlyreport)

# print("\n")
dayofweek = rep.DayOfWeekTI(Daily_Chart)
print(dayofweek)

