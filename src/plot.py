print("-----")
import plotly.plotly as py
from plotly.tools import FigureFactory as FF
from datetime import datetime
import pandas.io.data as web
import fortunacommon as fc

df = web.DataReader("aapl", 'yahoo', datetime(2007, 10, 1), datetime(2009, 4, 1))

fig = FF.create_candlestick(df.Open, df.High, df.Low, df.Close, dates=df.index)

py.iplot(fig, filename='plutus/plotlytest.png', validate=False)

fc.sendMail("plotly","plotly","plutus/plotlytest.png")
