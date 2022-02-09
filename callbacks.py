from logging.config import valid_ident
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
import dash_table
from pandas_datareader import data
import pandas as pd
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
import h2o
from h2o.automl import H2OAutoML
import math
import numpy as np
# from dash.dash_table.Format import Group
from dash_table.Format import Format,Group
from dash_table import FormatTemplate as FormatTemplate
from datetime import datetime as dt
from app import app
from helper_funcs import stock_picker,create_time_features,feat_eng,models_training,prediction,test_performance
from dash.exceptions import PreventUpdate
# from dash_extensions.enrich import Output, Dash, Trigger,FileSystemCache
# from dash.long_callback import DiskcacheLongCallbackManager
# import diskcache
# cache = diskcache.Cache("./cache")
# long_callback_manager = DiskcacheLongCallbackManager(cache)
# fsc = FileSystemCache("cache_dir")
# fsc.set("progress", None)
####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

####################### Corporate css formatting
corporate_colors = {
    'dark-blue-grey' : 'rgb(62, 64, 76)',
    'medium-blue-grey' : 'rgb(77, 79, 91)',
    'superdark-green' : 'rgb(41, 56, 55)',
    'dark-green' : 'rgb(57, 81, 85)',
    'medium-green' : 'rgb(93, 113, 120)',
    'light-green' : 'rgb(186, 218, 212)',
    'pink-red' : 'rgb(255, 101, 131)',
    'dark-pink-red' : 'rgb(247, 80, 99)',
    'white' : 'rgb(251, 251, 252)',
    'light-grey' : 'rgb(208, 206, 206)'
}

externalgraph_rowstyling = {
    'margin-left' : '15px',
    'margin-right' : '15px'
}

externalgraph_colstyling = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['superdark-green'],
    'background-color' : corporate_colors['superdark-green'],
    'box-shadow' : '0px 0px 17px 0px rgba(186, 218, 212, .5)',
    'padding-top' : '10px'
}

filterdiv_borderstyling = {
    'border-radius' : '0px 0px 10px 10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : corporate_colors['light-green'],
    'background-color' : corporate_colors['light-green'],
    'box-shadow' : '2px 5px 5px 1px rgba(255, 101, 131, .5)'
    }

navbarcurrentpage = {
    'text-decoration' : 'underline',
    'text-decoration-color' : corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
    }

recapdiv = {
    'border-radius' : '10px',
    'border-style' : 'solid',
    'border-width' : '1px',
    'border-color' : 'rgb(251, 251, 252, 0.1)',
    'margin-left' : '15px',
    'margin-right' : '15px',
    'margin-top' : '15px',
    'margin-bottom' : '15px',
    'padding-top' : '5px',
    'padding-bottom' : '5px',
    'background-color' : 'rgb(251, 251, 252, 0.1)'
    }

recapdiv_text = {
    'text-align' : 'left',
    'font-weight' : '350',
    'color' : corporate_colors['white'],
    'font-size' : '1.5rem',
    'letter-spacing' : '0.04em'
    }

####################### Corporate chart formatting

corporate_title = {
    'font' : {
        'size' : 16,
        'color' : corporate_colors['white']}
}

