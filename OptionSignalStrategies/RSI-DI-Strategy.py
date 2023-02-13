import datetime
from pathlib import Path
import atomic as atom
import definitions as defs
import pandas as pd
import datetime

from ta.volatility import BollingerBands
from ta.trend import MACD
from ta.momentum import RSIIndicator
from ta.trend import IchimokuIndicator
from ta.trend import EMAIndicator
from ta.trend import SMAIndicator
from ta.trend import ADXIndicator
from ta.volatility import KeltnerChannel

def OPDataExists(date):
  Banknifty_Path = "../../NIFTYOptionsData/OptionsData/Banknifty/"
  Nifty_Path = "../../NIFTYOptionsData/OptionsData/Nifty/"
  date_string = date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(NPath)
  my_fileBN = Path(BNPath)
  # print("Working on file - "+date_string)
  if my_fileN.exists() and my_fileBN.exists():
    return True
  else:
    return False

def getOPData(date, EnterTime, symbol):
  Banknifty_Path = "../../NIFTYOptionsData/OptionsData/Banknifty/"
  Nifty_Path = "../../NIFTYOptionsData/OptionsData/Nifty/"
  date_string = date.strftime("%Y/Data%Y%m%d.csv")
  BNPath = Banknifty_Path + date_string
  NPath = Nifty_Path + date_string
  my_fileN = Path(NPath)
  my_fileBN = Path(BNPath)
  delta = 0
  # print("Working on file - "+date_string)
  if my_fileN.exists() and my_fileBN.exists():
    masterdfN = atom.LoadDF(NPath)
    masterdfBN = atom.LoadDF(BNPath)
    if (symbol == "N"):
      masterdf = masterdfN
      sym = defs.N
    else:
      masterdf = masterdfBN
      sym = defs.BN
  spotdata = atom.GetSpotData(masterdf, sym)
  for s in range(len(spotdata)):
    currentcandle = spotdata.iloc[s]
    if currentcandle.name.time() == EnterTime:
      exp = atom.GetExpiry(masterdf, sym)
      if sym == defs.N:
        cst = currentcandle["open"]
        cst = int(round(cst / 50, 0) * 50)
      elif sym == defs.BN:
        cst = currentcandle["open"]
        cst = int(round(cst / 100, 0) * 100)
      opdfCE = masterdf[masterdf['symbol'] == sym + exp + str(cst + delta) + "CE"]
      opdfPE = masterdf[masterdf['symbol'] == sym + exp + str(cst - delta) + "PE"]
      break
  return (opdfCE, opdfPE)


# Conditions with RSI
def LongEnterConditionRSIDI(s, opdata, longRSIThresh, ADXThresh):
  if (opdata["rsi"][s] < longRSIThresh) and (opdata["rsi"][s] > opdata["rsi"][s - 1]) and (
          opdata["diplus"][s] > opdata["diminus"][s]):
    return True
  else:
    return False


def ShortEnterConditionRSIDI(s, opdata, shortRSIThresh, ADXThresh):
  if (opdata["rsi"][s] > shortRSIThresh) and (opdata["rsi"][s] < opdata["rsi"][s - 1]) and (
          opdata["diminus"][s] > opdata["diplus"][s]):  # and (stock["adx"][s] > ADXThresh):
    return True
  else:
    return False


def LongExitConditionRSIDI(s, opdata, longposition, longRSIThresh, SLPc):
  # Exit Condition based on longexit
  if (opdata["rsi"][s] > longRSIThresh) or (opdata["diplus"][s] < opdata["diminus"][s]):
    return True
  elif (opdata["close"][s] - longposition["Buy Price"]) < -1 * SLPc * opdata["close"][s]:
    return True
  else:
    return False


def ShortExitConditionRSIDI(s, opdata, shortposition, shortRSIThresh, SLPc):
  # Exit Condition based on longexit
  if (opdata["rsi"][s] < shortRSIThresh) or (opdata["diminus"][s] < opdata["diplus"][s]):
    return True
  elif (shortposition["Sell Price"] - opdata["close"][s]) < -1 * SLPc * opdata["close"][s]:
    return True
  else:
    return False

def SingleDayCEBuy(opdfCE, lotsize):
  longRSIThresh = 70
  ADXThresh = 30
  longpositions = []
  longposition = {}
  SLPc = 1
  win = 20
  count = 0
  LongActive = False
  TotalPNL = 0
  Rsi = RSIIndicator(opdfCE['close'], window=win)
  opdfCE["rsi"] = Rsi.rsi()
  Adx = ADXIndicator(opdfCE['high'], opdfCE['low'], opdfCE['close'], window=win)
  opdfCE["adx"] = Adx.adx()
  opdfCE["diplus"] = Adx.adx_pos()
  opdfCE["diminus"] = Adx.adx_neg()
  opdfCE = opdfCE.dropna()
  MinVal = -5
  for s in range(len(opdfCE)):
    count = count + 1
    if (count < len(opdfCE)) and (s > 0):
      if (LongEnterConditionRSIDI(s, opdfCE, longRSIThresh, ADXThresh)) and not LongActive:
        longposition["Buy Time"] = opdfCE["time"][s + 1]
        longposition["Buy Price"] = opdfCE["open"][s + 1]
        longposition["Date"] = opdfCE["date"][s + 1]
        LongActive = True
      if LongActive and LongExitConditionRSIDI(s, opdfCE, longposition, longRSIThresh, SLPc):
        longposition["Sell Time"] = opdfCE["time"][s + 1]
        longposition["Sell Price"] = opdfCE["open"][s + 1]
        longposition["PNL"] = longposition["Sell Price"] - longposition["Buy Price"]
        TotalPNL = TotalPNL + longposition["PNL"]
        longpositions.append(longposition)
        LongActive = False
        longposition = {}
      if LongActive:
        if TotalPNL + (opdfCE["open"][s + 1] - longposition["Buy Price"]) < MinVal:
          longposition["Sell Time"] = opdfCE["time"][s + 1]
          longposition["Sell Price"] = opdfCE["open"][s + 1]
          longposition["PNL"] = longposition["Sell Price"] - longposition["Buy Price"]
          TotalPNL = TotalPNL + longposition["PNL"]
          longpositions.append(longposition)
          break
      if TotalPNL < MinVal:
        break
  longpos = pd.DataFrame(longpositions)
  return (longpos, TotalPNL*lotsize)


