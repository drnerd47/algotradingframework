import plotly.graph_objs as go
import matplotlib.pyplot as plt

def plotCandlestickChart(data):
    # Create chart object
    chart_data = [go.Candlestick(x=data.index[:100], 
                                open=data['open'][:100], 
                                high=data['high'][:100], 
                                low=data['low'][:100],
                                close=data['close'][:100]
                                )]
    # Load chart data
    fig = go.Figure(data=chart_data)
    # Update chart layout
    fig.update_layout(xaxis_rangeslider_visible=False, xaxis_showticklabels=True, yaxis_showticklabels=True)
    # Plot chart
    fig.show();

def plotBollingerBands(data):
    plt.figure(figsize=(20,10))
    data['close'].plot(label='CLOSE PRICE',  color="black")
    data['upband'].plot(label='UPPER BAND', linestyle = '--', linewidth = 1, color="orange")
    data['lowband'].plot(label="LOWER BAND",linestyle = '--', linewidth = 1, color="orange")
    plt.legend(loc='upper left')
    plt.show()

def plotMACD(data):
    plt.figure(figsize=(20,10))
    plt.plot(data.signal, label='signal', color='red')
    plt.plot(data.MACD, label='MACD', color='green')
    plt.legend()
    plt.show()

def plotBB(df):   
    chart_data = [go.Candlestick(x=df.index, 
                                open=df['open'], 
                                high=df['high'], 
                                low=df['low'],
                                close=df['close'], showlegend=False,
                                name= 'candlestick'
                                )]
    # Load chart data
    fig = go.Figure(data=chart_data)
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

# PlotSignal function takes the signal data i.e. the data where signals are generated( spot data )
def PlotSignal(df, start, end):
    df = df[df.index.date >= start]
    df = df[df.index.date <= end]

    bearentry = df[df.EntrySignal == -2]
    bullentry = df[df.EntrySignal == 2]
    stoploss = df[df.ExitSignal == -1]
    target = df[df.ExitSignal == 1]
    eodsquareoff = df[df.ExitSignal == 0]

    fig = go.Figure()

    fig.add_trace(go.Line(
        x = df.index,
        y = df.close,
        mode = "lines",
        name = "Close"
    ))

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

    fig.update(layout_xaxis_rangeslider_visible=True)    
    fig.update_xaxes(
        rangebreaks=[ dict(bounds=["sat", "mon"]) , dict(bounds=[16, 9], pattern="hour")])
    fig.show();




