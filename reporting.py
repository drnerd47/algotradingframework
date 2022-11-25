import pandas as pd

def Report(trades):

  rep = {}
  date = trades["date"].tolist()
  reason = trades["reason"].tolist()
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

    data = shots['reason'].to_frame()
    data['start_of_streak'] = data['reason'].ne(data['reason'].shift())
    data['streak_id'] = data.start_of_streak.cumsum()
    data['streak_counter'] = data.groupby('streak_id').cumcount() + 1
    shots_with_streaks = pd.concat([shots, data['streak_counter']], axis=1)
    return shots_with_streaks

  shots = trades['reason'].to_frame()
  generate_streak_info(shots)

  Max_winning_Streak = generate_streak_info(shots)[generate_streak_info(shots)["reason"] == "Time Up"]["streak_counter"].max()
  Max_Losing_Streak = generate_streak_info(shots)[generate_streak_info(shots)["reason"] == "SL HIT"]["streak_counter"].max()

  Zero_SL_HIT = counts.count(0)
  First_SL_HIT = counts.count(1)
  Second_SL_HIT = counts.count(2)
  Total_Profit_on_win_days = trades[trades["Daily pnl"] > 0]["Daily pnl"].sum()
  Total_Loss_on_bad_days = trades[trades["Daily pnl"] < 0]["Daily pnl"].sum()
  Overall_Net = Total_Profit_on_win_days - (-Total_Loss_on_bad_days)
  Max_Profit = trades["Daily pnl"].max()
  Max_Loss = trades["Daily pnl"].min()
  Total_no_of_trades = trades["pnl"].count()
  Total_no_of_days = trades[trades["Daily pnl"] != 0]["Daily pnl"].count()
  Avg_Day_Net = Overall_Net/Total_no_of_days
  Total_no_of_win_trades = trades[trades["Daily pnl"] > 0]["Daily pnl"].count()
  Total_no_of_bad_trades = trades[trades["Daily pnl"] < 0]["Daily pnl"].count()
  Avg_Profit_win_trades = Total_Profit_on_win_days/Total_no_of_win_trades
  Avg_Loss_bad_trades = Total_Loss_on_bad_days/Total_no_of_bad_trades
  Win_Percentage_trades = '{:.1%}'.format(Total_no_of_win_trades/Total_no_of_days)
  Loss_Percentage_trades = '{:.1%}'.format(Total_no_of_bad_trades/Total_no_of_days)
  Win_Ratio = Total_no_of_win_trades / Total_no_of_trades
  Loss_Ratio = Total_no_of_bad_trades / Total_no_of_trades
  Expectancy = ((Avg_Profit_win_trades/-Avg_Loss_bad_trades)*Win_Ratio) - Loss_Ratio
  trades_op = trades['symbol'].str.slice(9, 16)
  x = pd.to_datetime(trades_op, infer_datetime_format=True)
  trades["Expiry Date"] = x
  Expiry_info = trades[trades["date"] == x]
  x = pd.to_datetime(x)
  Expiry_Net = Expiry_info["Daily pnl"].sum()
  Total_no_of_expiry = Expiry_info[Expiry_info["Daily pnl"] !=0]["Daily pnl"].count()
  Avg_Expiry_Net = Expiry_Net/Total_no_of_expiry
  Max_Drawdown = trades["Daily Cummulative pnl"].min()
  Return_to_MDD_Ratio = Overall_Net/Max_Drawdown
  Lot_Size = trades["date"].value_counts()[0]

  rep =    {"Overall Profit" :Overall_Net, "Avg Expiry Profit" : Avg_Expiry_Net,"Avg Day Profit": Avg_Day_Net, "Max Profit": Max_Profit, "Max Loss" : Max_Loss,
            "Total Expiries" : Total_no_of_expiry, "Win%" : Win_Percentage_trades, "Loss%" : Loss_Percentage_trades,
            "Avg Profit On Win Days" : Avg_Profit_win_trades, "Avg Loss On Loss Days" : Avg_Loss_bad_trades , "Max Drawdown(MDD)" : Max_Drawdown,
            "Return to MDD Ratio" : Return_to_MDD_Ratio, "Expectancy" : Expectancy, "0 SL/TP Hit Count" : Zero_SL_HIT ,"1 SL/TP Hit Count" : First_SL_HIT,
            "2 SL/TP Hit Count" : Second_SL_HIT, "Max_Winning_Streak" : Max_winning_Streak, "Max_Losing_Streak" : Max_Losing_Streak, "Lot Size" : Lot_Size}
  report = pd.DataFrame(rep, index=[0])
  return report

def WeeklyBreakdown(trades):
  x = trades.set_index('date')
  y = x.resample("W-Fri")["Daily pnl"].sum()
  Weekly_BreakDown = pd.DataFrame(y, columns=["Daily pnl"])
  Weekly_BreakDown['Week Count'] = ["Week" + "-" + str(i) for i in range(1, len(Weekly_BreakDown) + 1)]
  return Weekly_BreakDown

def MonthlyBreakDown(trades):
  x = trades.groupby("Month")
  y = trades.groupby("Year")
  a = print("Yearly BreakDown For Month","\n")
  for key, item in y:
    p = y.get_group(key).groupby("Month")['Daily pnl'].sum()
    Month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    p = p.reindex(Month_order, axis=0)
    b = print(key,"\n")
    c = print(p,"\n\n")
  e = print("Total of Monthly BreakDown","\n\n")
  f = trades.groupby("Month")["Daily pnl"].sum()
  Month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  f = f.reindex(Month_order, axis=0)
  f = print(f,"\n")
  repa = {a,b,c,e,f}
  return repa

def DayOfWeek(trades):
  y = trades.groupby("Year")
  z = trades.groupby("DayOfWeek")
  a = print("Yearly BreakDown For Day Of Week","\n")
  for key, item in y:
    r = y.get_group(key).groupby("DayOfWeek")['Daily pnl'].sum()
    Week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    r = r.reindex(Week_order, axis=0)
    b = print(key,"\n")
    d = print(r,"\n\n")
  e = print("Total of Day of Week BreakDown","\n\n")
  g = trades.groupby("DayOfWeek")["Daily pnl"].sum()
  Week_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  g = g.reindex(Week_order, axis=0)
  g = print(g,"\n")
  repa = {a,b,d,e,g}
  return repa
