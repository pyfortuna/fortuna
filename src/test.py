import fortunacommon

pr=fortunacommon.loadProperties()

quandlURL="https://www.quandl.com/api/v3/datasets/NSE/ASHOKLEY.csv?api_key=" + pr['quandl.api.key']

print(quandlURL)
