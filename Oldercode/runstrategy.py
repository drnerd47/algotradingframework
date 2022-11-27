import datetime
import pandas as pd
from pathlib import Path
import time

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
      tic = time.perf_counter()
      td = PlaceStrategy(df, currentcandle, config, positions, td)
      toc = time.perf_counter()
      print(f"Time taken by Place Strategy is {toc - tic:0.4f} seconds")

      placed = True

    if placed:
      tic = time.perf_counter()
      trades = CheckStopLoss(config, td, trades, currentcandle)
      toc = time.perf_counter()
      print(f"Time taken by Check Stop Loss is {toc - tic:0.4f} seconds")
      if currentcandle.name.time() == config["ExitTime"] :
          trades = SquareOffEOD(td,currentcandle,trades)
          #trades.groupby("date")["pnl"].sum()
  return trades

Banknifty_Path = '/Users/rishabhiyer/Software/algotrading/NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = '/Users/rishabhiyer/Software/algotrading/NIFTYOptionsData/OptionsData/Nifty/'

start_date = datetime.date(2022, 1, 3)
end_date = datetime.date(2022, 1, 10)
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
    tic = time.perf_counter()
    trades = RunSingleDayStrategy(df, trades, config, positions)
    toc = time.perf_counter()
    print(f"Time taken is {toc - tic:0.4f} seconds")
  else:
    print("No data for " + start_date.strftime("%Y-%m-%d"))
  start_date += delta