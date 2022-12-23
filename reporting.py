import pandas as pd
import numpy as np
import pandas as pd

def GetDailyChart(trades):
  Daily_Chart = pd.DataFrame()
  Daily_Chart["Daily pnl"] = trades.groupby("date")["pnl"].sum(np.ptp)
  Daily_Chart['Fut pnl'] = trades.groupby("date")["Futpnl"].sum(np.ptp)
  Daily_Chart['Spot pnl'] = trades.groupby("date")['Spotpnl'].sum(np.ptp)

  Daily_Chart["Daily Cummulative pnl"] = Daily_Chart['Daily pnl'].cumsum()
  Daily_Chart['Spot Cummulative pnl'] = Daily_Chart['Spot pnl'].cumsum()
  Daily_Chart['Fut Cummulative pnl'] = Daily_Chart['Fut pnl'].cumsum()

  Daily_Chart.index = pd.to_datetime(Daily_Chart.index)
  Daily_Chart['DayOfWeek'] = Daily_Chart.index.day_name()
  Daily_Chart["Month"] = Daily_Chart.index.month_name()
  Daily_Chart["Year"] = Daily_Chart.index.year

  return Daily_Chart

def generate_streak_info(trades):
  data = trades['Reason'].to_frame()
  data['start_of_streak'] = data['Reason'].ne(data['Reason'].shift())
  data['streak_id'] = data.start_of_streak.cumsum()
  data['streak_counter'] = data.groupby('streak_id').cumcount() + 1
  return data

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

  # Calculating Streak
  shots = generate_streak_info(trades)
  Max_winning_Streak = shots[shots["Reason"] == "Time Up"]["streak_counter"].max()
  Max_Losing_Streak = shots[shots["Reason"] == "SL HIT"]["streak_counter"].max()
  # Calculating SL / TG counts
  Zero_SL_HIT = counts.count(0)
  First_SL_HIT = counts.count(1)
  Second_SL_HIT = counts.count(2)
  # Calculating Total Profit and Loss  
  Total_profit_on_win_days = Daily_Chart[Daily_Chart["Daily pnl"] > 0]["Daily pnl"].sum()
  Total_Loss_on_bad_days = Daily_Chart[Daily_Chart["Daily pnl"] < 0]["Daily pnl"].sum()

  Total_profit_on_win_days_spot = Daily_Chart[Daily_Chart['Spot pnl'] > 0]['Spot pnl'].sum()
  Total_Loss_on_bad_days_spot = Daily_Chart[Daily_Chart['Spot pnl'] < 0]['Spot pnl'].sum()

  Total_profit_on_win_days_fut = Daily_Chart[Daily_Chart['Fut pnl'] > 0]['Fut pnl'].sum()
  Total_Loss_on_bad_days_fut = Daily_Chart[Daily_Chart['Fut pnl'] < 0]['Fut pnl'].sum()  
  
  Overall_Net = Total_profit_on_win_days + Total_Loss_on_bad_days
  Overall_Net_spot = Total_profit_on_win_days_spot + Total_Loss_on_bad_days_spot
  Overall_Net_fut = Total_profit_on_win_days_fut + Total_Loss_on_bad_days_fut
  # Maximum Profit and Maximum Loss
  Max_Profit = Daily_Chart["Daily pnl"].max()
  Max_Loss = Daily_Chart["Daily pnl"].min()

  Max_Profit_fut = Daily_Chart['Fut pnl'].max()
  Max_Loss_fut = Daily_Chart['Fut pnl'].min()

  Max_Profit_spot = Daily_Chart['Spot pnl'].max()
  Max_Loss_spot = Daily_Chart['Spot pnl'].min()
  # Average PnL
  Total_no_of_trades = trades["pnl"].count()
  Total_no_of_days = Daily_Chart[Daily_Chart["Daily pnl"] != 0]["Daily pnl"].count()
  Avg_Day_Net = Overall_Net / Total_no_of_days
  Avg_Day_Net_spot = Overall_Net_spot / Total_no_of_days
  Avg_Day_Net_fut = Overall_Net_fut / Total_no_of_days
  # Calculatin Win and Loss trades count
  Total_Win_Trades = Daily_Chart[Daily_Chart["Daily pnl"] > 0]["Daily pnl"].count()
  Total_Loss_Trades = Daily_Chart[Daily_Chart["Daily pnl"] < 0]["Daily pnl"].count()

  Total_Win_Trades_spot = Daily_Chart[Daily_Chart['Spot pnl'] > 0]['Spot pnl'].count()
  Total_Loss_Trades_spot = Daily_Chart[Daily_Chart["Spot pnl"] < 0]["Spot pnl"].count()
  
  Total_Win_Trades_fut = Daily_Chart[Daily_Chart['Fut pnl'] > 0]['Fut pnl'].count()
  Total_Loss_Trades_fut = Daily_Chart[Daily_Chart["Fut pnl"] < 0]["Fut pnl"].count()
  # Calculating Average profit on win days and Average loss on bad days
  Avg_Profit_win_trades = Total_profit_on_win_days / Total_Win_Trades
  Avg_Loss_bad_trades = Total_Loss_on_bad_days / Total_Loss_Trades

  Avg_Profit_win_trades_spot = Total_profit_on_win_days_spot / Total_Win_Trades_spot
  Avg_Loss_bad_trades_spot = Total_Loss_on_bad_days_spot / Total_Loss_Trades_spot

  Avg_Profit_win_trades_fut = Total_profit_on_win_days_fut / Total_Win_Trades_fut
  Avg_Loss_bad_trades_fut = Total_Loss_on_bad_days_fut / Total_Loss_Trades_fut
  # Calculating Win and Loss ratios
  Win_Ratio = Total_Win_Trades / Total_no_of_trades
  Loss_Ratio = Total_Loss_Trades / Total_no_of_trades

  Win_Ratio_spot = Total_Win_Trades_spot / Total_no_of_trades
  Loss_Ratio_spot = Total_Loss_Trades_spot / Total_no_of_trades

  Win_Ratio_fut = Total_Win_Trades_fut / Total_no_of_trades
  Loss_Ratio_fut = Total_Loss_Trades_fut / Total_no_of_trades
  # Calculating Expectancy
  Expectancy = ((Avg_Profit_win_trades / -Avg_Loss_bad_trades) * Win_Ratio) - Loss_Ratio
  Expectancy_spot = ((Avg_Profit_win_trades_spot / -Avg_Loss_bad_trades_spot) * Win_Ratio_spot) - Loss_Ratio_spot
  Expectancy_fut = ((Avg_Profit_win_trades_fut / -Avg_Loss_bad_trades_fut) * Win_Ratio_fut) - Loss_Ratio_fut
  # Calculating Expiry Info
  Expiry_Date = trades["Expiry"]
  Daily_Chart["Expiry_Date"] = pd.to_datetime(Expiry_Date, infer_datetime_format=True)
  Expiry_info = Daily_Chart[Daily_Chart.index == Daily_Chart["Expiry_Date"]]

  Expiry_Net = Expiry_info["Daily pnl"].sum()
  Expiry_Net_spot = Expiry_info['Spot pnl'].sum()
  Expiry_Net_fut = Expiry_info['Fut pnl'].sum()

  Total_no_of_expiry = Expiry_info[Expiry_info["Daily pnl"] != 0]["Daily pnl"].count()
  Total_no_of_expiry_spot = Expiry_info[Expiry_info["Spot pnl"] != 0]["Spot pnl"].count()
  Total_no_of_expiry_fut = Expiry_info[Expiry_info["Fut pnl"] != 0]["Fut pnl"].count()

  Avg_Expiry_Net = Expiry_Net / Total_no_of_expiry
  Avg_Expiry_Net_spot = Expiry_Net_spot / Total_no_of_expiry_spot
  Avg_Expiry_Net_fut = Expiry_Net_fut / Total_no_of_expiry_fut
  # Calculating Drawdown
  Roll_max = Daily_Chart["Daily Cummulative pnl"].rolling(window=Daily_Chart.size, min_periods=1).max()
  Roll_max_spot = Daily_Chart["Spot Cummulative pnl"].rolling(window=Daily_Chart.size, min_periods=1).max()
  Roll_max_fut = Daily_Chart["Fut Cummulative pnl"].rolling(window=Daily_Chart.size, min_periods=1).max()

  Daily_Drawdown = Daily_Chart["Daily Cummulative pnl"] - Roll_max
  Daily_Drawdown_spot = Daily_Chart['Spot Cummulative pnl'] - Roll_max_spot
  Daily_Drawdown_fut = Daily_Chart["Fut Cummulative pnl"] - Roll_max_fut
  
  Max_Drawdown = min(Daily_Drawdown)
  Max_Drawdown_spot = min(Daily_Drawdown_spot)
  Max_Drawdown_fut = min(Daily_Drawdown_fut)

  Return_to_MDD_Ratio = Overall_Net / Max_Drawdown
  Return_to_MDD_Ratio_spot = Overall_Net_spot / Max_Drawdown_spot
  Return_to_MDD_Ratio_fut = Overall_Net_fut / Max_Drawdown_fut

  Lot_Size = trades['Trade Type'].nunique()
  
  rep_list = []
  rep = {"Overall Profit": Overall_Net, "Avg Expiry Profit": Avg_Expiry_Net, "Avg Day Profit": Avg_Day_Net,
         "Max Profit": Max_Profit, "Max Loss": Max_Loss,
         "Total Expiries": Total_no_of_expiry, "Win%": Win_Ratio, "Loss%": Loss_Ratio,
         "Avg Profit On Win Days": Avg_Profit_win_trades, "Avg Loss On Loss Days": Avg_Loss_bad_trades,
         "Max Drawdown(MDD)": Max_Drawdown,
         "Return to MDD Ratio": Return_to_MDD_Ratio, "Expectancy": Expectancy, "0 SL/TP Hit Count": Zero_SL_HIT,
         "1 SL/TP Hit Count": First_SL_HIT,
         "2 SL/TP Hit Count": Second_SL_HIT, "Max_Winning_Streak": Max_winning_Streak,
         "Max_Losing_Streak": Max_Losing_Streak, "Lot Size": Lot_Size}
  rep = pd.DataFrame(rep, index=['Option'])
  rep_list.append(rep)

  rep_spot = {"Overall Profit": Overall_Net_spot, "Avg Expiry Profit": Avg_Expiry_Net_spot, "Avg Day Profit": Avg_Day_Net_spot,
         "Max Profit": Max_Profit_spot, "Max Loss": Max_Loss_spot,
         "Total Expiries": Total_no_of_expiry_spot, "Win%": Win_Ratio_spot, "Loss%": Loss_Ratio_spot,
         "Avg Profit On Win Days": Avg_Profit_win_trades_spot, "Avg Loss On Loss Days": Avg_Loss_bad_trades_spot,
         "Max Drawdown(MDD)": Max_Drawdown_spot,
         "Return to MDD Ratio": Return_to_MDD_Ratio_spot, "Expectancy": Expectancy_spot, "0 SL/TP Hit Count": Zero_SL_HIT,
         "1 SL/TP Hit Count": First_SL_HIT,
         "2 SL/TP Hit Count": Second_SL_HIT, "Max_Winning_Streak": Max_winning_Streak,
         "Max_Losing_Streak": Max_Losing_Streak, "Lot Size": Lot_Size}
  rep_spot = pd.DataFrame(rep_spot, index=['Spot'])
  rep_list.append(rep_spot)

  rep_fut = {"Overall Profit": Overall_Net_fut, "Avg Expiry Profit": Avg_Expiry_Net_fut, "Avg Day Profit": Avg_Day_Net_fut,
         "Max Profit": Max_Profit_fut, "Max Loss": Max_Loss_fut,
         "Total Expiries": Total_no_of_expiry_fut, "Win%": Win_Ratio_fut, "Loss%": Loss_Ratio_fut,
         "Avg Profit On Win Days": Avg_Profit_win_trades_fut, "Avg Loss On Loss Days": Avg_Loss_bad_trades_fut,
         "Max Drawdown(MDD)": Max_Drawdown_fut,
         "Return to MDD Ratio": Return_to_MDD_Ratio_fut, "Expectancy": Expectancy_fut, "0 SL/TP Hit Count": Zero_SL_HIT,
         "1 SL/TP Hit Count": First_SL_HIT,
         "2 SL/TP Hit Count": Second_SL_HIT, "Max_Winning_Streak": Max_winning_Streak,
         "Max_Losing_Streak": Max_Losing_Streak, "Lot Size": Lot_Size}
  rep_fut = pd.DataFrame(rep_fut, index=['Future'])
  rep_list.append(rep_fut)

  report = pd.concat(rep_list)
  return report


