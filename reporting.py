import pandas as pd
import numpy as np
import pandas as pd

def GetDailyChart(trades):
  Daily_Chart = pd.DataFrame(trades, columns=["date", "Daily pnl", "DayOfWeek", "Month", "Year", "Spot pnl", "Fut pnl"])
  Daily_pnl = trades.groupby("date")["pnl"].sum(np.ptp)
  Daily_pnl = trades.groupby("date")["pnl"].sum(np.ptp)
  Daily_Chart = Daily_pnl.to_frame()
  Daily_Chart["Date"] = pd.to_datetime(Daily_Chart.index)
  Daily_Chart["Daily pnl"] = trades.groupby("date")["pnl"].sum(np.ptp)
  Daily_Chart["DayOfWeek"] = Daily_Chart["Date"].dt.day_name()
  Daily_Chart["Month"] = Daily_Chart['Date'].dt.month_name()
  Daily_Chart["Year"] = Daily_Chart['Date'].dt.year
  Daily_Chart = Daily_Chart.drop(["pnl"], axis=1)
  Daily_Chart = Daily_Chart.reset_index()
  Daily_Chart = Daily_Chart.drop(["date"], axis=1)
  Daily_Chart["Daily Cummulative pnl"] = Daily_Chart['Daily pnl'].cumsum()

  return Daily_Chart




def Report(trades, Daily_Chart):
  rep = {}
  date = trades["date"].tolist()
  reason = trades["Reason"].tolist()
  dct = {}
  for x in range(len(date)):
    if reason[x] == "SL HIT":
      if date[x] not in dct:
        dct[date[x]] = 1
      else:
        dct[date[x]] += 1
  for x in range(len(date)):
    if date[x] not in dct:
      dct[date[x]] = 0
    counts = list(dct.values())

  def generate_streak_info(trades):
    data = shots['Reason'].to_frame()
    data['start_of_streak'] = data['Reason'].ne(data['Reason'].shift())
    data['streak_id'] = data.start_of_streak.cumsum()
    data['streak_counter'] = data.groupby('streak_id').cumcount() + 1
    shots_with_streaks = pd.concat([shots, data['streak_counter']], axis=1)
    return shots_with_streaks

  shots = trades['Reason'].to_frame()
  generate_streak_info(shots)

  Max_winning_Streak = generate_streak_info(shots)[generate_streak_info(shots)["Reason"] == "Time Up"]["streak_counter"].max()
  Max_Losing_Streak = generate_streak_info(shots)[generate_streak_info(shots)["Reason"] == "SL HIT"]["streak_counter"].max()

  Zero_SL_HIT = counts.count(0)
  First_SL_HIT = counts.count(1)
  Second_SL_HIT = counts.count(2)
  Total_Profit_on_win_days = Daily_Chart[Daily_Chart["Daily pnl"] > 0]["Daily pnl"].sum()
  Total_Loss_on_bad_days = Daily_Chart[Daily_Chart["Daily pnl"] < 0]["Daily pnl"].sum()
  Overall_Net = Total_Profit_on_win_days - (-Total_Loss_on_bad_days)
  Max_Profit = Daily_Chart["Daily pnl"].max()
  Max_Loss = Daily_Chart["Daily pnl"].min()
  Total_no_of_trades = trades["pnl"].count()
  Total_no_of_days = Daily_Chart[Daily_Chart["Daily pnl"] != 0]["Daily pnl"].count()
  Avg_Day_Net = Overall_Net / Total_no_of_days
  Total_no_of_win_trades = Daily_Chart[Daily_Chart["Daily pnl"] > 0]["Daily pnl"].count()
  Total_no_of_bad_trades = Daily_Chart[Daily_Chart["Daily pnl"] < 0]["Daily pnl"].count()
  Avg_Profit_win_trades = Total_Profit_on_win_days / Total_no_of_win_trades
  Avg_Loss_bad_trades = Total_Loss_on_bad_days / Total_no_of_bad_trades
  Win_Percentage_trades = '{:.1%}'.format(Total_no_of_win_trades / Total_no_of_days)
  Loss_Percentage_trades = '{:.1%}'.format(Total_no_of_bad_trades / Total_no_of_days)
  Win_Ratio = Total_no_of_win_trades / Total_no_of_trades
  Loss_Ratio = Total_no_of_bad_trades / Total_no_of_trades
  Expectancy = ((Avg_Profit_win_trades / -Avg_Loss_bad_trades) * Win_Ratio) - Loss_Ratio
  Expiry_Date = trades["Expiry"]
  Daily_Chart["Expiry_Date"] = pd.to_datetime(Expiry_Date, infer_datetime_format=True)
  Expiry_info = Daily_Chart[Daily_Chart["Date"] == Daily_Chart["Expiry_Date"]]
  Expiry_Net = Expiry_info["Daily pnl"].sum()
  Total_no_of_expiry = Expiry_info[Expiry_info["Daily pnl"] != 0]["Daily pnl"].count()
  Avg_Expiry_Net = Expiry_Net / Total_no_of_expiry
  Roll_max = Daily_Chart["Daily Cummulative pnl"].rolling(window=Daily_Chart.size, min_periods=1).max()
  Daily_Drawdown = Daily_Chart["Daily Cummulative pnl"] - Roll_max
  Max_Drawdown = min(Daily_Drawdown)
  Return_to_MDD_Ratio = Overall_Net / Max_Drawdown
  Lot_Size = trades['Trade Type'].nunique()

  rep = {"Overall Profit": Overall_Net, "Avg Expiry Profit": Avg_Expiry_Net, "Avg Day Profit": Avg_Day_Net,
         "Max Profit": Max_Profit, "Max Loss": Max_Loss,
         "Total Expiries": Total_no_of_expiry, "Win%": Win_Percentage_trades, "Loss%": Loss_Percentage_trades,
         "Avg Profit On Win Days": Avg_Profit_win_trades, "Avg Loss On Loss Days": Avg_Loss_bad_trades,
         "Max Drawdown(MDD)": Max_Drawdown,
         "Return to MDD Ratio": Return_to_MDD_Ratio, "Expectancy": Expectancy, "0 SL/TP Hit Count": Zero_SL_HIT,
         "1 SL/TP Hit Count": First_SL_HIT,
         "2 SL/TP Hit Count": Second_SL_HIT, "Max_Winning_Streak": Max_winning_Streak,
         "Max_Losing_Streak": Max_Losing_Streak, "Lot Size": Lot_Size}
  report = pd.DataFrame(rep, index=[0])
  return report


