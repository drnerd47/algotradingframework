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
year = 2022
startmonth = 1
endmonth = 12
start_date = datetime.date(year, startmonth, 1)
end_date = datetime.date(year, endmonth, 31)

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

print("Test Directional Config")

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"

approach = "BB2"
config = defconfigs.bb2_Ns
#approach = "RSI-Dual"
#config = defconfigs.rsidual_Ns
#approach = "RSI-ADX"
#config = defconfigs.rsiadx_BNs
#approach = "EMA"
#config = defconfigs.ema_Ns
#approach = "ST"
#config = defconfigs.st_Nb
#approach = "RSI2"
#config = defconfigs.rsi2_BNb
#config = opconfigs.rsi2Nb1

print(approach)
print(config)
(data, trades) = RunStrategy.RunDirectionalStrategy(start_date, end_date, approach, config, Banknifty_Path, Nifty_Path)
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
# print(Daily_Chart)
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

