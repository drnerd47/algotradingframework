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
    fig.show()

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