def WeeklyBreakDown(Daily_Chart):
  Daily_Chart["Date"] = pd.to_datetime(Daily_Chart["Date"])
  Daily_Chart = Daily_Chart.set_index("Date")
  y = Daily_Chart.resample('W-Fri').sum()
  Weekly_BreakDown = pd.DataFrame(y, columns=["Daily pnl"])
  Weekly_BreakDown['Week Count'] = ["Week" + "-" + str(i) for i in range(1, len(Weekly_BreakDown) + 1)]
  Weekly_BreakDown = Weekly_BreakDown.rename(columns = {'Daily pnl':'Weekly pnl'})
  return Weekly_BreakDown

def MonthlyBreakDown(Daily_Chart, filename):
  y = Daily_Chart.groupby("Year")
  for key, item in y:
    p = y.get_group(key).groupby("Month")["Daily pnl"].sum()
    Month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']

    file = open(filename, 'w')
    file.write("Yearly BreakDown For Months\n\n")
    file.write(str(key) + '\n\n')
    p = p.reindex(Month_order, axis=0)
    file.write(str(p) + "\n\n")
  f = Daily_Chart.groupby("Month")["Daily pnl"].sum()
  Month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November', 'December']
  f = f.reindex(Month_order, axis=0)
  file.write('Total BreakDown For Months\n\n')
  file.write(str(f) + "\n\n")
  file.close()


def DayOfWeek(Daily_Chart, filename):
  a = "DayOfWeek\n"
  file = open(filename, 'w')
  y = Daily_Chart.groupby("Year")
  for key, item in y:
    r = y.get_group(key).groupby("DayOfWeek")['Daily pnl'].sum()
    Week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    r = r.reindex(Week_order, axis=0)
    file.write(a + '\n\n')
    file.write(str(key) + '\n\n')
    file.write(str(r) + "\n\n")
  g = Daily_Chart.groupby("DayOfWeek")["Daily pnl"].sum()
  Week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  g = g.reindex(Week_order, axis=0)
  file.write("Total Breakdown for Months\n\n")
  file.write(str(g) + '\n\n')
  file.close()