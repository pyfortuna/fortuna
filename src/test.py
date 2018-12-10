'''
References:
  https://github.com/Arkoprabho/NSEToolsPy/blob/master/nsetools/nse.py
  https://docs.python.org/3.4/howto/urllib2.html#headers
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-12-2018&toDate=07-12-2018&dataType=PRICEVOLUMEDELIVERABLE
'''

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

def nse_headers():
    return {'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Host': 'nseindia.com',
            'Referer': "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0&smeFlag=0&itpFlag=0",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
            'X-Requested-With': 'XMLHttpRequest'
            }

nseURL="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?"
values = {'symbol' : 'ASHOKLEY',
          'segmentLink' : '3',
          'symbolCount' : '1',
          'series' : 'ALL',
          'dateRange' : '3month',
          'fromDate' : '',
          'toDate' : '',
          'dataType' : 'PRICEVOLUMEDELIVERABLE' }

headers = nse_headers()
data = urllib.parse.urlencode(values)
data = data.encode('ascii')
req = urllib.request.Request(nseURL, data, headers)
with urllib.request.urlopen(req) as response:
   the_page = response.read()

history_df=pd.read_html(the_page, header=0, index_col='Date')[0]
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

mavg = boll_df['close'].rolling(20).mean()
mstd = boll_df['close'].rolling(20).std()
hband = mavg + 2*mstd
lband = mavg - 2*mstd
#boll_df['hband']=pd.Series(hband, name='hband')
#boll_df['lband']=pd.Series(lband, name='lband')
boll_df=boll_df.assign(sma20=mavg)
boll_df=boll_df.assign(hband=hband)
boll_df=boll_df.assign(lband=lband)
boll_df=boll_df.assign(reco=None)
#recoList=boll_df['reco']
#recoList="-"
#if boll_df['close'] < lband:
#  recoList="BUY"
#boll_df=boll_df.assign(reco=recoList)




def getReco(row):
    if (row.close < row.lband) :
        return "[ B ]"
    elif (row.close > row.hband) :
        return "[ S ]"
    else:
        return "[   ]"

boll_df.loc[:, 'reco'] = boll_df.apply(getReco, axis = 1)






def getTrend(row):
    if (row.uptrend) :
        return "[ U ]"
    else:
        return "[ D ]"

boll_df=boll_df.assign(uptrend=None)
boll_df['uptrend'] = boll_df.close.ge(boll_df.close.shift())
boll_df=boll_df.assign(trend=None)
boll_df.loc[:, 'trend'] = boll_df.apply(getTrend, axis = 1)
boll_df=boll_df.drop(columns=['uptrend'])

print(boll_df.round(2))

