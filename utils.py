import definitions as defs
import glob, os
import pandas as pd


def BuyMarginCalculator(trades, symbol):
  if symbol == defs.BN :
    margin = trades.EnterPrice * defs.BNLOTSIZE
  elif symbol == defs.N :
    margin = trades.EnterPrice * defs.NLOTSIZE
  return margin.max()

def SellMarginCalculator(positiontype, numcalllegs, numputlegs, symbol):
  if (positiontype == "Naked"):
    if (symbol == defs.BN):
      singlecost = 150000
      doublecost = 180000
    elif (symbol == defs.N):
      singlecost = 125000
      doublecost = 110000
  elif (positiontype == "Hedged"):
    if (symbol == defs.BN):
      singlecost = 45000
      doublecost = 70000
    elif (symbol == defs.N):
      singlecost = 30000
      doublecost = 60000
  return min(numcalllegs, numputlegs)*doublecost + (max(numcalllegs, numputlegs) - min(numcalllegs, numputlegs))*singlecost

def CsvToPickle(csv_folder_path, pickle_folder_path):
  files = glob.glob(os.path.join(csv_folder_path, 'Data*.csv'))

  for file in files:
      filename = os.path.split(file)[1]
      filename = filename[:len(filename)-4]
      df = pd.read_csv(file)
      df.to_pickle(pickle_folder_path + "/"+ filename + ".pkl")
