'''
from mpl_finance import plot_day_summary_oclh
import pandas as pd
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

trace = go.Ohlc(x=df['Date'],
                open=df['AAPL.Open'],
                high=df['AAPL.High'],
                low=df['AAPL.Low'],
                close=df['AAPL.Close'])
data = [trace]
py.iplot(data, filename='plutus/plotlytest.png')

fc.sendMail("plotly","plotly","plutus/plotlytest.png")
'''
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.dates import (MONDAY, DateFormatter, MonthLocator,
                              WeekdayLocator, date2num)

from mpl_finance import candlestick2_ohlc
import fortunacommon

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')
print(df)

fig, ax = plt.subplots()

print("before plot")
#candlestick_ohlc(ax, zip(df['Date'],df['AAPL.Open'], df['AAPL.High'],df['AAPL.Low'], df['AAPL.Close']))
candlestick2_ohlc(ax, df['AAPL.Open'], df['AAPL.High'],df['AAPL.Low'], df['AAPL.Close'])
print("after plot")

#ax.autoscale_view()
#ax.xaxis.grid(True, 'major')
#ax.grid(True)

#fig.autofmt_xdate()

#f=plt.get_figure()
fig.savefig("/home/ec2-user/plutus/candleplot.png")
fortunacommon.sendMail("candleplot","candleplot","/home/ec2-user/plutus/candleplot.png")
