import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from matplotlib.ticker import Formatter
from mpl_finance import candlestick_ohlc
from mpl_finance import candlestick2_ohlc
import pandas as pd
import numpy as np
from datetime import datetime
'''
import fortunacommon
'''
class MyFormatter(Formatter): #test002
  def __init__(self, dates, fmt='%d\n%b'):
    self.dates = dates
    self.fmt = fmt
  def __call__(self, x, pos=0):
    ind = int(np.round(x))
    if ind >= len(self.dates) or ind < 0:
      return ''
    return num2date(self.dates[ind]).strftime(self.fmt)
      
#def plotCandlestick(df,filename,dateFormat):
def plotCandlestick(df,filename,w,h):
  ohlc = []
  for index, row in df.iterrows():
    #nDate=date2num(datetime.strptime(row.name,dateFormat))
    nDate=date2num(row.name.to_pydatetime())
    rec = nDate, row['open'], row['high'], row['low'], row['close']
    ohlc.append(rec)
  fig, ax = plt.subplots(figsize=(w,h))
  formatter = MyFormatter(df.index.values)  #test002

  candlestick_ohlc(ax, ohlc, colorup='#77d879', colordown='#B72015')
  #ax.plot_date(df.index.values, df['sma20'].values, color='b', linestyle='solid', marker=',', linewidth=1) #test002
  ax.plot_date(np.arange(len(df.index.values)), df['sma20'].values, color='b', linestyle='solid', marker=',', linewidth=1)
  ax.autoscale_view()
  ax.fill_between(df.index.values, df['hband'].values, df['lband'].values, color='#b3e1f2', alpha=0.15)
  ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0)) #test001
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%b'))  #test002
  ax.xaxis.set_major_formatter(formatter)
  fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)

'''
# TEST PROGRAM
o_file="/home/ec2-user/plutus/candleplot.png"
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
df.rename(columns={ 'AAPL.Open':'open',
                    'AAPL.High':'high',
                    'AAPL.Low':'low',
                    'AAPL.Close':'close'}, 
                    inplace=True)
plotCandlestick(df,o_file)
fortunacommon.sendMail("candleplot","candleplot",o_file)
'''
