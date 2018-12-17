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

from mpl_finance import plot_day_summary_oclh


df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

fig, ax = plt.subplots()
plot_day_summary_oclh(ax, zip(df['Date'],df['AAPL.Open'], df['AAPL.Close'],df['AAPL.Low'], df['AAPL.High']))

ax.autoscale_view()
ax.xaxis.grid(True, 'major')
ax.grid(True)

fig.autofmt_xdate()

f=plt.get_figure()
f.savefig("/home/ec2-user/plutus/candleplot.png")
fortunacommon.sendMail("candleplot","candleplot","/home/ec2-user/plutus/candleplot.png")
