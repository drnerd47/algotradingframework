import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import directional as direc
import GetConfigs
import datetime
import time

def RunDirectionalStrategy(start_date, end_date, approach, config, Banknifty_Path, Nifty_Path):
  if (approach == "RSI-Dual"):
    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetRSIDualConfig(config)
  elif (approach == "ST"):
    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetSTconfig(config)
  elif (approach == "BB2"):
    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetBB2Config(config)
  elif (approach == "BB1"):
    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetBB1Config(config)
  elif (approach == "RSI-ADX"):
    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetRSIADXconfig(config)
  elif (approach == "RSI2"):
    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetRSI2Config(config)
  elif (approach == "EMA"):
    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetEMAconfig(config)
  tic = time.time()
  data = direc.getTIIndicatorData(start_date, end_date, Nifty_Path, Banknifty_Path, generalconfig, TIconfig)
  delta = datetime.timedelta(days=1)
  trade = pd.DataFrame()
  trades = pd.DataFrame()

  while start_date <= end_date:
    date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
    BNPath = Banknifty_Path + date_string
    NPath = Nifty_Path + date_string
    my_fileN = Path(NPath)
    my_fileBN = Path(BNPath)
    # print("Working on file - "+date_string)
    if my_fileN.exists() and my_fileBN.exists():
      masterdfN = atom.LoadDF(NPath)
      masterdfBN = atom.LoadDF(BNPath)
      if (generalconfig["symbol"] == defs.BN):
        trade = strategies.DirectionalStrategy(data, masterdfBN, generalconfig, positionconfig, TIconfig, start_date)
      elif (generalconfig["symbol"] == defs.N):
        trade = strategies.DirectionalStrategy(data, masterdfN, generalconfig, positionconfig, TIconfig, start_date)
      #print(trade)
      if (len(trade) > 0):
        trades = trades.append(trade)
    # else:
    #   print("No data for " + start_date.strftime("%Y-%m-%d"))
    start_date += delta

  toc = time.time()
  print(" Time taken to run this strategy ", toc-tic)
  # print(trades)
  trades['date'] = pd.to_datetime(trades["date"])
  trades = trades.reset_index()
  trades = trades.drop(["index"], axis = 1)
  return (data, trades)

def RunIntradayStrategy(start_date, end_date, config, Banknifty_Path, Nifty_Path):
  (generalconfig, positionconfig) = GetConfigs.GetINDStraddlesConfig(config)
  delta = datetime.timedelta(days=1)
  trade = pd.DataFrame()
  trades = pd.DataFrame()

  while start_date <= end_date:
    date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
    BNPath = Banknifty_Path + date_string
    NPath = Nifty_Path + date_string
    my_fileN = Path(NPath)
    my_fileBN = Path(BNPath)
    print(date_string)
    if my_fileN.exists() and my_fileBN.exists():
      masterdfN = atom.LoadDF(NPath)
      masterdfBN = atom.LoadDF(BNPath)
      if (generalconfig["symbol"] == defs.BN):
        trade = strategies.IntraDayStrategy(masterdfBN, generalconfig, positionconfig)
      elif (generalconfig["symbol"] == defs.N):
        trade = strategies.IntraDayStrategy(masterdfN, generalconfig, positionconfig)
      if (len(trade) > 0):
        trades = trades.append(trade)
    else:
      print("No data for " + start_date.strftime("%Y-%m-%d"))
    start_date += delta

  toc = time.time()
  print("Time taken to run this Strategy ", toc-tic)

  trades['date'] = pd.to_datetime(trades["date"])
  trades = trades.reset_index()
  trades = trades.drop(["index"],axis = 1)
  return trades