
from pandas_datareader import data
import pandas as pd

from datetime import date
from datetime import datetime
from datetime import timedelta
import h2o
from h2o.automl import H2OAutoML
import math
import numpy as np

def stock_picker(tickers:list,data_source,start_date,end_date):
    '''INPUT
    ticker: a list of tickers of interest
    start_date: first date
    end_date: last date of interest
    
    OUTPUT
    price_df: a dataframe with ticker, date and final adj price'''
    price_df=data.DataReader(tickers,data_source,start_date,end_date)
    #stack the symbols
    prices_stacked_df=price_df['Adj Close'].stack()
    
    #reset the index and sort values
    prices_stacked_df=prices_stacked_df.reset_index()
    prices_stacked_df=prices_stacked_df.sort_values(by=['Symbols','Date'])
    prices_stacked_df_clean=prices_stacked_df.rename(columns={0:'Prices'})

    return prices_stacked_df_clean

def create_time_features(df):
    """
    Creates time series features from datetime index
    """
    df['date'] = pd.to_datetime(df['Date'])
#     df['hour'] = df['date'].dt.hour
    # df['dayofweek'] = np.where(df['date'].dt.dayofweek<5,1,0)
    df['dayofweek1'] = df['date'].dt.dayofweek
    df['norms']=2*np.pi*df['dayofweek1']/df['dayofweek1'].max()
#     df['cosday']==np.cos(df['norms'])
#     df['sinday']==np.sin(df['norms'])
    df['quarter'] = df['date'].dt.quarter
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    df['dayofyear'] = df['date'].dt.dayofyear
    df['sin_day'] = np.sin(df['dayofyear'])
    df['cos_day'] = np.cos(df['dayofyear'])
    df['dayofmonth'] = df['date'].dt.day
    df['weekofyear'] = df['date'].dt.weekofyear
    df['end']=df['date'].dt.is_month_end
    df['weekofmonth']=(df['date'].dt.day-1)//7+1

    X = df
    return X


def feat_eng(df):
    '''This is a tsfresh function to pivot the data and create aggregates with tsfresh and pick relevant ones
    INPUT:
    stocks_df: a dataframe with prices 
    
    OUTPUT:
    train_model_df: output dataframe with date features'''

    train_model_df=create_time_features(df.sort_values(by=['Symbols','Date'])).drop(['Date','date'],1)
    train_model_df=train_model_df.rename(columns={'Prices':'y'})

    return train_model_df



validation_period=7

def models_training(train_features,models_to_explore:int,validation_period:int):
    '''INPUT:
    train_features: dataframe with training features, all symbols and label
    validation_period: validation period as int
    
    OUTPUT:
    
    models: list of best models per symbol
    symbols: list of symbols
    test_df: dataframe with test predictions'''
    global models
    global symbols
    global test_df
    models=[]
    symbols=[]
    test_df=[]
    for i in train_features['Symbols'].unique():

        

        train1=train_features[train_features['Symbols']==i].drop('Symbols',1)
    #     n=train1.shape[0]
    #     test_cut=math.ceil(n*0.3)
        train=train1.iloc[:-validation_period]
        test=train1.iloc[-validation_period:]
        train2 = h2o.H2OFrame(train)
        test2 = h2o.H2OFrame(test)


        x_train = train2.columns
        y_train = "y"
        x_train.remove(y_train)


        # Run AutoML for 20 base models (limited to 1 hour max runtime by default)
        aml = H2OAutoML(max_models=models_to_explore)
        aml.train(x=x_train, y=y_train, training_frame=train2)

        # View the AutoML Leaderboard
        lb = aml.leader
        predicts=aml.leader.predict(test2).as_data_frame()
        test=test.reset_index()
        test['pred']=predicts

        models.append(lb)
    
        test_df.append(test)
        symbols.append(i)

#     h2o.shutdown()
        
    return models,symbols,test_df


def prediction(models, symbols, target_date):

    """INPUT: models: a list of trained models
    symbols: a list of tickers to predict
    target_date: a date you need predicted"""
    df= pd.DataFrame(
          {'Date' : target_date
          }
        )
    feats=create_time_features(df).drop(['Date','date'],1)

    
    prices_predictions = pd.DataFrame(columns = ['Date', 'Ticker', 'Prediction'])

    for model, symbol in zip(models, symbols):
        pred_df = h2o.H2OFrame(feats)

        prediction = model.predict(pred_df).as_data_frame()['predict']
        print(prediction)
        predicted_df = pd.DataFrame(
          {'Date' : target_date,
          'Ticker' : symbol,
          'Prediction' : prediction
          }
        )

        prices_predictions = prices_predictions.append(predicted_df, ignore_index = True)
    
    return prices_predictions


def test_performance(models,symbols,validation_date):
    '''INPUT test_df with: forecasted: the forecasted column actual: the actual column OUTPUT: mape: mean absolute percentage error'''
    mape_df=pd.DataFrame()
    for i in (7,14,28):
        
        df=stock_picker(symbols,'yahoo',pd.to_datetime(pd.to_datetime(validation_date)-timedelta(i)),validation_date)

        df2=feat_eng(df)
    
        for p,j in zip(range(len(symbols)),symbols):
            df3=df2[df2['Symbols']==j]
            print(df3)
            pred_df = h2o.H2OFrame(df3.drop(['Symbols','y'],1))
            df3=df3.reset_index(drop=True)
            df3['pred'] = models[p].predict(pred_df).as_data_frame()['predict']
            df3['symbol']=symbols[p]
            df3['period']=i
            # print(df3)
            
            
            error = abs(df3['pred']-df3['y'])
            mae = error/df3['y']
            mape = (mae*100).mean()
            # print('MAPE for {} is {}% on {} days of data from validation date'.format(symbols[p],round(mape,3),i))
            # print(df3['symbol'][0])
            mape_df=mape_df.append(pd.DataFrame(
          {'days_from_validation_date' :i,
          'Ticker' : df3['symbol'][0],
          'MAPE' : mape
          },
      index=[0]
        ))
        # h2o.shutdown()
    return mape_df