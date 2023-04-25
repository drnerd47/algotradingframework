import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import directional as direc
import GetConfigs
import datetime
import time

def RunDirectionalStrategy(start_date, end_date, approach, config, Banknifty_Path, Nifty_Path, Finnifty_Path):
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
  data = direc.getTIIndicatorData(start_date, end_date, Nifty_Path, Banknifty_Path, Finnifty_Path, generalconfig, TIconfig)
  delta = datetime.timedelta(days=1)
  trade = pd.DataFrame()
  trades = pd.DataFrame()

  while start_date <= end_date:
    date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
    BNPath = Banknifty_Path + date_string
    NPath = Nifty_Path + date_string
    FNPath = Finnifty_Path + date_string
    my_fileN = Path(NPath)
    my_fileBN = Path(BNPath)
    my_fileFN = Path(FNPath)
    # print("Working on file - "+date_string)
    if generalconfig['symbol'] == defs.BN and my_fileBN.exists() :
      masterdfBN = atom.LoadDF(BNPath)
      trade = strategies.DirectionalStrategy(data, masterdfBN, generalconfig, positionconfig, TIconfig, start_date)

    if generalconfig['symbol'] == defs.N and my_fileN.exists() :
      masterdfN = atom.LoadDF(NPath)
      trade = strategies.DirectionalStrategy(data, masterdfN, generalconfig, positionconfig, TIconfig, start_date)
    
    if generalconfig['symbol'] == defs.FN and my_fileFN.exists() :
      masterdfFN = atom.LoadDF(FNPath)
      trade = strategies.DirectionalStrategy(data, masterdfFN, generalconfig, positionconfig, TIconfig, start_date)

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

def RunIntradayStrategy(start_date, end_date, config, Banknifty_Path, Nifty_Path, Finnifty_Path):
  delta = datetime.timedelta(days=1)
  trade = pd.DataFrame()
  trades = pd.DataFrame()
  
  tic = time.time()
  origDelta = config["Delta"]
  if config['symbol'] == defs.N or config['symbol'] == defs.BN :
    while start_date <= end_date:
      if start_date.weekday() == defs.THU:
        config["Delta"] = config["DeltaThu"]
      else:
        config["Delta"] = origDelta
      (generalconfig, positionconfig) = GetConfigs.GetINDStranglesConfig(config)
      date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
      BNPath = Banknifty_Path + date_string
      NPath = Nifty_Path + date_string
      my_fileN = Path(NPath)
      my_fileBN = Path(BNPath)
      runToday = (not config["OnlyThu"]) or (start_date.weekday() == defs.THU)
      if my_fileN.exists() and my_fileBN.exists() and runToday:
        masterdfN = atom.LoadDF(NPath)
        masterdfBN = atom.LoadDF(BNPath)
        if (generalconfig["symbol"] == defs.BN):
          trade, PNLTracker, PNLTrackerSumm = strategies.IntraDayStrategy(masterdfBN, generalconfig, positionconfig)
        elif (generalconfig["symbol"] == defs.N):
          trade, PNLTracker, PNLTrackerSumm = strategies.IntraDayStrategy(masterdfN, generalconfig, positionconfig)
        if (len(trade) > 0):
          trades = trades.append(trade)
          
      start_date += delta
  elif config['symbol'] == defs.FN:
    while start_date <= end_date:
      if start_date.weekday() == defs.TUE:
        config["Delta"] = config["DeltaTue"]
      else:
        config["Delta"] = origDelta
      (generalconfig, positionconfig) = GetConfigs.GetINDStranglesConfig(config)
      date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
      FNPath = Finnifty_Path + date_string
      my_fileFN = Path(FNPath)
      runToday = (not config["OnlyTue"]) or (start_date.weekday() == defs.TUE)
      if my_fileFN.exists() and runToday:
        masterdfFN = atom.LoadDF(FNPath)
        if (generalconfig["symbol"] == defs.FN):
          trade, PNLTracker, PNLTrackerSumm = strategies.IntraDayStrategy(masterdfFN, generalconfig, positionconfig)
        if (len(trade) > 0):
          trades = trades.append(trade)
      start_date += delta
  toc = time.time()
  print("Time taken to run this Strategy ", toc-tic)

  trades['date'] = pd.to_datetime(trades["date"])
  trades = trades.reset_index()
  trades = trades.drop(["index"],axis = 1)
  return trades