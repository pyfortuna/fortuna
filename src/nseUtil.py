'''
References:
  https://github.com/Arkoprabho/NSEToolsPy/blob/master/nsetools/nse.py
  https://docs.python.org/3.4/howto/urllib2.html#headers
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE
  https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=+&fromDate=01-12-2018&toDate=07-12-2018&dataType=PRICEVOLUMEDELIVERABLE
'''

import datetime
import urllib.request
#import matplotlib
import pandas as pd
#import candleplot as cplot

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
            'series' : 'EQ', #2018/12/27: Changed ALL to EQ
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
# Function to get Historical price
# -----------------------------------------------
def getHistoricPrice(companyName, startDate, endDate):
  dayList = get100DayList(startDate,endDate)
  history_df = pd.DataFrame()
  for dayRange in dayList:
    req=getRequest(companyName,dayRange['start'],dayRange['end'])
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

  o_df=history_df[['open','high','low','close','vwap']]
  return o_df
