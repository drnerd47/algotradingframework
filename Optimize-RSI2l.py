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
import TIconfigs
import operator
import GetConfigs
import directional as direc

import warnings
warnings.filterwarnings("ignore")

def get_RSI2config_space_directional():
    cs = sp.Space()
    #TBull1 = sp.Int("TBull1", 40, 80, q=5, default_value=60)
    #TBear1 = sp.Int("TBear1", 20, 60, q=5, default_value=40)
    #TBull2 = sp.Int("TBull2", 50, 100, q=5, default_value=90)
    #TBear2 = sp.Int("TBear2", 5, 50, q=5, default_value=10)
    window1 = sp.Int("window1", 10, 20, q=2, default_value=14)
    window2 = sp.Int("window2", 2, 8, q=2, default_value=2)
    SL = sp.Int("SL", 0, 1, default_value=1)
    #Target = sp.Int("Target", 0, 1, default_value=1)
    SLPc = sp.Int("SLPc", 15, 50, q=5, default_value=20)
    #TargetPc = sp.Int("TargetPc", 40, 80, q=5, default_value=70)
    Resample = sp.Int("Resample", 2, 10, q=1, default_value=10)
    #Delta = sp.Int("Delta", 0, 1500, q=100, default_value=0)
    cs.add_variables([SL, SLPc, window1, window2, Resample])
    #cs.add_variables([TBull1, TBear1, TBull2, TBear2, SL, SLPc, Target, TargetPc, window1, window2, Resample, rolling, reenter, Delta])
    return cs

def GetRSI2ConfigsPB(SL, Target, SLPc, TargetPc, Resample, TBull1, TBear1, TBull2, TBear2, symbol, action, rolling, reenter,
                     Delta, window1, window2, SLTGContinuous, TrailSL, MaxReEnterCounterBull, MaxReEnterCounterBear):
    if action == defs.BUY:
        callstance = defs.BULL
        putstance = defs.BEAR
    elif action == defs.SELL:
        callstance = defs.BEAR
        putstance = defs.BULL
    positionconfig = [{"Type":defs.CALL,"Action":action,"Delta":Delta, "NumLots":1,
                       "SL": SL, "Target":Target, "Stance": callstance, "SLPc": SLPc, "TargetPc": TargetPc},
                       {"Type":defs.PUT,"Action":action,"Delta":-1*Delta, "NumLots":1,
                       "SL": SL, "Target": Target, "Stance": putstance, "SLPc": SLPc, "TargetPc": TargetPc}]
    SLBool = False
    TBool = False
    if (SL == defs.YES):
        SLBool = True
    if (Target == defs.YES):
        TBool = True
    if symbol == defs.BN:
        lotsize = defs.BNLOTSIZE
    elif symbol == defs.N :
        lotsize = defs.NLOTSIZE
    generalconfig = {"symbol": symbol, "EnterTime": datetime.time(9, 15), "ExitTime": datetime.time(15, 15),
                           "Resample": Resample, "StopLoss": SLBool, "Target": TBool, "StopLossCond": "PremiumBased",
                           "TargetCond": "PremiumBased", "Slippage": defs.SLIPPAGE, "LotSize": lotsize, "Rolling": rolling, "Reenter": reenter,
                     "SLTGContinuous": SLTGContinuous, "TrailSL": TrailSL, "MaxReEnterCounterBull": MaxReEnterCounterBull, "MaxReEnterCounterBear": MaxReEnterCounterBear}

    ticonfig = [{"TI": "RSI", "columnname": "RSI14", "ThreshBull": TBull1, "ThreshBear": TBear1, "Window": window1, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.lt, "BearOperator": operator.gt},
        {"TI": "RSI", "columnname": "RSI2", "Window": window2, "ThreshBull": TBull2, "ThreshBear": TBear2, "SL": defs.NO,
         "Target": defs.NO, "BullOperator": operator.lt, "BearOperator": operator.gt}]
    return (ticonfig, generalconfig, positionconfig)


def get_objective_function(config):
    Banknifty_Path = "../NIFTYOptionsData/OptionsData/Banknifty/"
    Nifty_Path = "../NIFTYOptionsData/OptionsData/Nifty/"
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 12, 31)
    delta = datetime.timedelta(days=1)
    Resample = config['Resample']
    window1 = config['window1']
    window2 = config["window2"]
    SLPc = config['SLPc']
    SL = config['SL']

    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetRSI2ConfigsPB(SL, defs.NO, SLPc, 70, Resample, 40,
                                                                    60, 10, 90, defs.BN, defs.SELL, defs.YES,
                                                                    defs.YES, 0, window1, window2,
                                                                    defs.YES, defs.NO, 5, 5)
    data = direc.getTIIndicatorData(start_date, end_date, Nifty_Path, Banknifty_Path, generalconfig, TIconfig)

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
                trade = strategies.DirectionalStrategy(data, masterdfBN, generalconfig, positionconfig, TIconfig,
                                                       start_date)
            elif (generalconfig["symbol"] == defs.N):
                trade = strategies.DirectionalStrategy(data, masterdfN, generalconfig, positionconfig, TIconfig,
                                                       start_date)
            # print(trade)
            if (len(trade) > 0):
                trades = trades.append(trade)
        # else:
        #   #print("No data for " + start_date.strftime("%Y-%m-%d"))
        start_date += delta

    # data.to_csv(Result_path + "Data_" + approach + ".csv")
    # print(trades)
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
    result['objs'] = [-1 * Overall_Net, -1 * Max_Drawdown]
    return result

from openbox import Optimizer
ref_point = [-1000,0]
space = get_RSI2config_space_directional()
opt = Optimizer(
    get_objective_function,
    space,
    num_objs=2,
    num_constraints=0,
    max_runs=50,
    surrogate_type='gp',
    acq_type='ehvi',
    acq_optimizer_type='random_scipy',
    initial_runs=10,
    init_strategy='sobol',
    ref_point=ref_point,
    time_limit_per_trial=10000,
    task_id='mo',
    random_state=1,
)
opt.run()