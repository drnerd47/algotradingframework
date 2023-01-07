import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd

def plotChart(df):
    try:
        df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
        df.set_index('datetime', inplace= True)
    except:
        pass
    # Create chart object
    fig = go.Figure()

    fig.add_trace(go.Line(
        x = df.index,
        y = df.close,
        mode = "lines",
        name = "Close"
    ))
    # Update chart layout
    fig.update_layout(xaxis_rangeslider_visible=True, xaxis_showticklabels=True, yaxis_showticklabels=True)
    # fig.update_layout(yaxis_range=[min(dfx.low), max(df.high)]) 
    fig.update_xaxes(rangebreaks=[ dict(bounds=["sat", "mon"]) , dict(bounds=[16, 9], pattern="hour")]) 
    # Plot chart
    fig.show();


def plotCandlestickChart(df, start, end):
    df = df[df.index.date >= start]
    df = df[df.index.date <= end]
    # Create chart object
    chart_df = [go.Candlestick(x=df.index, 
                                open=df['open'], 
                                high=df['high'], 
                                low=df['low'],
                                close=df['close']
                                )]
    # Load chart df
    fig = go.Figure(data=chart_df)
    # Update chart layout
    fig.update_layout(xaxis_rangeslider_visible=True, xaxis_showticklabels=True, yaxis_showticklabels=True)
    fig.update_layout(yaxis_range=[min(df.low), max(df.high)]) 
    fig.update_xaxes(rangebreaks=[ dict(bounds=["sat", "mon"]) , dict(bounds=[16, 9], pattern="hour")]) 
    # Plot chart
    fig.show();

def plotBollingerBands(df, start, end):
    df = df[df.index.date >= start]
    df = df[df.index.date <= end]
    
    plt.figure(figsize=(20,10))
    df['close'].plot(label='CLOSE PRICE',  color="black")
    df['upband'].plot(label='UPPER BAND', linestyle = '--', linewidth = 1, color="orange")
    df['lowband'].plot(label="LOWER BAND",linestyle = '--', linewidth = 1, color="orange")
    plt.legend(loc='upper left')
    plt.show()

def plotMACD(df, start, end):
    df = df[df.index.date >= start]
    df = df[df.index.date <= end]
    
    plt.figure(figsize=(20,10))
    plt.plot(df.signal, label='signal', color='red')
    plt.plot(df.MACD, label='MACD', color='green')
    plt.legend()
    plt.show()

def plotBB(df, start, end):   
    df = df[df.index.date >= start]
    df = df[df.index.date <= end]
    
    chart_df = [go.Candlestick(x=df.index, 
                                open=df['open'], 
                                high=df['high'], 
                                low=df['low'],
                                close=df['close'], showlegend=False,
                                name= 'candlestick'
                                )]
    # Load chart df
    fig = go.Figure(data=chart_df)
    # Moving Average
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['sma'],
                            line_color = 'black',
                            name = 'sma'))
    # Upper Bound
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['upband'],
                            line_color = 'gray',
                            line = {'dash': 'dash'},
                            name = 'upper band',
                            opacity = 0.5))
    # Lower Bound fill in between with parameter 'fill': 'tonexty'
    fig.add_trace(go.Scatter(x = df.index,
                            y = df['lowband'],
                            line_color = 'gray',
                            line = {'dash': 'dash'},
                            fill = 'tonexty',
                            name = 'lower band',
                            opacity = 0.5))
    # range slider; 
    fig.update(layout_xaxis_rangeslider_visible=True)
       
    fig.update_xaxes(
        rangebreaks=[ dict(bounds=["sat", "mon"]) , dict(bounds=[16, 9], pattern="hour")])  

    fig.show();

