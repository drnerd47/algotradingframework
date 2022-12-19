import datetime
import atomic as atom
import definitions as defs
from pathlib import Path
import pandas as pd
import strategies
import reporting as rep
import positionconfigs as posconfig
import generalconfigs as genconfig
import TIconfigs
import directional as direc
import os

import warnings
warnings.filterwarnings("ignore")

# Logic to define path
user = "SD"

if user == "SD":
  Root = "D:/Work/Sykes and Ray/"
  Result_path = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/"
  parent_dir = "D:/Work/Sykes and Ray/NIFTYOptionsData/OptionsData/Results/BasketStrategies/"
elif user == "RI":
  Root = "../"
  Result_path = "Results/"
  parent_dir = "BasketStrategies/"
elif user == "MS":
  Root = "Moulik's File path"
  Result_path = " Moulik's result path"
  parent_dir = " "

Banknifty_Path = Root + "NIFTYOptionsData/OptionsData/Banknifty/"
Nifty_Path = Root + "NIFTYOptionsData/OptionsData/Nifty/"


strategytypes = [ "IntraDayN", "IntraDayBN", "IntradayNRE", "IntradayBNRE", "ExpiryBN", "ExpiryN", "NextDayBNMW", "NextDayNMW", "NextDayBNF", "NextDayNF", "IntradaySA", "ExpirySA", "NextDaySA",
                "RSI-ADXNb", "RSIDualNb", "BB2Nb", "RSI-ADXBNb", "RSIDualBNb", "BB2BNb", "RSI-ADXNs", "RSIDualNs", "BB2Ns", "SupertrendNs", "RSI-ADXBNs", "RSIDualBNs", "BB2BNs", "SupertrendBNs"]



start = datetime.date(2020, 1 , 1)
end = datetime.date(2020, 12, 31)

def RunStrategy(strattypes, start, end):
    if (strattypes == "IntraDayN"):
        generalconfig = genconfig.generalconfigIntradayN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
        directional = False
    elif (strattypes == "IntraDayBN"):
        generalconfig = genconfig.generalconfigIntradayBN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
        directional = False
    elif (strattypes == "IntradayNRE"):
        generalconfig = genconfig.generalconfigIntradayREN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
        directional = False
    elif (strattypes == "IntradayBNRE"):
        generalconfig = genconfig.generalconfigIntradayREBN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = True
        Arb = False
        directional = False
    elif (strattypes == "ExpiryBN"):
        generalconfig = genconfig.generalconfigExpiryBN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
        directional = False
    elif (strattypes == "ExpiryN"):
        generalconfig = genconfig.generalconfigExpiryN
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
        directional = False
    elif (strattypes == "NextDayBNMW"):
        generalconfig = genconfig.generalconfigNextDayBNMW
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
        directional = False
    elif (strattypes == "NextDayNMW"):
        generalconfig = genconfig.generalconfigNextDayNMW
        positionconfig = posconfig.positionconfigShortStraddle
        intraday = False
        Arb = False
        directional = False
    elif (strattypes == "NextDayBNF"):
        generalconfig = genconfig.generalconfigNextDayBNF
        positionconfig = posconfig.positionconfigLongStraddle
        intraday = False
        Arb = False
        directional = False
    elif (strattypes == "NextDayNF"):
        generalconfig = genconfig.generalconfigNextDayNF
        positionconfig = posconfig.positionconfigLongStraddle
        intraday = False
        Arb = False
        directional = False
    elif (strattypes == "IntradaySA"):
        generalconfig = [genconfig.generalconfigIntradayBN, genconfig.generalconfigIntradayN]
        positionconfig = posconfig.positionconfitStatArbStraddle
        intraday = True
        Arb = True
        directional = False
    elif (strattypes == "ExpirySA"):
        generalconfig = [genconfig.generalconfigExpiryBN, genconfig.generalconfigExpiryN]
        positionconfig = posconfig.positionconfitStatArbStraddle
        intraday = False
        Arb = True
        directional = False
    elif (strattypes == "NextDaySA"):
        generalconfig = [genconfig.generalconfigNextDayBNMW, genconfig.generalconfigNextDayNMW]
        positionconfig = posconfig.positionconfitStatArbStraddle
        intraday = False
        Arb = True
        directional = False
