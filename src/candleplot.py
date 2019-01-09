import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from mpl_finance import candlestick_ohlc
from mpl_finance import candlestick2_ohlc
import pandas as pd
from datetime import datetime
from dateutil.rrule import rrule #test001
'''
import fortunacommon
'''

#def plotCandlestick(df,filename,dateFormat):
def plotCandlestick(df,filename):
  ohlc = []
  for index, row in df.iterrows():
    #nDate=date2num(datetime.strptime(row.name,dateFormat))
    nDate=date2num(row.name.to_pydatetime())
    rec = nDate, row['open'], row['high'], row['low'], row['close']
    ohlc.append(rec)
  #fig, ax = plt.subplots(figsize=(20, 15))
  fig, ax = plt.subplots()
  candlestick_ohlc(ax, ohlc, colorup='#77d879', colordown='#db3f3f')
  ax.plot_date(df.index.values, df['sma20'].values, color='b', linestyle='solid', marker=',', linewidth=1)
  ax.autoscale_view()
  #ax.xaxis.grid(True, 'major')
  #ax.grid(True)
  ax.fill_between(df.index.values, df['hband'].values, df['lband'].values, color='blue', alpha=0.1)
  #ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=[0,2,4])) #test001
  ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0)) #test001
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%d\n%b'))
  #fig.autofmt_xdate()
  fig.savefig(filename, dpi=300)

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
