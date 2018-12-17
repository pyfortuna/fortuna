print("-----")
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
from datetime import datetime
import pandas.io.data as web
import fortunacommon as fc
import test as tt

e = datetime.datetime.now()
s = e - datetime.timedelta(days=30)
dayList = tt.get100DayList(s,e)
history_df = tt.getHistoricData('ASHOKLEY',s,e)

fig = FF.create_candlestick(history_df.ppen, history_df.high, history_df.low, history_df.close, dates=history_df.index)

py.iplot(fig, filename='plutus/plotlytest.png', validate=False)

fc.sendMail("plotly","plotly","plutus/plotlytest.png")
