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

class MyFormatter(Formatter): #test002
  def __init__(self, dateNumList, fmt='%d\n%b'):
    self.fmt = fmt
    self.dateNumList = dateNumList
  def __call__(self, x, pos=0):
    idx=int(x)
    if idx < 0:
      return num2date(self.dateNumList[0]+idx).strftime(self.fmt)
    elif idx >= len(self.dateNumList):
      return num2date(self.dateNumList[-1]+(idx-len(self.dateNumList)-1)).strftime(self.fmt)
    else:
      return num2date(self.dateNumList[idx]).strftime(self.fmt)
      
def plotCandlestick(df,filename,w,h):
  ohlc = []
  dateNumList = [] #test002
  indexList = [] #test002
  i=0
  for index, row in df.iterrows():
    nDate=date2num(row.name.to_pydatetime())
    rec = i, row['open'], row['high'], row['low'], row['close']
    ohlc.append(rec)
    dateNumList.append(nDate) #test002
    indexList.append(i) #test002
    i+=1
  
  fig, ax = plt.subplots(figsize=(w,h))
  formatter = MyFormatter(dateNumList)  #test002
  ax.xaxis.set_major_formatter(formatter)

  candlestick_ohlc(ax, ohlc, colorup='#77d879', colordown='#b72015')
  ax.plot(indexList, df['sma20'].values, color='#5899bb', linestyle='solid', marker=',', linewidth=1)
  ax.plot(indexList, df['hband'].values, color='#5899bb', linestyle='solid', marker=',', linewidth=1)
  ax.plot(indexList, df['lband'].values, color='#5899bb', linestyle='solid', marker=',', linewidth=1)
  #ax.autoscale_view()
  ax.fill_between(indexList, df['hband'].values, df['lband'].values, color='#88ccee', alpha=0.15) #test002
  fig.savefig(filename, dpi=300, bbox_inches='tight', pad_inches=0)