def WeeklyBreakDown(Daily_Chart):
  # Daily_Chart["Date"] = pd.to_datetime(Daily_Chart["Date"])
  # Daily_Chart = Daily_Chart.set_index("Date")
  weeklybreakdown = Daily_Chart.resample('W-Fri')[['Daily pnl', 'Spot pnl', 'Fut pnl']].sum()
  
  return weeklybreakdown

def MonthlyBreakDown(Daily_Chart):
  Daily_Chart.sort_values(['Year', 'Month'])
  Monthly_BreakDown = Daily_Chart.groupby(['Year', 'Month'])[['Daily pnl', 'Spot pnl', 'Fut pnl']].sum()
  return Monthly_BreakDown

  # y = Daily_Chart.groupby("Year")
  # for key in y:
  #   p = y.get_group(key).groupby("Month")["Daily pnl"].sum()
  #   Month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
  #                  'November', 'December']

  #   file = open(filename, 'w')
  #   file.write("Yearly BreakDown For Months\n\n")
  #   file.write(str(key) + '\n\n')
  #   p = p.reindex(Month_order, axis=0)
  #   file.write(str(p) + "\n\n")
  # f = Daily_Chart.groupby("Month")["Daily pnl"].sum()
  # Month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
  #                'November', 'December']
  # f = f.reindex(Month_order, axis=0)
  # file.write('Total BreakDown For Months\n\n')
  # file.write(str(f) + "\n\n")
  # file.close()


def DayOfWeek(Daily_Chart):
  Daily_Chart.sort_values(['DayOfWeek'])
  dayofweek = Daily_Chart.groupby(['DayOfWeek', 'Year'])[['Daily pnl', 'Spot pnl', 'Fut pnl']].sum()
  return dayofweek
  
  # a = "DayOfWeek\n"
  # file = open(filename, 'w')
  # y = Daily_Chart.groupby("Year")
  # for key, item in y:
  #   r = y.get_group(key).groupby("DayOfWeek")['Daily pnl'].sum()
  #   Week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  #   r = r.reindex(Week_order, axis=0)
  #   file.write(a + '\n\n')
  #   file.write(str(key) + '\n\n')
  #   file.write(str(r) + "\n\n")
  # g = Daily_Chart.groupby("DayOfWeek")["Daily pnl"].sum()
  # Week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  # g = g.reindex(Week_order, axis=0)
  # file.write("Total Breakdown for Months\n\n")
  # file.write(str(g) + '\n\n')
  # file.close()