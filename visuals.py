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
    plt.plot(data['date'], data['close'])
    plt.plot(data['date'], data['lowband'], color="orange")
    plt.plot(data['date'], data['upband'], color="orange")
    plt.fill_between(data['date'], data['lowband'], data['upband'], alpha=0.2, color="orange")
    plt.show()

def plotMACD(data):
    plt.plot(data.signal, label='signal', color='red')
    plt.plot(data.MACD, label='MACD', color='green')
    plt.legend()
    plt.show()



