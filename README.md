# Project Overview

The stock market has always been a sort of black box inn its performance. 
Investors have tried multiple ways to predict future prices in order to make the right investment. 
It has been an area of interest for me  not only because of the money one can make; but also the power one would have over multiple companies.

Is it possible to accurately predict stock prices? 
According to Burton Malkiel , an American economist and author; stocks have unpredictable and random behaviour, this makes all methods of prediction unreliable.
In the recent years, because of advancement in technology, multiple prediction methods have been developed among them machine learning.

In this project, I will start a journey of predicting stock prices


# Problem Statement

The main objective of this project is to predict stock prices using machine learning.

The main challenge is to allow the user to select whichever stock they are interested in as well as prediction dates.

I will build a solution that includes:
    
1. Uses stock price data from Yahoo Finance

2. Perform all machine learning steps including training multiple models, validating the models

3. A python dash dashboard that acts as a user interface to select:
    

    a. A start and end date to train a model
    
    b. A start and end date to predict
    
    c. A date to validate and see the models performance
    
    d. Number of models to explore in h2o
    
    e. Symbols to be predicted (multiple or one)
    
    The user will see:

        a. A table with the best trained models performance
        
        b. A graph with all symbol predictions


# Metrics

The method that will be used is regression and the metric of interest will be MAPE ( mean absolute percentage error).


![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-09%20at%2022.22.19.png)

This measure is easy to understand because it provides the error in terms of percentages. 

Also, because absolute percentage errors are used, the problem of positive and negative errors canceling each other out is avoided. Consequently, MAPE is a measure commonly used in forecasting. 

The smaller the MAPE the better the forecast and the more profit we can make since we have the correct future information.

# Data Processing

The data I will be using is from yahoo finance, downloaded by pandas.dataset. I created a loop to find all symbols available in yahoo finance at a given time and used these symbols as my list of tickers in the final dashboard.

The data misses weekend information, I imputed with mean. Nothing else is necessary interms of data processing.

# EDA

Since we have to build a solution to predict any symbol from the stocks, we wont be able to explore all symbols, but we will use 'GS' for data exploration annd model building.

I choose 'GS' not because of any good generalization, but simply because I have history with their stocks.

We will use pandas_datareader to get the stock closing prices from Yahoo.


![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-09%20at%2022.29.51.png)


## Visualizations

![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-09%20at%2022.33.00.png)


There was a dip around March 2020, this is expected because it was the start of Corona. The stock prices however started growing from then.

There is some signal in the date features because we can see clear seasonal effects as below- there is always a dip in the 4th week of Jan,Feb,Mar,May,Sep,Dec, current years have had the biggest growths:
    
![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-09%20at%2022.59.17.png)

![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-09%20at%2022.59.23.png)


The plot below shows that the cumulative log returns for GS looks like it has hit a plateau in the recent months;

![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-09%20at%2022.44.11.png)

## Since we see some seasonality in the dates, we can create date features and try regression


# Modelling

## Baseline

I built a baseline using ARIMA, since its a good statistical to go to model for time series. 

An autoregressive integrated moving average (ARIMA) model is a generalization of an autoregressive moving average (ARMA) model. Both of these models are fitted to time series data either to better understand the data or to predict future points in the series (forecasting). ARIMA models are applied in some cases where data show evidence of non-stationarity, where an initial differencing step (corresponding to the "integrated" part of the model) can be applied one or more times to eliminate the non-stationarity. ARIMA model is of the form: ARIMA(p,d,q): p is AR parameter, d is differential parameter, q is MA parameter

I devided the data into 4 windows- the train, and 3 validation sets (from future data)

The results are as below:
    
   1. 4.7% MAPE for window 1
   
   
   2. 5.1% MAPE for window 2
   
   
   3. 5.7% MAPE for window 3
   
The MAPE increases the further we go in the future

# Model Evaluation and Validation

### XGBOOST

XGBOOST regressor with date features had the perfomance below:

    1. MAPE of 9.4% for window 1
    
    2. MAPE of 9.2% for window 2
    
    3. MAPE of 12.9% for window 3
    
## Hyper Parameter Tuning

I tuned the XGBOOST regressor using randomized search; I used randomized search because it is faster. 

The parameter space used was as below:

params = {
    'n_estimators':[500],
    'min_child_weight':[4,5], 
    'gamma':[i/10.0 for i in range(3,6)],  
    'subsample':[i/10.0 for i in range(6,11)],
    'colsample_bytree':[i/10.0 for i in range(6,11)], 
    'max_depth': [2,3,4,6,7],
    'objective': ['reg:squarederror', 'reg:tweedie'],
    'booster': ['gbtree', 'gblinear'],
    'eval_metric': ['rmse'],
    'eta': [i/10.0 for i in range(3,6)],
}


The best paramaters were picked from the randomized cross validation. The results improved marginally:

    1. MAPE of 8.07% for window 1
    
    2. MAPE of 7.69% for window 2
    
    3. MAPE of 11.94% for window 3



## H2o AutoML Ensembles:

I went ahead to try h2o automl but got worse results:

    1. MAPE of 17.675466462433885 for window 1
    
    2. MAPE of 17.218327973193198 for window 2
    
    3. MAPE of 17.513003431351507 for window 3
    
    
# Results

Even though ARIMA had the best short term performance, it does bad in long term predictions. In the deployment I used H2o as my models because it is more stable.   

![list](Screenshot 2022-02-10 at 03.01.46.png)

# Stocks forecasting-Dashboard

![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-08%20at%2016.00.08.png)

# Summary

The models are called by the user on a dashboard; written in Python and including layout customisations with .css bootstrap.
The app has been deployed on Heroku and is visible here: https://stocks-prices-prediction-py.herokuapp.com/

The user can select:

1. A start and end date to train a model 
2. a start and end date to predict 
3. A date to validate and see the models performance
4. Symbols to be predicted (multiple or one)
5. Number of models to explore
6. User clicks compute for training and results. The training might take 2mins

The user will see:

1. A table with the best trained models performance
2. A graph with all symbol predictions

*NOTE: the dashboard will be slow during traininng since we are exploring multiple models (aprox: 2mins)

# Libraries used
The solution is built on pyhton 3.8.7:

  Brotli==1.0.7

  click==7.1.2

  dash==1.14.0

  dash-core-components==1.10.2

  dash-html-components==1.0.3

  dash-renderer==1.6.0

  dash-table==4.9.0

  Flask==1.1.2

  Flask-Compress==1.5.0

  future==0.18.2

  itsdangerous==1.1.0

  Jinja2==2.11.2

  MarkupSafe==1.1.1

  numpy==1.19.1

  pandas==1.4.0

  plotly==4.9.0

  python-dateutil==2.8.1

  pytz==2020.1

  retrying==1.3.3

  six==1.15.0

  Werkzeug==1.0.1

  xlrd==1.2.0

  gunicorn==20.0.4

  h2o==3.36.0.2

  pandas-datareader==0.10.0
  
 # Conclusions
 
 I was able to predict stock maarket in the short term with less than 5% MAPE but with worse MAPE in longer prediction periods. 
 
 # Improvements
 
 1. More work can be done to make the models better by including external data especially socail media data and other sites like reddit
 2. More work can be done in tuning the models for only specific symbols and not all
 3. For the dashboard, one can include a progress bar (code already in place but commented out)
 4. Cache already trained models on different dates and outcomes to make the dashboard run faster
 

# Acknowledgement
Thanks to Gabrielle Albini's work on how to custom style a dashboard


