import definitions as defs
import glob, os
import pandas as pd
import functools


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

# This function converts csv files to pickle files and takes the csv folder path and pickle folder path as arguments
def CsvToPickle(csv_folder_path, pickle_folder_path):
  files = glob.glob(os.path.join(csv_folder_path, 'Data*.csv'))
  for file in files:
      filename = os.path.split(file)[1]
      filename = filename[:len(filename)-4]
      df = pd.read_csv(file)
      df.to_pickle(pickle_folder_path + "/"+ filename + ".pkl")

# This function takes spot data and checks if every timestamp is available or not
def CheckTimeContinuity(df):
  timerange = pd.date_range("09:15", "15:29", freq="1min").time
  try:
    df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
  except:
    pass
  spottime = df['datetime'].dt.time.tolist()
  if functools.reduce(lambda x,y : x and y , map(lambda p, q : p==q, timerange, spottime ), True):
    print("All time stamps are available")
  else:
    timestamps_not_available = []
    for t in range(len(timerange)):
      if timerange[t] not in spottime:
        timestamps_not_available.append(timerange[t])
    print("These timestamps are missing = ", timestamps_not_available)

# This function adds replaces 9:00 with 9:59 and changes any duplicate values to the required timestamp comparing to the defined timerange
def EnsureTimeContinuity(df):
  df = df[df.symbol=="BANKNIFTY"]
  try:
    df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
  except:
    pass
  date = df['datetime'].dt.date.iloc[0]
  start = str(date) + " 9:15"
  end = str(date) + " 15:29"  
  datetimerange = pd.date_range(start, end, freq="1min")
  df['datetimerange'] = datetimerange
  mask = df.duplicated('datetime')
  df.loc[mask, 'datetime'] = df.loc[mask, 'datetimerange']
  custom_date = str(date) + " 09:00:00"
  replaced_date = str(date) + " 09:59:00"
  df['datetime'] = df['datetime'].replace([custom_date], replaced_date)  
  return df

  





