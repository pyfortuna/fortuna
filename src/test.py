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

nseURL="https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ASHOKLEY&segmentLink=3&symbolCount=1&series=ALL&dateRange=12month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE"

fp = urllib.request.urlopen(nseURL)
res = fp.read()

history_df = pd.read_html(res, header=0, index_col='Date')[0]

print(history_df)
