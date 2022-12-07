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
from openbox import Optimizer
import numpy as np
import matplotlib.pyplot as plt

Banknifty_Path = '../NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = '../NIFTYOptionsData/OptionsData/nifty/'

start_date = datetime.date(2022, 1, 1)
end_date = datetime.date(2022, 8, 30)
delta = datetime.timedelta(days=1)


def get_config_space_intraday_straddle():
    cs = sp.Space()
    SquareOffSL = sp.Int("SquareOffSL", 1, 2, default_value=1)
    SquareOffTG = sp.Int("SquareOffTG", 1, 2, default_value=1)
    ReEntrySL = sp.Int("ReEntrySL", 0, 1, default_value=0)
    ReEntryTG = sp.Int("ReEntryTG", 0, 1, default_value=0)
    MaxReEnterCounterTG = sp.Int("MaxReEnterCounterTG", 1, 10, default_value=3)
    MaxReEnterCounterSL = sp.Int("MaxReEnterCounterSL", 1, 10, default_value=3)
    SL = sp.Int("SL", 0, 1, default_value=1)
    Target = sp.Int("Target", 0, 1, default_value=1)
    SLPc = sp.Int("SLPc", 5, 40, q = 5, default_value=25)
    TargetPc = sp.Int("TargetPc", 30, 70, q = 10, default_value=50)
    cs.add_variables([SquareOffSL, SquareOffTG, ReEntrySL, ReEntryTG, MaxReEnterCounterTG, MaxReEnterCounterSL, SL, Target, SLPc, TargetPc])
    return cs

def get_objective_function(config):
    Banknifty_Path = '/content/drive/MyDrive/NIFTYOptionsData/OptionsData/Banknifty/'
    Nifty_Path = '/content/drive/MyDrive/NIFTYOptionsData/OptionsData/Nifty/'
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
        my_fileN = Path(NPath)
        my_fileBN = Path(BNPath)
        if my_fileN.exists() and my_fileBN.exists():
            masterdfN = atom.LoadDF(NPath)
            masterdfBN = atom.LoadDF(BNPath)
            if (generalconfig["symbol"] == defs.BN):
                trade = strategies.IntraDayStrategy(masterdfBN, generalconfig, positionconfig)
            elif (generalconfig["symbol"] == defs.N):
                trade = strategies.IntraDayStrategy(masterdfN, generalconfig, positionconfig)
            if (len(trade) > 0):
                trades = trades.append(trade)
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
    result['objs'] = [-1*Overall_Net, -1*Max_Drawdown]
    return result

ref_point = [-1000,0]
space = get_config_space_intraday_straddle()
opt = Optimizer(
    get_objective_function,
    space,
    num_objs=2,
    num_constraints=0,
    max_runs=30,
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

# plot pareto front
pareto_front = np.asarray(opt.get_history().get_pareto_front())
if pareto_front.shape[-1] in (2, 3):
    if pareto_front.shape[-1] == 2:
        plt.scatter(pareto_front[:, 0], pareto_front[:, 1])
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
    elif pareto_front.shape[-1] == 3:
        ax = plt.axes(projection='3d')
        ax.scatter3D(pareto_front[:, 0], pareto_front[:, 1], pareto_front[:, 2])
        ax.set_xlabel('Objective 1')
        ax.set_ylabel('Objective 2')
        ax.set_zlabel('Objective 3')
    plt.title('Pareto Front')
    plt.show()
