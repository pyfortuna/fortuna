import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from matplotlib.dates import num2date
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
  def __init__(self, dateNumList, fmt='%d\n%b'):
    self.fmt = fmt
    self.dateNumList = dateNumList
  def __call__(self, x, pos=0):
    print(x)
    return self.dateNumList[int(x)].strftime(self.fmt)
      
#def plotCandlestick(df,filename,dateFormat):
def plotCandlestick(df,filename,w,h):
  ohlc = []
  dateNumList = [] #test002
  indexList = [] #test002
  i=0
  for index, row in df.iterrows():
    #nDate=date2num(datetime.strptime(row.name,dateFormat))
    nDate=date2num(row.name.to_pydatetime())
    rec = nDate, row['open'], row['high'], row['low'], row['close']
    ohlc.append(rec)
    dateNumList.append(nDate) #test002
    i+=1
    indexList.append(i) #test002
  
  print('DEBUG: [dateNumList]')
  print(dateNumList)
  print('DEBUG: [indexList]')
  print(indexList)
  
  fig, ax = plt.subplots(figsize=(w,h))
  formatter = MyFormatter(dateNumList)  #test002

  candlestick_ohlc(ax, ohlc, colorup='#77d879', colordown='#b72015')
  #ax.plot_date(df.index.values, df['sma20'].values, color='b', linestyle='solid', marker=',', linewidth=1) #test002
  ax.plot(indexList, df['sma20'].values, color='b', linestyle='solid', marker=',', linewidth=1)
  ax.autoscale_view()
  ax.fill_between(indexList, df['hband'].values, df['lband'].values, color='#88ccee', alpha=0.15) #test002
  #ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0)) #test001 #test002
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
