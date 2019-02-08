import matplotlib.pyplot as plt
import matplotlib.dates as mdates
#from matplotlib.dates import date2num
#from matplotlib.dates import num2date
from matplotlib.ticker import Formatter
from mpl_finance import candlestick_ohlc
#from mpl_finance import candlestick2_ohlc
import pandas as pd
import numpy as np
from datetime import datetime

'''
============================================================================================================
Class for formatting X axis date labels
 - This is created to avoid the gap occuring for weekends and holidays
============================================================================================================
'''
class MyFormatter(Formatter):
  def __init__(self, dateList, fmt='%d\n%b'):
    self.fmt = fmt
    self.dateList = dateList
  def __call__(self, x, pos=0):
    idx=int(x)
    if idx >= len(self.dateList) or idx < 0:
      return ''
    else:
      return pd.to_datetime(self.dateList[idx]).strftime(self.fmt)

'''
============================================================================================================
Candlestick plot
============================================================================================================
'''
def plotCandlestick(df,filename,w,h):
  ohlc = []
  #dateNumList = []
  indexList = []
  i=0
  for index, row in df.iterrows():
    #nDate=date2num(row.name.to_pydatetime())
    rec = i, row['open'], row['high'], row['low'], row['close']
    ohlc.append(rec)
    #dateNumList.append(nDate)
    indexList.append(i)
    i+=1
  
  fig, ax = plt.subplots(figsize=(w,h))
  formatter = MyFormatter(df.index.values)
  ax.xaxis.set_major_formatter(formatter)

  candlestick_ohlc(ax, ohlc, colorup='#77d879', colordown='#b72015')
  ax.plot(indexList, df['sma20'].values, color='#5899bb', linestyle='solid', marker=',', linewidth=1)
  ax.plot(indexList, df['hband'].values, color='#5899bb', linestyle='solid', marker=',', linewidth=1)
  ax.plot(indexList, df['lband'].values, color='#5899bb', linestyle='solid', marker=',', linewidth=1)
  #ax.autoscale_view()
  ax.fill_between(indexList, df['hband'].values, df['lband'].values, color='#88ccee', alpha=0.15) #test002
  fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)

'''
============================================================================================================
SMA plot
============================================================================================================
'''
def plotSMA(df,smaFilename,w,h):
  fig, ax = plt.subplots(figsize=(w,h))
  ax.plot_date(df.index.values, df['sma200'].values, color='b', linestyle='solid', marker=',', linewidth=1, label='SMA/200')
  ax.plot_date(df.index.values, df['sma20'].values, color='g', linestyle='solid', marker=',', linewidth=1, label='SMA/20')
  ax.plot_date(df.index.values, df['close'].values, color='#B72015', linestyle='solid', marker=',', linewidth=1, label='Price')
  #ax.fill_between(df.index.values, df['hband'].values, df['lband'].values, color='blue', alpha=0.3)
  ax.legend(frameon=False)
  ax.xaxis_date()
  ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
  plt.savefig(smaFilename, dpi=300, bbox_inches='tight', pad_inches=0)

'''
============================================================================================================
MACD plot
============================================================================================================
'''
def plotMACD(df,macdFilename,w,h):
  fig, ax = plt.subplots(figsize=(w,h))
  formatter = MyFormatter(df.index.values)
  ax.xaxis.set_major_formatter(formatter)
  indexList=np.arange(len(df.index.values)).tolist()
  print(indexList)
  ax.plot(indexList, df['macd'].values, color='#000000', linestyle='solid', marker=',', linewidth=1, label='MACD')
  ax.plot(indexList, df['signal'].values, color='#FF0000', linestyle='solid', marker=',', linewidth=1, label='Signal')
  ax.bar(indexList, df['macdhisto'].values, color=df['macdhistocolor'].values)
  ax.legend(frameon=False)
  #ax.xaxis_date()
  #ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
  #ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
  plt.savefig(macdFilename, dpi=300, bbox_inches='tight', pad_inches=0)
