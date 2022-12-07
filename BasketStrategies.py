import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import positionconfigs as posconfig
import generalconfigs as genconfig

import warnings
warnings.filterwarnings("ignore")

Banknifty_Path = '../NIFTYOptionsData/OptionsData/Banknifty/'
Nifty_Path = '../NIFTYOptionsData/OptionsData/Nifty/'

strategytypes = {"IntraDayN": 0, "IntraDayBN": 1, "IntradayNRE": 2, "IntradayBNRE": 3, "ExpiryBN": 4, "ExpiryN": 5, "NextDayBNMW": 6, "NextDayNMW": 7,
                 "NextDayBNF": 8, "NextDayNF": 9, "IntradaySA": 10, "ExpirySA": 11, "NextDaySA": 12}
def RunStrategy(strattypes):
    if (strattypes == strategytypes["IntraDayN"]):
        generalconfig = genconfig.generalconfigIntradayN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
    elif (strattypes == strategytypes["IntraDayBN"]):
        generalconfig = genconfig.generalconfigIntradayBN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
    elif (strattypes == strategytypes["IntradayNRE"]):
        generalconfig = genconfig.generalconfigIntradayREN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
    elif (strattypes == strategytypes["IntradayBNRE"]):
        generalconfig = genconfig.generalconfigIntradayREBN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
    elif (strattypes == strategytypes["ExpiryBN"]):
        generalconfig = genconfig.generalconfigExpiryBN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
    elif (strattypes == strategytypes["ExpiryN"]):
        generalconfig = genconfig.generalconfigExpiryN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
    elif (strattypes == strategytypes["NextDayBNMW"]):
        generalconfig = genconfig.generalconfigNextDayBNMW
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
    elif (strattypes == strategytypes["NextDayNMW"]):
        generalconfig = genconfig.generalconfigNextDayNMW
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
    elif (strattypes == strategytypes["NextDayBNF"]):
        generalconfig = genconfig.generalconfigNextDayBNF
        positionconfig = posconfig.positionconfigLongStraddle
        intraday = False
        Arb = False
    elif (strattypes == strategytypes["NextDayNF"]):
        generalconfig = genconfig.generalconfigNextDayNF
        positionconfig = posconfig.positionconfigLongStraddle
        intraday = False
        Arb = False
    elif (strattypes == strategytypes["IntradaySA"]):
        generalconfig = [genconfig.generalconfigIntradayBN, genconfig.generalconfigIntradayN]
        positionconfig = posconfig.positionconfitStatArbStraddle
        intraday = True
        Arb = True
    elif (strattypes == strategytypes["ExpirySA"]):
        generalconfig = [genconfig.generalconfigExpiryBN, genconfig.generalconfigExpiryN]
        positionconfig = posconfig.positionconfitStatArbStraddle
        intraday = False
        Arb = True
    elif (strattypes == strategytypes["NextDaySA"]):
        generalconfig = [genconfig.generalconfigNextDayBNMW, genconfig.generalconfigNextDayNMW]
        positionconfig = posconfig.positionconfitStatArbStraddle
        intraday = False
        Arb = True

    trade = pd.DataFrame()
    trades = pd.DataFrame()
    positions = []
    positions1 = []
    positions2 = []
    start_date = datetime.date(2022, 1, 3)
    end_date = datetime.date(2022, 2, 28)
    delta = datetime.timedelta(days=1)

    while start_date <= end_date:
        trade = pd.DataFrame()
        date_string = start_date.strftime("%Y/Data%Y%m%d.csv")
        BNPath = Banknifty_Path + date_string
        NPath = Nifty_Path + date_string
        my_fileN = Path(NPath)
        my_fileBN = Path(BNPath)
        if my_fileN.exists() and my_fileBN.exists():
            masterdfN = atom.LoadDF(NPath)
            masterdfBN = atom.LoadDF(BNPath)
            if (Arb == False):
                if (generalconfig["symbol"] == defs.BN):
                    masterdf = masterdfBN
                elif (generalconfig["symbol"] == defs.N):
                    masterdf = masterdfN
                if (intraday == True):
                    trade = strategies.IntraDayStrategy(masterdf, generalconfig, positionconfig)
                else:
                    (trade, positions) = strategies.MultiDayStrategy(masterdf, positions, generalconfig, positionconfig)
            else:
                if (intraday == True):
                    trade1 = strategies.IntraDayStrategy(masterdfBN, generalconfig[0], positionconfig[0])
                    trade2 = strategies.IntraDayStrategy(masterdfN, generalconfig[1], positionconfig[1])
                    trade = trade.append(trade1)
                    trade = trade.append(trade2)
                else:
                    (trade1, positions1) = strategies.MultiDayStrategy(masterdfBN, positions1, generalconfig[0], positionconfig[0])
                    (trade2, positions2) = strategies.MultiDayStrategy(masterdfN, positions2, generalconfig[1], positionconfig[1])
                    trade = trade.append(trade1)
                    trade = trade.append(trade2)
            if (len(trade) > 0):
                trades = trades.append(trade)
        start_date += delta

    trades['date'] = pd.to_datetime(trades["date"])
    trades = trades.reset_index()
    trades = trades.drop(["index"],axis = 1)
    Daily_Chart = rep.GetDailyChart(trades)
    weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
    weeklyreport = weeklyreport.reset_index(drop=True)
    return (Daily_Chart["Daily pnl"], weeklyreport["Daily pnl"])

dailyArr = pd.DataFrame()
weeklyArr = pd.DataFrame()
for i in range(13):
    print("Running Strategy " + str(i))
    (daily, weekly) = RunStrategy(strattypes=i)
    dailyArr.append(daily)
    weeklyArr.append(weekly)