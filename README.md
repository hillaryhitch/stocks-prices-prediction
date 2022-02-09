# Stocks forecasting-Dashboard

![list](https://github.com/hillaryhitch/stocks-prices-prediction/blob/main/Screenshot%202022-02-08%20at%2016.00.08.png)

# Summary

This is a stocks prediction udacity nano degree capstone project. I basically changed it into a normal regression problem and used h2o autoML to train my models

The project has 3 parts:

1. Modelling (methods initially built in a jupyter notebook)
2. User dashboard , written in Python and including layout customisations with .css bootstrap.
The app has been deployed on Heroku and is visible here: https://stocks-prices-prediction-py.herokuapp.com/

The data used is historical adjusted closing prices downloaaded from yahoofinance using pandas_datareader. The inputs and outputs are all presented inform of a dash dashboard, the dashboard is open enough to give the user power to select multiple parameters.

The user can select:

1. A start and end date to train a model 
2. a start and end date to predict 
3. A datae to validate and see the models performance
4. Number of models to explore in h2o
5. Symbols to be predicted (multiple or one)

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

# Acknowledgement
Thanks to Gabrielle Albini's work on how to custom style a dashboard


