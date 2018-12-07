'''
References:
  https://github.com/Arkoprabho/NSEToolsPy/blob/master/nsetools/nse.py
  https://docs.python.org/3.4/howto/urllib2.html#headers
'''

import fortunacommon
import urllib.request
import pandas as pd

pr=fortunacommon.loadAppProperties()

'''
quandlURL="https://www.quandl.com/api/v3/datasets/NSE/ASHOKLEY.csv?api_key=" + pr['quandl.api.key']

print(quandlURL)

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
          'dateRange' : '1month',
          'fromDate' : '',
          'toDate' : '',
          'dataType' : 'PRICEVOLUMEDELIVERABLE' }

headers = nse_headers()
data = urllib.parse.urlencode(values)
data = data.encode('ascii')
req = urllib.request.Request(nseURL, data, headers)
with urllib.request.urlopen(req) as response:
   the_page = response.read()

history_df = pd.read_html(the_page, header=0, index_col='Date')[0]

print(history_df)