# PlotSignal function takes the signal df i.e. the df where signals are generated( spot df )
def PlotSignal(df, start, end):
    try:
        df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
        df.set_index('datetime', inplace= True)
    except:
        pass 

    df = df[df.index.date >= start]
    df = df[df.index.date <= end]      
    
    if "RSI14" and "RSI2" in df.columns:
        fig = make_subplots(rows=3, cols=1)
        
        fig.add_trace(go.Line(
        x = df.index,
        y = df.RSI14,
        mode = "lines",
        name = "RSI14"
        ), row=2, col=1)

        fig.add_trace(go.Line(
        x = df.index,
        y = df.RSI2,
        mode = "lines",
        name = "RSI2"
        ), row=3, col=1) 

    elif "RSI14" and "ADX14" in df.columns: 
        fig = make_subplots(rows=3, cols=1)
        
        fig.add_trace(go.Line(
        x = df.index,
        y = df.RSI14,
        mode = "lines",
        name = "RSI14"
        ), row=2, col=1)

        fig.add_trace(go.Line(
        x = df.index,
        y = df.ADX14,
        mode = "lines",
        name = "ADX14"
        ), row=3, col=1)

    elif "upband" and "lowband" in df.columns:
        fig = make_subplots(rows=1, cols=1)

        fig.add_trace(go.Line(
            x = df.index,
            y = df.upband,
            mode = "lines",
            name = "Upper Bollinger Band",
            marker = {'color' : 'black'}
        ), row = 1, col = 1) 
        fig.add_trace(go.Line(
            x = df.index,
            y = df.lowband,
            mode = "lines",
            name = "Lower Bollinger Band",
            marker = {'color' : 'black'}
        ), row = 1, col = 1) 
        
    else:
        fig = make_subplots(rows=1, cols=1)

    bearentry = df[df.EntrySignal == -2]
    bullentry = df[df.EntrySignal == 2]
    stoploss = df[df.ExitSignal == -1]
    target = df[df.ExitSignal == 1]
    eodsquareoff = df[df.ExitSignal == 0]      
    

    fig.add_trace(go.Line(
        x = df.index,
        y = df.close,
        mode = "lines",
        name = "Spot Close"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x = bearentry.index,
        y = bearentry.close,
        mode = "markers+text",
        name = "Bear Entry"
    ))

    fig.add_trace(go.Scatter(
        x = bullentry.index,
        y = bullentry.close,
        mode = "markers+text",
        name = "Bull Entry"
    ))

    fig.add_trace(go.Scatter(
        x = stoploss.index,
        y = stoploss.close,
        mode = "markers+text",
        name = "Stop Loss Hit"
    ))

    fig.add_trace(go.Scatter(
        x = target.index,
        y = target.close,
        mode = "markers+text",
        name = " Target Hit"
    ))

    fig.add_trace(go.Scatter(
        x = eodsquareoff.index,
        y = eodsquareoff.close,
        mode = "markers+text",
        name = "End of Day Square Off"
    ))

    #fig.update(layout_xaxis_rangeslider_visible=True)    
    fig.update_xaxes(
        rangebreaks=[ dict(bounds=["sat", "mon"]) , dict(bounds=[16, 9], pattern="hour")])
    fig.show();

# Plots Option data and takes Option data as argument
def plotOptionData(df):
    try:
        df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
        df.set_index('datetime', inplace= True)
    except:
        pass
    # Create chart object
    fig = go.Figure()

    fig.add_trace(go.Line(
        x = df.index,
        y = df.close,
        mode = "lines",
        name = "Close"
    ))
    # Update chart layout
    fig.update_layout(xaxis_rangeslider_visible=True, xaxis_showticklabels=True, yaxis_showticklabels=True)
    # fig.update_layout(yaxis_range=[min(dfx.low), max(df.high)]) 
    fig.update_xaxes(rangebreaks=[ dict(bounds=["sat", "mon"]) , dict(bounds=[16, 9], pattern="hour")]) 
    # Plot chart
    fig.show();

