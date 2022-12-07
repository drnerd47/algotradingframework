import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import generalconfigs as genconfigs
import positionconfigs as posconfigs
from openbox import sp
import numpy as np

Banknifty_Path = '../NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = '../NIFTYOptionsData/OptionsData/nifty/'

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 8, 30)
delta = datetime.timedelta(days=1)


def get_config_space_intraday_straddle():
    cs = sp.Space()
    SquareOffSL = sp.Int("SquareOffSL", 1, 2, default_value=1)
    SquareOffTG = sp.Int("SquareOffTG", 1, 12, default_value=1)
    # ReEntrySL = sp.Int("ReEntrySL", 0, 1, default_value=0)
    # ReEntryTG = sp.Int("ReEntryTG", 0, 1, default_value=0)
    # MaxReEnterCounterTG = sp.Int("MaxReEnterCounterTG", 1, 10, default_value=3)
    # MaxReEnterCounterSL = sp.Int("MaxReEnterCounterSL", 1, 10, default_value=3)
    ReEnterEvery = sp.Int("ReEnterEvery", 2, 30, default_value=2)
    SL = sp.Int("SL", 0, 1, default_value=1)
    Target = sp.Int("Target", 0, 1, default_value=1)
    SLPc = sp.Int("SLPc", 5, 40, q = 5, default_value=25)
    TargetPc = sp.Int("SLPc", 30, 70, q = 10, default_value=50)
    cs.add_variables([SquareOffSL, SquareOffTG, ReEnterEvery, SL, Target, SLPc, TargetPc])
    return cs

def get_objective_function(config):
    Banknifty_Path = '../NIFTYOptionsData/OptionsData/Banknifty/'
    Nifty_Path = '../NIFTYOptionsData/OptionsData/Nifty'
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 8, 30)
    delta = datetime.timedelta(days=1)
    SquareOffSL = config['SquareOffSL']
    SquareOffTG = config['SquareOffTG']
    # ReEntrySL = config['ReEntrySL']
    # ReEntryTG = config['ReEntryTG']
    # MaxReEnterCounterTG = config['MaxReEnterCounterTG']
    # MaxReEnterCounterSL = config['MaxReEnterCounterSL']
    ReEnterEvery = config['ReEnterEvery']
    SL = config['SL']
    Target = config['Target']
    SLPc = config['SLPc']
    TargetPc = config['TargetPc']
    generalconfig = genconfigs.GetGeneralConfigIntradayTime(SquareOffSL, SquareOffTG, defs.BN, ReEnterEvery)
    positionconfig = posconfigs.getStraddles(defs.SELL, SL, Target, SLPc, TargetPc)
    trade = pd.DataFrame()
    trades = pd.DataFrame()

    while start_date <= end_date:
        date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
        BNPath = Banknifty_Path + date_string
        NPath = Nifty_Path + date_string
        print(NPath)
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
    trades['date'] = pd.to_datetime(trades["date"])
    trades = trades.reset_index()
    trades = trades.drop(["index"], axis=1)
    Daily_Chart = rep.GetDailyChart(trades)
    Total_Profit_on_win_days = Daily_Chart[Daily_Chart["Daily pnl"] > 0]["Daily pnl"].sum()
    Total_Loss_on_bad_days = Daily_Chart[Daily_Chart["Daily pnl"] < 0]["Daily pnl"].sum()
    Overall_Net = Total_Profit_on_win_days - (-Total_Loss_on_bad_days)
    Roll_max = Daily_Chart["Daily Cummulative pnl"].rolling(window=Daily_Chart.size, min_periods=1).max()
    Daily_Drawdown = Daily_Chart["Daily Cummulative pnl"] - Roll_max
    Max_Drawdown = min(Daily_Drawdown)
    result = dict()
    result['objs'] = [-1*Overall_Net, Max_Drawdown]
    return result

config = {}
config['SquareOffSL'] = defs.ONELEG
config['SquareOffTG'] = defs.ONELEG
config['ReEntrySL'] = defs.NO
config['ReEntryTG'] = defs.NO
config['MaxReEnterCounterTG'] = 3
config['MaxReEnterCounterSL'] = 3
config['SL'] = defs.YES
config['Target'] = defs.NO
config['SLPc'] = 25
config['TargetPc'] = 50
config['ReEnterEvery'] = defs.YES

get_objective_function(config)