#######################################################################################################################################
    elif (strattypes == "RSI-ADXNb"):
        generalconfig = genconfig.generalconfigNRSIADX
        positionconfig = posconfig.positionconfigsinglebuydirec
        TIconfig = TIconfigs.TIconfigRSI_ADX
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "RSIDualNb"):
        generalconfig = genconfig.generalconfigNRSIDual
        positionconfig = posconfig.positionconfigsinglebuydirecSL
        TIconfig = TIconfigs.TIconfig_RSIDual
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "BB2Nb"):
        generalconfig = genconfig.generalconfigNBB
        positionconfig = posconfig.positionconfigsinglebuydirec
        TIconfig = TIconfigs.TIconfigBB2
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "RSI-ADXBNb"):
        generalconfig = genconfig.generalconfigBNRSIADX
        positionconfig = posconfig.positionconfigsinglebuydirec
        TIconfig = TIconfigs.TIconfigRSI_ADX
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "RSIDualBNb"):
        generalconfig = genconfig.generalconfigBNRSIDual
        positionconfig = posconfig.positionconfigsinglebuydirecSL
        TIconfig = TIconfigs.TIconfig_RSIDual
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "BB2BNb"):
        generalconfig = genconfig.generalconfigBNBB
        positionconfig = posconfig.positionconfigsinglebuydirec
        TIconfig = TIconfigs.TIconfigBB2
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "RSI-ADXNs"):
        generalconfig = genconfig.generalconfigNRSIADX
        positionconfig = posconfig.positionconfigsingleselldirec
        TIconfig = TIconfigs.TIconfigRSI_ADX
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "RSIDualNs"):
        generalconfig = genconfig.generalconfigNRSIDual
        positionconfig = posconfig.positionconfigsingleselldirecSL
        TIconfig = TIconfigs.TIconfig_RSIDual
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "BB2Ns"):
        generalconfig = genconfig.generalconfigNBB
        positionconfig = posconfig.positionconfigsingleselldirec
        TIconfig = TIconfigs.TIconfigBB2
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "SupertrendNs"):
        generalconfig = genconfig.generalconfigNST
        positionconfig = posconfig.positionconfigsingleselldirecSL
        TIconfig = TIconfigs.TIconfigST
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "RSI-ADXBNs"):
        generalconfig = genconfig.generalconfigBNRSIADX
        positionconfig = posconfig.positionconfigsingleselldirec
        TIconfig = TIconfigs.TIconfigRSI_ADX
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "RSIDualBNs"):
        generalconfig = genconfig.generalconfigBNRSIDual
        positionconfig = posconfig.positionconfigsingleselldirecSL
        TIconfig = TIconfigs.TIconfig_RSIDual
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "BB2BNs"):
        generalconfig = genconfig.generalconfigBNBB
        positionconfig = posconfig.positionconfigsingleselldirec
        TIconfig = TIconfigs.TIconfigBB2
        intraday = True
        Arb = False
        directional = True
    elif (strattypes == "SupertrendBNs"):
        generalconfig = genconfig.generalconfigBNST
        positionconfig = posconfig.positionconfigsingleselldirecSL
        TIconfig = TIconfigs.TIconfigST
        intraday = True
        Arb = False
        directional = True

    trade = pd.DataFrame()
    trades = pd.DataFrame()
    positions = []
    positions1 = []
    positions2 = []

    # years = [2019, 2020, 2021, 2022]
    # for year in years:
    
    start_date = start
    end_date = end
    delta = datetime.timedelta(days=1)

    # year_path = parent_dir+str(year)    
    directory = "Strategy "+str(strattypes)
    path = os.path.join(parent_dir, directory)
    
    file = Path(path)
    if file.exists():
        pass
    else:
        os.mkdir(path)  
    
    if directional == True:
        if (generalconfig["symbol"] == defs.N):
            data = direc.getMultipledayData(start_date, end_date, generalconfig['EnterTime'], Nifty_Path, defs.N, generalconfig["Resample"])
            data = direc.getTI(data, TIconfig)
        else:
            data = direc.getMultipledayData(start_date, end_date, generalconfig['EnterTime'], Banknifty_Path, defs.BN, generalconfig["Resample"])
            data = direc.getTI(data, TIconfig)  

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

                if (intraday == True and directional == False):
                    trade = strategies.IntraDayStrategy(masterdf, generalconfig, positionconfig)
                elif (intraday == False and directional == False):
                    (trade, positions) = strategies.MultiDayStrategy(masterdf, positions, generalconfig, positionconfig)
                elif (intraday == True and directional == True):                    
                    trade = strategies.DirectionalStrategy(data, masterdf, generalconfig, positionconfig, TIconfig, start_date)
                
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
    trades.to_csv(path+"/trades.csv")
    Daily_Chart = rep.GetDailyChart(trades)
    Daily_Chart.to_csv(path+"/Daily_Chart.csv")
    weeklyreport = rep.WeeklyBreakDown(Daily_Chart)
    weeklyreport = weeklyreport.reset_index(drop=True)
    weeklyreport.to_csv(path+"/weeklyreport.csv")
    # report = rep.Report(trades, Daily_Chart)
    # report.to_csv(path + "/Report.csv")


    return (Daily_Chart["Daily pnl"], weeklyreport["Weekly pnl"])

dailyArr = pd.DataFrame()
weeklyArr = pd.DataFrame()

for strategy in strategytypes :
    print("Running Strategy " + strategy)
    (daily, weekly) = RunStrategy(strategy, start, end)
    dailyArr['Strategy ' + strategy] = daily
    dailyArr = dailyArr.fillna(0)
    weeklyArr['Strategy ' + strategy] = weekly
    weeklyArr = weeklyArr.fillna(0)

# print("\n","Daily pnl","\n",dailyArr)
# print("\n")
# print("Weekly pnl","\n",weeklyArr)
# print("\n")

# print("Weekly Correlation")
# print("\n")
weeklyCorr = weeklyArr.corr()
# print(weeklyCorr)
# print("\n")
# print("Weekly Report: Sum and Mean")
# sum specific columns
col_list = list(weeklyArr)
weeklyArr['Mean Strategy'] = weeklyArr[col_list].mean(axis=1)
weeklyArr['Sum Strategy'] = weeklyArr[col_list].sum(axis=1)

df = pd.DataFrame()
df = weeklyArr.cumsum(axis=0)
Roll_max = df.rolling(window = weeklyArr.size, min_periods=1).max()
Weekly_Drawdown = df - Roll_max
Max_Drawdown = Weekly_Drawdown.min()
weeklyArr.loc["No. of Win Weeks"] = weeklyArr[weeklyArr > 0].count()
weeklyArr.loc["No. of Bad Weeks"] = weeklyArr[weeklyArr < 0].count()
weeklyArr.loc["Max Drawdown"] = Max_Drawdown
# print("\n")
# print(weeklyArr)
# print("\n")
weeklyCorr.to_csv(Result_path+"BasketCorr.csv")
weeklyArr.to_csv(Result_path+"BasketResults.csv")

