import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import pandas as pd

def plotChart(df, start, end):
    try:
        df['datetime'] = pd.to_datetime(df['datetime'], infer_datetime_format=True)
        df.set_index('datetime', inplace= True)
    except:
        pass
    df = df[df.index.date >= start]
    df = df[df.index.date <= end]
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
        name = "Close"
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

# def plotOptionData(df, start, end):