def SingleDayPEBuy(opdfPE, lotsize):
  longRSIThresh = 70
  ADXThresh = 30
  longpositions = []
  longposition = {}
  SLPc = 1
  win = 20
  count = 0
  LongActive = False
  TotalPNL = 0
  MinVal = -5
  Rsi = RSIIndicator(opdfPE['close'], window=win)
  opdfPE["rsi"] = Rsi.rsi()
  Adx = ADXIndicator(opdfPE['high'], opdfPE['low'], opdfPE['close'], window=win)
  opdfPE["adx"] = Adx.adx()
  opdfPE["diplus"] = Adx.adx_pos()
  opdfPE["diminus"] = Adx.adx_neg()
  opdfPE = opdfPE.dropna()

  for s in range(len(opdfPE)):
    count = count + 1
    if (count < len(opdfPE)) and (s > 0):
      if (LongEnterConditionRSIDI(s, opdfPE, longRSIThresh, ADXThresh)) and not LongActive:
        longposition["Buy Time"] = opdfPE["time"][s + 1]
        longposition["Buy Price"] = opdfPE["open"][s + 1]
        LongActive = True
      if LongActive and LongExitConditionRSIDI(s, opdfPE, longposition, longRSIThresh, SLPc):
        longposition["Sell Time"] = opdfPE["time"][s + 1]
        longposition["Sell Price"] = opdfPE["open"][s + 1]
        longposition["PNL"] = longposition["Sell Price"] - longposition["Buy Price"]
        TotalPNL = TotalPNL + longposition["PNL"]
        longpositions.append(longposition)
        LongActive = False
        longposition = {}
      if LongActive:
        if TotalPNL + (opdfPE["open"][s + 1] - longposition["Buy Price"]) < MinVal:
          longposition["Sell Time"] = opdfPE["time"][s + 1]
          longposition["Sell Price"] = opdfPE["open"][s + 1]
          longposition["PNL"] = longposition["Sell Price"] - longposition["Buy Price"]
          TotalPNL = TotalPNL + longposition["PNL"]
          longpositions.append(longposition)
          break
      if TotalPNL < MinVal:
        break
  longpos = pd.DataFrame(longpositions)
  return (longpos, TotalPNL*lotsize)

EnterTime = datetime.time(9,16)
symbol = "N"
lotsize = 50

def RunStrategy(start_date, end_date):
  delta = datetime.timedelta(days=1)
  TotalPNL = 0
  CallPNLVec = pd.DataFrame()
  PutPNLVec = pd.DataFrame()
  while start_date <= end_date:
    if OPDataExists(start_date):
      (opdfCE, opdfPE) = getOPData(start_date, EnterTime, symbol)
      (longposCE, TotalPNLCE) = SingleDayCEBuy(opdfCE, lotsize)
      (longposPE, TotalPNLPE) = SingleDayPEBuy(opdfPE, lotsize)
      TotalPNL = TotalPNL + TotalPNLCE + TotalPNLPE
      CallPNLVec = CallPNLVec.append({"Date": start_date, "PNL": TotalPNLCE}, ignore_index=True)
      PutPNLVec = PutPNLVec.append({"Date": start_date, "PNL": TotalPNLPE}, ignore_index=True)
      print("Date: " + str(start_date) + ", Call PNL: " + str(TotalPNLCE) + ", Put PNL: " + str(TotalPNLPE) + ", Total PNL: " + str(TotalPNL))
    start_date += delta
  return (TotalPNL, CallPNLVec, PutPNLVec)

starttime = datetime.date(2022, 1, 1)
endtime = datetime.date(2022, 9, 30)
(TotalPNL, CallPNLVec, PutPNLVec) = RunStrategy(starttime, endtime)

#date = datetime.date(2022, 3, 30)
#(opdfCE, opdfPE) = getOPData(date, EnterTime, symbol)
#(longposCE, TotalPNLCE) = SingleDayCEBuy(opdfCE, lotsize)
#(longposPE, TotalPNLPE) = SingleDayPEBuy(opdfPE, lotsize)
#print(longposCE)
#print(longposPE)
#print(TotalPNLCE)
#print(TotalPNLPE)
