'''
References:
  https://github.com/Arkoprabho/NSEToolsPy/blob/master/nsetools/nse.py
  https://docs.python.org/3.4/howto/urllib2.html#headers
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-12-2018&toDate=07-12-2018&dataType=PRICEVOLUMEDELIVERABLE
'''

import datetime
import nseUtil as nu
import fortunacommon
#import urllib.request
import matplotlib
import pandas as pd
import candleplot as cplot


# -----------------------------------------------
# MAIN PROGRAM
# -----------------------------------------------
e = datetime.datetime.now()
s = e - datetime.timedelta(days=60)
history_df = nu.getHistoricPrice('ASHOKLEY',s,e)

# ------------------------------------------------------------------------------------------------
# Bollinger Bands
#  https://en.wikipedia.org/wiki/Bollinger_Bands
#  https://github.com/bukosabino/ta/blob/5e8e92bd9e41eec559a3dd849d1bfe9143cf84ae/ta/volatility.py
# ------------------------------------------------------------------------------------------------
boll_df=history_df[['close']]

sma20 = boll_df['close'].rolling(20).mean()
mstd = boll_df['close'].rolling(20).std()
hband = sma20 + 2*mstd
lband = sma20 - 2*mstd
hband_1_20 = sma20 + mstd
lband_1_20 = sma20 - mstd
bbw = mstd/sma20*100

boll_df=boll_df.assign(sma20=sma20)
boll_df=boll_df.assign(hband=hband)
boll_df=boll_df.assign(lband=lband)
boll_df=boll_df.assign(hband_1_20=hband_1_20)
boll_df=boll_df.assign(lband_1_20=lband_1_20)
boll_df=boll_df.assign(bbw=bbw)

# Find Bollinger Band Position
def getBBPos(row):
    if (row.close < row.lband) :
        return "BL"
    elif (row.close > row.lband) and (row.close < row.sma20) :
        return "LB"
    elif (row.close > row.sma20) and (row.close < row.hband) :
        return "UB"
    elif (row.close > row.hband) :
        return "AU"
    else:
        return "  "
boll_df.loc[:, 'bb'] = boll_df.apply(getBBPos, axis = 1)


# Find Double Bollinger Band Position
def getDoubleBBPos(row):
    if (row.close < row.lband) :
        return " BSZ "
    elif (row.close >= row.lband) and (row.close < row.lband_1_20) :
        return " *SZ "
    elif (row.close >= row.lband_1_20) and (row.close < row.sma20) :
        return " NZ2 "
    elif (row.close >= row.sma20) and (row.close < row.hband_1_20) :
        return " NZ1 "
    elif (row.close >= row.hband_1_20) and (row.close < row.hband) :
        return " *BZ "
    elif (row.close >= row.hband) :
        return " ABZ "
    else:
        return "  "
boll_df.loc[:, 'dbb'] = boll_df.apply(getDoubleBBPos, axis = 1)


# Create Trend List
sma20List=list(boll_df['sma20'])
trendList = []
trendList.append('-')
i = 1
while i < len(sma20List):
  if sma20List[i] > sma20List[i-1]:
    trendList.append('U')
  else:
    trendList.append('D')
  i += 1

  
# Create Trend Strength List
trendStrengthList = []
trendStrengthList.append(0)
i = 1
while i < len(trendList):
  if trendList[i] != trendList[i-1]:
    trendStrengthList.append(1)
  else:
    trendStrengthList.append(trendStrengthList[i-1]+1)
  i += 1


# Create Trend List
bbwList=list(boll_df['bbw'])
bbwMin=min(bbwList[20:])
bbwMax=max(bbwList[20:])
bbwRatioList = ['-']*20
bbwRatioTrendList = ['-']*20

i = 20
while i < len(bbwList):
  bbwRatio = (bbwList[i]-bbwMin)/(bbwMax-bbwMin)*9+1
  bbwRatioList.append(round(bbwRatio))
  if bbwRatioList[i-1] == '-':
    bbwRatioTrendList.append('-')
  else:
    if bbwRatioList[i] > bbwRatioList[i-1]:
      bbwRatioTrendList.append('U')
    elif bbwRatioList[i] < bbwRatioList[i-1]:
      bbwRatioTrendList.append('D')
    else:
      bbwRatioTrendList.append(bbwRatioTrendList[i-1])
  
  i += 1


# Add Trend list and Trend strength list to dataframe
se1 = pd.Series(trendList)
boll_df['trend'] = se1.values
se2 = pd.Series(trendStrengthList)
boll_df['strength'] = se2.values
se3 = pd.Series(bbwRatioList)
boll_df['bbwr'] = se3.values
se4 = pd.Series(bbwRatioTrendList)
boll_df['bbwrt'] = se4.values

# Prediction logic
def getPrediction(row):
    if (row.strength >= 10) and (row.bbwrt == "D") and (row.bbwr < 3):
        return "breakout"
    else:
        return ""
boll_df.loc[:, 'prediction'] = boll_df.apply(getPrediction, axis = 1)

# Print output
print(boll_df[['close','trend', 'strength','bb','bbwr','bbwrt','prediction']].round(1).to_string())

# Create output file
boll_df[['close','trend', 'strength','bb','bbwr','bbwrt','prediction']].to_csv("/home/ec2-user/plutus/bbout.csv")
#fortunacommon.sendMail("Data","SMA Data","/home/ec2-user/plutus/bbout.csv")

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
fortunacommon.sendMail("Candle","Candle",o_file)
