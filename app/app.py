from flask import Flask, render_template, request, redirect

import quandl as Qd
import pandas as pd
import numpy as np
import os
from datetime import datetime
from datetime import timedelta
from bokeh.io import curdoc
from bokeh.layouts import row, column, gridplot
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components,file_html
from os.path import dirname, join  

app = Flask(__name__)
app.vars={}


# def add_one_month(dt0):
#     temp = datetime(dt0.year, dt0.month, dt0.day) + timedelta(days=32)
#     next_month = datetime(temp.year, temp.month, dt0.day)
#     return next_month

def plot_closing_price(ticker='GOOG',start_date='2014-01-01',end_date='2017-01-01'):
    API_key = 'xT9VhtodYJ7fzaKqVDby'
    # tmp = datetime.strptime(year_month, '%Y-%m')
    # start_date = datetime(tmp.year,tmp.month,1)
    # end_date = add_one_month(start_date)
    data = Qd.get('WIKI/%s' %ticker, trim_start = start_date, trim_end = end_date , authtoken=API_key)
    keep =['Adj. High','Adj. Low','Adj. Close','Adj. Volume']
    df = pd.DataFrame(data)
    mydf = df[keep]
    mydf.reset_index(level=0, inplace=True)
    p = figure(plot_width=700, plot_height=500,x_axis_type="datetime", title=" Quandl WIKI EOD Stock Prices: %s" %ticker)
    # normalized_df=(mydf['Adj. Volume']-mydf['Adj. Volume'].min())/(mydf['Adj. Volume'].max()-mydf['Adj. Volume'].min())
    # p.circle(mydf['Date'], mydf["Adj. Close"], size=5+5*normalized_df, fill_color='darkblue', legend = 'Norm. Volume', fill_alpha=0.4, line_color='black', line_alpha = 0.8)
    p.line(mydf['Date'], mydf["Adj. Close"],line_color='darkblue', line_width = 1.5, line_alpha=0.5, legend= 'Adj. Close')
    p.legend.background_fill_alpha = 0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price' 
    p.background_fill_color = "#dddddd"
    p.grid.grid_line_color = "white"
    p.legend.location = "top_center"

    return p

@app.route("/index", methods=['GET','POST'])    

def index():
    
    if request.method == 'GET':
        return render_template('index.html')
        
    else:
        #request was a POST
        ticker = request.form['ticker']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        plot = plot_closing_price(ticker,start_date,end_date)

        script, div = components(plot)       
        return render_template('plotpage.html', script=script, div=div)
       
@app.route('/', methods=['GET','POST'])
def main():
    return redirect('/index')

if __name__== "__main__":

    app.run(port=33507, debug = True)
