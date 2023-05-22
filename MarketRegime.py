import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
import plotly.graph_objects as go
from plotly.graph_objs.scatter.marker import Line
from plotly.subplots import make_subplots
import plotly.express as px
from sklearn.cluster import AgglomerativeClustering
from sklearn.mixture import GaussianMixture
import math
import yfinance as yf
import datetime
import warnings

warnings.filterwarnings('ignore')

def prepare_data_for_model_input(prices, ma):
    '''
        Input:
        prices (df) - Dataframe of close prices
        ma (int) - legth of the moveing average
        
        Output:
        prices(df) - An enhanced prices dataframe, with moving averages and log return columns
        prices_array(nd.array) - an array of log returns
    '''
    prices.index = prices.index.date
    # print(prices)
    intrument = prices.columns.name
    prices[f'{intrument}_ma'] = prices.rolling(ma).mean()
    prices[f'{intrument}_log_return'] = np.log(prices[f'{intrument}_ma']/prices[f'{intrument}_ma'].shift(1)).dropna()
 
    prices.dropna(inplace = True)
    prices_array = np.array([[q] for q in prices[f'{intrument}_log_return'].values])
    
    return prices, prices_array

class RegimeDetection:
 
    def get_regimes_hmm(self, input_data, params):
        hmm_model = self.initialise_model(GaussianHMM(), params).fit(input_data)
        return hmm_model
    
    def get_regimes_clustering(self, params):
        clustering =  self.initialise_model(AgglomerativeClustering(), params)
        return clustering
    
    def get_regimes_gmm(self, input_data, params):
        gmm = self.initialise_model(GaussianMixture(), params).fit(input_data)
        return gmm
        
    def initialise_model(self, model, params):
        for parameter, value in params.items():
            setattr(model, parameter, value)
        return model
    
def plot_hidden_states(hidden_states, prices_df):
    
    '''
    Input:
    hidden_states(numpy.ndarray) - array of predicted hidden states
    prices_df(df) - dataframe of close prices
    
    Output:
    Graph showing hidden states and prices
    
    '''
    
    colors = ['blue', 'green']
    n_components = len(np.unique(hidden_states))
    fig = go.Figure()
 
    for i in range(n_components):
        mask = hidden_states == i
        print('Number of observations for State ', i,":", len(prices_df.index[mask]))
        
        fig.add_trace(go.Scatter(x=prices_df.index[mask], y=prices_df['Close'][mask],
                    mode='markers',  name='Hidden State ' + str(i), marker=dict(size=4,color=colors[i])))
        
    fig.update_layout(height=400, width=900, legend=dict(
            yanchor="top", y=0.99, xanchor="left",x=0.01), margin=dict(l=20, r=20, t=20, b=20)).show()
    
def feed_forward_training(model, params, prices, split_index, retrain_step):
    '''
    Input:
    model (<class 'method'>) - either gmm (Gaussian Mixture Models) or hmm (Hidden Markov Model)
    params (dict) - dictionary of parameters for a model
    prices (df) - Dataframe of close prices
    split_index (str) - index to split initial traing dataset and out of sample testing set
    retrain_step (int) - number of observations after which we retrain the model
    
    Output:
    states_pred (numpy.ndarray) - array of predicted hidden states
    '''
    # train/test split and initial model training
    init_train_data = prices[:split_index]
    test_data = prices[split_index:]
    rd_model = model(init_train_data, params)
    
    # predict the state of the next observation
    states_pred = []
    for i in range(math.ceil(len(test_data))):
        split_index += 1
        preds = rd_model.predict(prices[:split_index]).tolist()
        states_pred.append(preds[-1])
        
        # retrain the existing model
        if i % retrain_step == 0:
            rd_model = model(prices[:split_index], params)
            
    return  states_pred

regime_detection = RegimeDetection()
# GETTING DATA
Stock =      yf.Ticker('^NSEI')
Data = Stock.history(period='max')

drop_cols = []
for col in Data.columns:
    if col == 'Close':
        pass
    else:
        drop_cols.append(col)

Data.drop(columns=drop_cols, inplace=True)
prices, prices_array = prepare_data_for_model_input(Data, 14)
print(prices)
print(prices_array)
# # COMPLETE TRAINING
# params = {'n_components':2, 'covariance_type':"full", 'random_state':100}
# hmm_model = regime_detection.get_regimes_hmm(prices_array, params)
# hmm_states = hmm_model.predict(prices_array)
# plot_hidden_states(np.array(hmm_states), prices[['Close']])

# FEED FORWARD TRAINING
model_hmm =  regime_detection.get_regimes_hmm
params = {'n_components':2, 'covariance_type': 'full', 'random_state':100}
split_index = np.where(prices.index > datetime.date(2015, 1, 1))[0][0]
states_pred_hmm = feed_forward_training(model_hmm, params, prices_array, split_index, 20)
plot_hidden_states(np.array(states_pred_hmm), prices[['Close']][split_index:])