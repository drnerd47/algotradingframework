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

def get_RSIADXconfig_space_directional():
    cs = sp.Space()
    window = sp.Int("window", 10, 20, q=2, default_value=14)
    SL = sp.Int("SL", 0, 1, default_value=1)
    #Target = sp.Int("Target", 0, 1, default_value=1)
    SLPc = sp.Int("SLPc", 15, 50, q=5, default_value=20)
    #TargetPc = sp.Int("TargetPc", 40, 80, q=5, default_value=70)
    Resample = sp.Int("Resample", 2, 10, q=1, default_value=3)
    #Delta = sp.Int("Delta", 0, 1500, q=100, default_value=0)
    cs.add_variables([SL, SLPc, window, Resample])
    #cs.add_variables([TBull1, TBear1, TBull2, TBear2, SL, SLPc, Target, TargetPc, window1, window2, Resample, rolling, reenter, Delta])
    return cs


def get_objective_function(config):
    Banknifty_Path = "../NIFTYOptionsData/OptionsData/Banknifty/"
    Nifty_Path = "../NIFTYOptionsData/OptionsData/Nifty/"
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 12, 31)
    delta = datetime.timedelta(days=1)
    Resample = config['Resample']
    window = config['window']
    SLPc = config['SLPc']
    SL = config['SL']

    (TIconfig, generalconfig, positionconfig) = GetConfigs.GetRSIADXconfigsPB(defs.BUY, defs.BN, 0, Resample, 60, 40, SL, SLPc, defs.NO, 70, 20, 20,
                                                                    defs.NO, defs.YES, window, defs.YES, defs.NO)
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
space = get_RSIADXconfig_space_directional()
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