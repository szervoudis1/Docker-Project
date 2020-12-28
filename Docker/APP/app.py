from flask import Flask,render_template,send_file
import io
import os
import random
import datetime
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from scipy.stats import norm



app = Flask(__name__)

list_of_stocks = ['IBM','GOOG','FB']
image_name = ''

def inputs(Stock_name,start_date,stop_date):
    df = None
    df = web.DataReader(f'{Stock_name}','yahoo',start_date,stop_date)
    df.to_csv(f'{Stock_name}' + ' - Rates.csv')


def daily_fluctuation(Stock_name):
    df = pd.read_csv(f'{Stock_name}' + ' - Rates.csv')
    df['Fluctuation'] = 100 * (df['Close'] - df['Open']) / df ['Open']
    output_excel_writer = pd.ExcelWriter(f'New_{Stock_name}.xlsx')
    df.to_excel(output_excel_writer, index=False)
    output_excel_writer.save()
    output_excel_writer.close()

    
def normalize(Stock_name):
    df = None
    df = pd.read_excel(f'New_{Stock_name}.xlsx',engine='openpyxl')
    # Υπολογσιμός Standard Deviation & Mean
    std = np.std(df['Fluctuation'],ddof=1)
    mean = np.mean(df['Fluctuation'])

    
    bins = (df['Fluctuation'].max() - df['Fluctuation'].min()) * 10
    bins = int(bins)

    plt.clf()
    domain = np.linspace(np.min(df['Fluctuation']),np.max(df['Fluctuation']))
    plt.plot(domain,norm.pdf(domain,mean,std))
    plt.hist(df['Fluctuation'], edgecolor = 'black',alpha=0.5,bins=bins, density=True)
    plt.title(f'{Stock_name}' + " - Normal Fit")
    plt.xlabel("Day_Var")
    plt.ylabel("Density")

    # Title box with blue line
    blue_line = mlines.Line2D([], [], color='blue', marker='',markersize=10,
                        label= "\n" + '$\mathcal{N}$ ' +  
                        f'$( \mu  \\approx {round((mean),5)} , \
                           \sigma  \\approx {round((std),5)} )$\n')
    plt.legend(handles=[blue_line])


def save_image():
	
      plt.savefig('static/images/' + image_name)
	

PEOPLE_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route('/')
def index():
    
    Stock_name = random.choice(list_of_stocks)
    print("The Chosen Stock Name : " + f'{Stock_name}')
    start_date = datetime.datetime(2019,11,1)
    stop_date = datetime.datetime(2020,11,1)
    
    ## 2
    inputs(Stock_name,start_date,stop_date)
    
    ## 3
    daily_fluctuation(Stock_name)
    
    ## 4
    normalize(Stock_name)

    
    global image_name
    image_name = 'image_'+ Stock_name + str(start_date) + str(stop_date) + '.jpg'
    
    ## 5
    save_image()
    
    
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    return render_template("index.html", user_image = full_filename)


if __name__ == "__main__":
    
    # Export Port
    app.run(host='0.0.0.0',port=5000,debug=False)
  

    























    





