# input a single trade from trades file, signal data is the whole signal data df, datapath = ['Banknifty Path', 'Nifty Path']
def plotTrade(trade, signaldata, datapath):
    OpSymbol = trade['symbol']
    tradedate = trade['date']
    tradedate = pd.to_datetime(tradedate, infer_datetime_format=True).date()
    expirydate = trade['Expiry']
    expirydate = pd.to_datetime(expirydate, infer_datetime_format=True).date()
    entertime = trade['EnterTime']
    entertime = pd.to_datetime(entertime, infer_datetime_format=True).time()
    exittime = trade['ExitTime']
    exittime = pd.to_datetime(exittime, infer_datetime_format=True).time()

    symbols = ['BANKNIFTY', 'NIFTY']
    if OpSymbol[0:9] in symbols:
        symbol = OpSymbol[0:9]
    elif OpSymbol[0:5] in symbols:
        symbol = OpSymbol[0:5]

    if symbol == 'BANKNIFTY':
        path = datapath[0]
    elif symbol == 'NIFTY':
        path = datapath[1]
    
    date_path = tradedate.strftime("%Y/Data%Y%m%d.csv")
    data_path = path + date_path
    data = pd.read_csv(data_path)

    try:
        data['datetime'] = pd.to_datetime(data['datetime'], infer_datetime_format=True)
        data.set_index('datetime', inplace= True)
    except:
        pass

    spotdata = data[data.symbol == symbol]
    opdata = data[data.symbol == OpSymbol]   
    
    try:
        signaldata['datetime'] = pd.to_datetime(signaldata['datetime'], infer_datetime_format=True)
        signaldata.set_index('datetime', inplace= True)
    except:
        pass 

    df = signaldata[signaldata.index.date == tradedate]

    bearentry = df[df.EntrySignal == -2]
    bullentry = df[df.EntrySignal == 2]
    stoploss = df[df.ExitSignal == -1]
    target = df[df.ExitSignal == 1]
    eodsquareoff = df[df.ExitSignal == 0] 

    # Plotting indicators
    if "RSI14" and "RSI2" in df.columns:
        fig = make_subplots(rows=4, cols=1, subplot_titles=(symbol, OpSymbol, "RSI14", "RSI2"))
        
        fig.add_trace(go.Line(
        x = df.index,
        y = df.RSI14,
        mode = "lines",
        name = "RSI14"
        ), row=3, col=1)

        fig.add_trace(go.Line(
        x = df.index,
        y = df.RSI2,
        mode = "lines",
        name = "RSI2"
        ), row=4, col=1) 

    elif "RSI14" and "ADX14" in df.columns: 
        fig = make_subplots(rows=4, cols=1, subplot_titles=(symbol, OpSymbol, "RSI", "ADX"))
        
        fig.add_trace(go.Line(
        x = df.index,
        y = df.RSI14,
        mode = "lines",
        name = "RSI14"
        ), row=3, col=1)

        fig.add_trace(go.Line(
        x = df.index,
        y = df.ADX14,
        mode = "lines",
        name = "ADX14"
        ), row=4, col=1)

    elif "upband" and "lowband" in df.columns:
        fig = make_subplots(rows=2, cols=1)

        fig.add_trace(go.Line(
            x = df.index,
            y = df.upband,
            mode = "lines",
            name = "Upper Bollinger Band",
            marker = {'color' : 'yellow'}
        ), row = 1, col = 1) 
        fig.add_trace(go.Line(
            x = df.index,
            y = df.lowband,
            mode = "lines",
            name = "Lower Bollinger Band",
            marker = {'color' : 'yellow'}
        ), row = 1, col = 1)
    
    else:
        fig = make_subplots(rows=2, cols=1, subplot_titles=(symbol, OpSymbol), shared_xaxes=True, vertical_spacing= 0.5)

    # Plotting Option Close
    fig.add_trace(go.Line(
        x = opdata.index,
        y = opdata.close,
        mode = "lines",
        name = OpSymbol + " "+ str(tradedate) + " Close"
    ), row=2, col=1)

    # Plotting Spot Close
    fig.add_trace(go.Line(
        x = spotdata.index,
        y = spotdata.close,
        mode = "lines",
        name = symbol + " Close",
        marker = {'color' : 'black'}
    ), row=1, col=1)
    
    # Adding entry and exit points
    fig.add_trace(go.Scatter(
        x = bearentry.index,
        y = bearentry.close,
        mode = "markers+text",
        name = "Bear Entry",
        text=["Bear Entry"],
        textposition="bottom center"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x = bullentry.index,
        y = bullentry.close,
        mode = "markers+text",
        name = "Bull Entry",
        text=["Bull Entry"],
        textposition="bottom center"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x = stoploss.index,
        y = stoploss.close,
        mode = "markers+text",
        name = "Stop Loss Hit",
        text=["Stop Loss Hit"],
        textposition="bottom center"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x = target.index,
        y = target.close,
        mode = "markers+text",
        name = "Target Hit",
        text=["Target Hit"],
        textposition="bottom center"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x = eodsquareoff.index,
        y = eodsquareoff.close,
        mode = "markers+text",
        name = "End of Day Square Off",
        text=["EOD Square Off"],
        textposition="bottom center"
    ), row=1, col=1)

    fig.update_layout(
    autosize=False,
    width=1600,
    height=900,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",
)
    #fig.update(layout_xaxis_rangeslider_visible=True)    
    fig.update_xaxes(rangebreaks=[ dict(bounds=["sat", "mon"]) , dict(bounds=[16, 9], pattern="hour")])
    fig.show();



