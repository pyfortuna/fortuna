'''
References:
  https://github.com/Arkoprabho/NSEToolsPy/blob/master/nsetools/nse.py
  https://docs.python.org/3.4/howto/urllib2.html#headers
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-12-2018&toDate=07-12-2018&dataType=PRICEVOLUMEDELIVERABLE
'''

import datetime
import fortunacommon
import urllib.request
import pandas as pd

pr=fortunacommon.loadAppProperties()

'''
quandlURL="https://www.quandl.com/api/v3/datasets/NSE/ASHOKLEY.csv?api_key=" + pr['quandl.api.key']
with urlopen(quandlURL) as response:
  for line in response:
    dataLine=str(line.strip()).replace("b","").replace("'","")
    print(dataLine)
'''

# ------------------------------
# Return header for HTTP Request
# ------------------------------
def nse_headers():
    return {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'nseindia.com',
            'Referer': "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0&smeFlag=0&itpFlag=0",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
            'X-Requested-With': 'XMLHttpRequest'
            }


# ------------------------
# Return HTTP Request data
# ------------------------
def getRequest(symbol, fromDt, toDt):
  nseURL="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?"
  values = {'symbol' : symbol,
            'segmentLink' : '3',
            'symbolCount' : '1',
            'series' : 'ALL',
            'dateRange' : '',
            'fromDate' : fromDt,
            'toDate' : toDt,
            'dataType' : 'PRICEVOLUMEDELIVERABLE' }
  data = urllib.parse.urlencode(values)
  data = data.encode('ascii')
  headers = nse_headers()
  req = urllib.request.Request(nseURL, data, headers)
  return req

# -----------------------------------------------
# Function to split duration to batch of 100 days
#  - Due to restriction in NSE URL
# -----------------------------------------------
def get100DayList(start, end):
  NSE_DATE_FMT="%d-%m-%Y"
  dates={}
  datesList = []
  difference = (end - start).days
  if difference > 100:
    curr_end = start + datetime.timedelta(days=100)
    while curr_end <= end:
      dates['start']=start.strftime(NSE_DATE_FMT)
      dates['end']=curr_end.strftime(NSE_DATE_FMT)
      datesList.append(dates.copy())
      start = curr_end + datetime.timedelta(days=1)
      curr_end += datetime.timedelta(days=100)
    if start < end:
      dates['start']=start.strftime(NSE_DATE_FMT)
      dates['end']=end.strftime(NSE_DATE_FMT)
      datesList.append(dates.copy())
  else:
    dates['start']=start.strftime(NSE_DATE_FMT)
    dates['end']=end.strftime(NSE_DATE_FMT)
    datesList.append(dates.copy())
  return datesList

# -----------------------------------------------
# MAIN PROGRAM
# -----------------------------------------------
e = datetime.datetime.now()
s = e - datetime.timedelta(days=120)
dayList = get100DayList(s,e)
history_df = pd.DataFrame()

for dayRange in dayList:
  req=getRequest('DABUR',dayRange['start'],dayRange['end'])
  with urllib.request.urlopen(req) as response:
     the_page = response.read()
  history_df=history_df.append(pd.read_html(the_page, header=0, index_col='Date')[0])


history_df.rename(columns={'Open Price':'open',
                            'High Price':'high',
                            'Low Price':'low',
                            'Close Price':'close',
                            'VWAP':'vwap',
                            'Total Traded Quantity':'qty'}, 
                            inplace=True)

input_df=history_df[['open','high','low','close','vwap']]
#print(input_df)

d_df=input_df.diff()
#print(d_df.query('close == close'))

sma_df=input_df.rolling(window=30).mean().round(2).diff()
#print(sma_df.query('close > 0'))
#print(sma_df.query('close == close'))

# Bollinger Bands
#  https://en.wikipedia.org/wiki/Bollinger_Bands
#  https://github.com/bukosabino/ta/blob/5e8e92bd9e41eec559a3dd849d1bfe9143cf84ae/ta/volatility.py
boll_df=history_df[['close']]
#print(boll_df)

sma20 = boll_df['close'].rolling(20).mean()
mstd = boll_df['close'].rolling(20).std()
hband = sma20 + 2*mstd
lband = sma20 - 2*mstd
hband_1_20 = sma20 + mstd
lband_1_20 = sma20 - mstd
bbw = mstd/sma20*100
#boll_df['hband']=pd.Series(hband, name='hband')
#boll_df['lband']=pd.Series(lband, name='lband')
boll_df=boll_df.assign(sma20=sma20)
boll_df=boll_df.assign(hband=hband)
boll_df=boll_df.assign(lband=lband)
boll_df=boll_df.assign(hband_1_20=hband_1_20)
boll_df=boll_df.assign(lband_1_20=lband_1_20)
boll_df=boll_df.assign(bbw=bbw)
boll_df=boll_df.assign(bb=None)
#recoList=boll_df['reco']
#recoList="-"
#if boll_df['close'] < lband:
#  recoList="BUY"
#boll_df=boll_df.assign(reco=recoList)




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





def getTrend(row):
    if (row.uptrend) :
        return "U"
    else:
        return "D"
'''
boll_df=boll_df.assign(uptrend=None)
boll_df['uptrend'] = boll_df.sma20.ge(boll_df.sma20.shift())
'''

sma20List=list(boll_df['sma20'])
trendList = []
trendList.append('-')
i = 1
while i < len(sma20List):
  if i > 0:
    if sma20List[i] > sma20List[i-1]:
      trendList.append('U')
    else:
      trendList.append('D')

trendStrengthList = []
trendStrengthList.append(0)
i = 1
while i < len(trendList):
  if index > 0:
    if trendList[i] != trendList[i-1]:
      trendStrengthList.append(1)
    else:
      trendStrengthList.append(trendStrengthList[i-1]+1)

se1 = pd.Series(trendList)
boll_df['trend'] = se1.values
se2 = pd.Series(trendStrengthList)
boll_df['strength'] = se2.values

'''
boll_df=boll_df.assign(trend=None)
boll_df.loc[:, 'trend'] = boll_df.apply(getTrend, axis = 1)

boll_df=boll_df.assign(strength=None)
#boll_df.loc[:, 'strength'] = boll_df.groupby('uptrend').cumsum()+1
#print(boll_df[['uptrend']])
#print(boll_df.groupby('uptrend')[['uptrend']])

boll_df=boll_df.drop(columns=['uptrend'])
'''

print(boll_df[['close','trend', 'strength','bb','dbb']].round(2).to_string())

#boll_df[['close','trend','bb','dbb']].to_csv("/home/ec2-user/plutus/bb_out.csv")
