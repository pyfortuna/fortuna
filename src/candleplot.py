import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import date2num
from mpl_finance import candlestick_ohlc
from mpl_finance import candlestick2_ohlc
import fortunacommon
import datetime


def plotCandlestick(df,filename):
  fig, ax = plt.subplots()
  candlestick_ohlc(ax, zip(date2num(datetime.fromisoformat(df['Date']),df['AAPL.Open'], df['AAPL.High'],df['AAPL.Low'], df['AAPL.Close']))
  #candlestick2_ohlc(ax, df['AAPL.Open'], df['AAPL.High'],df['AAPL.Low'], df['AAPL.Close'])
  #ax.autoscale_view()
  #ax.xaxis.grid(True, 'major')
  #ax.grid(True)
  fig.autofmt_xdate()
  fig.savefig(filename)

o_file="/home/ec2-user/plutus/candleplot.png"
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
plotCandlestick(df,o_file)
fortunacommon.sendMail("candleplot","candleplot",o_file)
