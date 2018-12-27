'''
References:
  https://github.com/Arkoprabho/NSEToolsPy/blob/master/nsetools/nse.py
  https://docs.python.org/3.4/howto/urllib2.html#headers
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-12-2018&toDate=07-12-2018&dataType=PRICEVOLUMEDELIVERABLE
'''

import datetime
#import nseUtil as nu
import fortunacommon
#import urllib.request
import matplotlib
import pandas as pd
import candleplot as cplot
import bollingerUtil as bu

# -----------------------------------------------
# MAIN PROGRAM
# -----------------------------------------------
def process(companyCode):
  print('-'*40)
  print(companyCode)
  boll_df = bu.processBB(companyCode)
  # Print output
  print(boll_df[['close','trend', 'strength','bb','bbwr','bbwrt','bbpos','prediction']].tail(10).round(1).to_string())
  # Create output file
  boll_df[['close','trend', 'strength','bb','bbwr','bbwrt','prediction']].to_csv("/home/ec2-user/plutus/bbout.csv")
  #fortunacommon.sendMail("Data","SMA Data","/home/ec2-user/plutus/bbout.csv")

process('ASHOKLEY')
process('SUPRAJIT')
process('IBULHSGFIN')
process('TATAMOTORS')
'''
# -----------
# SMA Plot
# -----------
plot_df=boll_df[['close','sma20', 'hband','lband','hband_1_20','lband_1_20']]
plot_df=plot_df.dropna()
plot = plot_df.plot(color = ['xkcd:darkblue','xkcd:grey','xkcd:grey','xkcd:grey','xkcd:grey','xkcd:grey'], figsize=(12, 8), legend=False)
fig = plot.get_figure()
fig.savefig("/home/ec2-user/plutus/smaplot.png")
#fortunacommon.sendMail("Plot","SMA Plot","/home/ec2-user/plutus/smaplot.png")


# -----------
# Candle Plot
# -----------
bplot_df=history_df[['open','close','high','low']]
bplot_df=bplot_df.dropna()
print(bplot_df)
o_file="/home/ec2-user/plutus/candle.png"
cplot.plotCandlestick(bplot_df,o_file,'%d-%b-%Y')
#fortunacommon.sendMail("Candle","Candle",o_file)
'''