corporate_xaxis = {
    'showgrid' : False,
    'linecolor' : corporate_colors['light-grey'],
    'color' : corporate_colors['light-grey'],
    'tickangle' : 315,
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_yaxis = {
    'showgrid' : True,
    'color' : corporate_colors['light-grey'],
    'gridwidth' : 0.5,
    'gridcolor' : corporate_colors['dark-green'],
    'linecolor' : corporate_colors['light-grey'],
    'titlefont' : {
        'size' : 12,
        'color' : corporate_colors['light-grey']},
    'tickfont' : {
        'size' : 11,
        'color' : corporate_colors['light-grey']},
    'zeroline': False
}

corporate_font_family = 'Dosis'

corporate_legend = {
    'orientation' : 'h',
    'yanchor' : 'bottom',
    'y' : 1.01,
    'xanchor' : 'right',
    'x' : 1.05,
	'font' : {'size' : 9, 'color' : corporate_colors['light-grey']}
} # Legend will be on the top right, above the graph, horizontally

corporate_margins = {'l' : 5, 'r' : 5, 't' : 45, 'b' : 15}  # Set top margin to in case there is a legend

corporate_layout = go.Layout(
    font = {'family' : corporate_font_family},
    title = corporate_title,
    title_x = 0.5, # Align chart title to center
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis = corporate_xaxis,
    yaxis = corporate_yaxis,
    height = 270,
    legend = corporate_legend,
    margin = corporate_margins
    )


####################################################################################################
# 000 - DEFINE ADDITIONAL FUNCTIONS
####################################################################################################



def colorscale_generator(n, starting_col = {'r' : 186, 'g' : 218, 'b' : 212}, finish_col = {'r' : 57, 'g' : 81, 'b' : 85}):
    """This function generate a colorscale between two given rgb extremes, for an amount of data points
    The rgb should be specified as dictionaries"""
    r = starting_col['r']
    g = starting_col['g']
    b = starting_col['b']
    rf = finish_col['r']
    gf = finish_col['g']
    bf = finish_col['b']
    ri = (rf - r) / n
    gi = (gf - g) / n
    bi = (bf - b) / n
    color_i = 'rgb(' + str(r) +','+ str(g) +',' + str(b) + ')'
    my_colorscale = []
    my_colorscale.append(color_i)
    for i in range(n):
        r = r + ri
        g = g + gi
        b = b + bi
        color = 'rgb(' + str(round(r)) +','+ str(round(g)) +',' + str(round(b)) + ')'
        my_colorscale.append(color)

    return my_colorscale

# Create a corporate colorcale
colors = colorscale_generator(n=11)

corporate_colorscale = [
    [0.0, colors[0]],
    [0.1, colors[1]],
    [0.2, colors[2]],
    [0.3, colors[3]],
    [0.4, colors[4]],
    [0.5, colors[5]],
    [0.6, colors[6]],
    [0.7, colors[7]],
    [0.8, colors[8]],
    [0.9, colors[9]],
    [1.0, colors[10]]]


####################################################################################################
# 001 - Pred performance table
####################################################################################################
# @app.callback(Output("result", "children"), Trigger("l2_model_cnt", "value"))
# def run_calculation(l2_model_cnt):
#     for i in range(l2_model_cnt):
#         fsc.set("progress", str((i + 1) / l2_model_cnt))  # update progress
#         time.sleep(10)  # do actual calculation (emulated by sleep operation)
#     return "done"


# @app.callback(Output("progress", "children"), Trigger("interval", "n_intervals"))
# def updateprogress(l2_model_cnt):
#     value = fsc.get("progress")  # get progress
#     if value is None:
#         raise PreventUpdate
#     return "Progress is {:.0f}%".format(float(fsc.get("progress")) * 100)




@app.callback(
    [dash.dependencies.Output('recap-table', 'data'), dash.dependencies.Output('recap-table', 'columns'), dash.dependencies.Output('recap-table', 'style_data_conditional')],
	[dash.dependencies.Output('pred', 'figure')],
    [dash.dependencies.State('date-picker-price', 'start_date'),
	 dash.dependencies.State('date-picker-price', 'end_date'),
     dash.dependencies.State('l1_tickers', 'value'),
     dash.dependencies.State('date-picker-val', 'date'),
     dash.dependencies.State('l2_model_cnt', 'value'),
     dash.dependencies.Input('create_button', 'n_clicks'),
     dash.dependencies.State('date_picker_target', 'start_date'),
	 dash.dependencies.State('date_picker_target', 'end_date')])


def get_data(start_date, end_date, l1_tickers, date,l2_model_cnt,clicks,start,end):

        #To determine if n_clicks is changed. 
    changed_ids = [p['prop_id'].split('.')[0] for p in dash.callback_context.triggered]
    
    button_pressed = 'create_button' in changed_ids

    if not button_pressed:
        PreventUpdate
    else:

        stocks_df=stock_picker(l1_tickers,'yahoo',start_date,end_date)

        # create feats
        train_features=feat_eng(stocks_df)

        #train models
        
        h2o.init(max_mem_size_GB=16,nthreads=10)
        

        models,symbols,test_df=models_training(train_features,l2_model_cnt,7)


        val=test_performance(models,symbols,date)
        # val=val.reset_index(drop=True)
        val['MAPE']=round(val['MAPE'],2)
        val=val.sort_values(by=['MAPE','Ticker'])#.drop_duplicates(subset=['Ticker','days_from_validation_date'])
        # Configure table data
        
        data = val.to_dict('records')
        columns = [
            {'id' : 'Ticker', 'name' : 'Ticker'},
            {'id' : 'days_from_validation_date', 'name' : 'days_from_validation_date', 'type' : 'numeric'},#,'format' : Format(scheme=Scheme.fixed, precision=0, group=Group.no, group_delimiter=',', decimal_delimiter='.')},
            {'id' : 'MAPE', 'name' : '% MAPE', 'type': 'numeric'}
        ]

        # Configure conditional formatting
        conditional_style=[
            {'if' : {
                'filter_query' : '{MAPE} < 5',
                'column_id' : 'MAPE'},
            'backgroundColor' : corporate_colors['light-green'],
            'color' : corporate_colors['dark-green'],
            'fontWeight' : 'bold'
            },
            {'if' : {
                'filter_query' : '{MAPE}  >= 5',
                'column_id' : 'MAPE'},
            'backgroundColor' : corporate_colors['pink-red'],
            'color' : corporate_colors['dark-green'],
            'fontWeight' : 'bold'
            },
        ]
        # h2o.shutdown()


        preds=prediction(models, symbols, pd.date_range(pd.to_datetime(start),pd.to_datetime(end),freq='d'))
        
    
        # Build graph
        import plotly.express as px

        fig=px.line(preds,x='Date',y='Prediction',color='Ticker',line_group='Ticker',hover_name='Ticker',markers=True)
        # fig.update_layout(xaxis=dict(showgrid=False),
        #       yaxis=dict(showgrid=False))
        fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
        fig.update_layout(font = {'family' : corporate_font_family},
        xaxis = corporate_xaxis,
        yaxis = corporate_yaxis,legend = corporate_legend,
        margin = corporate_margins,
        title_text='Price Prediction',
        title_font_size= 20,
        title_font_color=corporate_colors['white'])
        

        # h2o.shutdown()
        return data, columns, conditional_style,fig

####################################################################################################
# 003 - SALES COUNT DAY
# ####################################################################################################
# @app.callback(
#     dash.dependencies.Output('sales-count-day', 'figure'),
# 	[dash.dependencies.Input('date-picker-sales', 'start_date'),
# 	 dash.dependencies.Input('date-picker-sales', 'end_date'),
#      dash.dependencies.Input('reporting-groups-l1dropdown-sales', 'value'),
#      dash.dependencies.Input('reporting-groups-l2dropdown-sales', 'value')])
# def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
#     start = dt.strptime(start_date, '%Y-%m-%d')
#     end = dt.strptime(end_date, '%Y-%m-%d')

#     # Filter based on the dropdowns
#     isselect_all_l1 = 'Start' #Initialize isselect_all
#     isselect_all_l2 = 'Start' #Initialize isselect_all
#     ## L1 selection (dropdown value is a list!)
#     for i in reporting_l1_dropdown:
#         if i == 'All':
#             isselect_all_l1 = 'Y'
#             break
#         elif i != '':
#             isselect_all_l1 = 'N'
#         else:
#             pass
#     # Filter df according to selection
#     if isselect_all_l1 == 'N':
#         sales_df_1 = sales_import.loc[sales_import[sales_fields['reporting_group_l1']].isin(reporting_l1_dropdown), : ].copy()
#     else:
#         sales_df_1 = sales_import.copy()
#     ## L2 selection (dropdown value is a list!)
#     for i in reporting_l2_dropdown:
#         if i == 'All':
#             isselect_all_l2 = 'Y'
#             break
#         elif i != '':
#             isselect_all_l2 = 'N'
#         else:
#             pass
#     # Filter df according to selection
#     if isselect_all_l2 == 'N':
#         sales_df = sales_df_1.loc[sales_df_1[sales_fields['reporting_group_l2']].isin(reporting_l2_dropdown), :].copy()
#     else:
#         sales_df = sales_df_1.copy()
#     del sales_df_1

#     #Aggregate df
#     val_cols = [sales_fields['sales'],sales_fields['sales target']]
#     sales_df = sales_df.groupby(sales_fields['date'])[val_cols].agg('sum')
#     sales_df.reset_index(inplace=True)

#     # Filter based on the date filters
#     df = sales_df.loc[(sales_df[sales_fields['date']]>=start) & (sales_df[sales_fields['date']]<=end), :].copy()
#     del sales_df

#     # Build graph
#     hovertemplate_xy = (
#     "<i>Day</i>: %{x|%a, %d-%b-%Y}<br>"+
#     "<i>Sales</i>: %{y:,d}"+
#     "<extra></extra>") # Remove trace info
#     data = go.Scatter(
#         x = df[sales_fields['date']],
#         y = df[sales_fields['sales']],
#         line = {'color' : corporate_colors['light-green'], 'width' : 0.5},
#         hovertemplate = hovertemplate_xy)
#     fig = go.Figure(data=data, layout=corporate_layout)
#     fig.update_layout(
#         title={'text' : "Sales per Day"},
#         xaxis = {
#             'title' : "Day",
#             'tickformat' : "%d-%m-%y"},
#         yaxis = {
#             'title' : "Sales (units)",
#             'range' : [0, 100000]},
#         showlegend = False)

#     return fig

####################################################################################################
