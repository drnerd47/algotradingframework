import datetime
import pandas as pd
from pathlib import Path
import time

def Report(trades):

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

def PlaceStrategy(df, currentcandle, config, positions, td):
  print("Placing Strategy!")
  exp = df.iloc[0]['symbol'][9:16] # [5:12] for nifty, [9:16] for banknifty
  cst = currentcandle['open']
  cst = int(round(cst/100, 0)*100)
  for pos in positions:
    opdf = df[df['symbol'] == config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"]]
    # print(config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"])
    if currentcandle.name in opdf.index:
      price = opdf.loc[currentcandle.name]["open"]
      tdcurr = {"EnterPrice": price, "Position":pos, "OpData": df[df['symbol'] == config["symbol"] + exp + str(cst + pos["Delta"]) + pos["Type"]],
                "Entertime": currentcandle.name.time(), "Qty": 25*pos["LotSize"], "date" : currentcandle.name.date(),
                "SLCond": price + pos["Buy/Sell"]*price*pos["SLPc"]/100,
                "Active": True, "Strike": cst + pos["Delta"], "symbol":df.iloc[0]['symbol']}
      td.append(tdcurr)
  return td

def CheckStopLoss(config, td, trades, currentcandle):
  for t in td :
    trade = {}
    if currentcandle.name in t['OpData'].index:
      if t["OpData"].loc[currentcandle.name]['high'] >= t['SLCond'] and t['Active'] :
        if (config["SquareOff"] == 1):

          Str = ""
          if (t["Position"]["Buy/Sell"] == -1):
            Str = "Buy "
          else:
            Str = "Sell "
          Str = Str + t["Position"]["Type"]
          exitprice = t["SLCond"]
          enterprice = t['EnterPrice']
          trade = {'EnterPrice': enterprice, 'ExitPrice': exitprice, 'ExitTime': currentcandle.name.time(),
                  'Reason': "SL HIT", 'Trade Type': Str, "pnl": (enterprice - exitprice)*t["Position"]["Buy/Sell"]*t["Qty"],
                  "date" : t["date"], "symbol":t["symbol"]}
          t["Active"] = False
          trades = trades.append(trade, ignore_index = True)
        else:
          # Square off the Leg which triggered the Stop Loss!
          Str = ""
          if (t["Position"]["Buy/Sell"] == -1):
            Str = "Buy "
          else:
            Str = "Sell "
          Str = Str + t["Position"]["Type"]
          exitprice = t["SLCond"]
          enterprice = t['EnterPrice']
          trade = {'EnterPrice': enterprice, 'ExitPrice': exitprice, 'ExitTime': currentcandle.name.time(),
                  'Reason': "SL HIT", 'Trade Type': Str, "pnl": (enterprice - exitprice)*t["Position"]["Buy/Sell"]*t["Qty"],
                  "date" : t["date"], "symbol":t["symbol"]}
          t["Active"] = False
          trades = trades.append(trade, ignore_index = True)
          # Squaprre off all other Legs
          for tother in td:
            if (tother != t):
              Str = ""
              if (tother["Position"]["Buy/Sell"] == -1):
                Str = "Buy "
              else:
                Str = "Sell "
              Str = Str + tother["Position"]["Type"]
              exitprice = tother["OpData"].loc[currentcandle.name]['close']
              enterprice = tother['EnterPrice']
              trade = {'EnterPrice': enterprice, 'ExitPrice': exitprice, 'ExitTime': currentcandle.name.time(),
                      'Reason': "SL SQ OFF", 'Trade Type': Str, "pnl": (enterprice - exitprice)*t["Position"]["Buy/Sell"]*t["Qty"],
                      "date" : t["date"], "symbol":t["symbol"]}
              tother["Active"] = False
              trades = trades.append(trade, ignore_index = True)

    return trades

def SquareOffEOD(td,currentcandle,trades):
  # Square off all active legs EOD
  for t in td:
    if currentcandle.name in t['OpData'].index:
      if (t['Active']):
        Str = ""
        if (t["Position"]["Buy/Sell"] == -1):
          Str = "Buy "
        else:
          Str = "Sell "
        Str = Str + t["Position"]["Type"]
        exitprice = t["OpData"].loc[currentcandle.name]['open']
        enterprice = t['EnterPrice']
        trade = {'EnterPrice': enterprice, 'ExitPrice': exitprice, 'ExitTime': currentcandle.name.time(),
                      'Reason': "TIME UP", 'Trade Type': Str, "pnl": (enterprice - exitprice)*t["Position"]["Buy/Sell"]*t["Qty"],
                "date" : t["date"], "symbol":t["symbol"]}
        trades = trades.append(trade, ignore_index = True)
        trades["Cummulative pnl"] = trades['pnl'].cumsum()
        trades["Daily pnl"] = trades.groupby("date")["pnl"].cumsum()
        trades["Daily Cummulative pnl"] = trades['pnl'].cumsum()
        # trades["Daily pnl"][0::2] = 0
  return trades

def RunSingleDayStrategy(df, trades, config, positions):
  spotdata = df[df['symbol'] == config['symbol']]
  spotdata.head(100)
  placed = False
  td = []
  for s in range(len(spotdata)):
    currentcandle = spotdata.iloc[s]
    if currentcandle.name.time() == config["EnterTime"] and not placed:
      td = PlaceStrategy(df, currentcandle, config, positions, td)
      placed = True

    if placed:
      trades = CheckStopLoss(config, td, trades, currentcandle)
      if currentcandle.name.time() == config["ExitTime"] :
          trades = SquareOffEOD(td,currentcandle,trades)
          #trades.groupby("date")["pnl"].sum()
  return trades

def Report(trades):

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

Banknifty_Path = '/Users/rishabhiyer/Software/algotrading/NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = '/Users/rishabhiyer/Software/algotrading/NIFTYOptionsData/OptionsData/Nifty/'

start_date = datetime.date(2021, 1, 3)
end_date = datetime.date(2021, 2, 28)
delta = datetime.timedelta(days=1)

trades = pd.DataFrame()
df_list = []
while start_date <= end_date:
  date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
  currpath = Banknifty_Path + date_string
  print(currpath)
  my_file = Path(currpath)
  if my_file.exists():
    df = pd.read_csv(currpath)
    df = df.drop('datetime.1', axis=1)
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index(df['datetime'])
    df_list.append(df)
    #print(df)
    #df.info()
    #spotdata = df[df['symbol'] == 'BANKNIFTY']
    #spotdata.head(100)
    config = {"SquareOff":1,"EnterTime":datetime.time(9,30),"ExitTime":datetime.time(15,15), "symbol":"BANKNIFTY"}
    # Buy: -1, Sell: 1, Delta = 0 means ATM
    positions = [{"Type":"CE","Buy/Sell":1,"Delta":0,"SLPc":25, "LotSize":1},{"Type":"PE","Buy/Sell":1,"Delta":0,"SLPc":25, "LotSize":1}]
    trades = RunSingleDayStrategy(df, trades, config, positions)
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta

print(trades)
report = Report(trades)
print(report)