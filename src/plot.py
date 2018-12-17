print("-----")
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import fortunacommon as fc
import test as tt

e = datetime.now()
s = e - timedelta(days=30)
history_df = tt.getHistoricData('ASHOKLEY',s,e)

trace = go.Ohlc(x=history_df.index, open=history_df.open, high=history_df.high, low=history_df.low, close=history_df.close)
data = [trace]
py.iplot(data, filename='plutus/plotlytest.png', validate=False)

fc.sendMail("plotly","plotly","plutus/plotlytest.png")
