import fortunacommon

pr=fortunacommon.loadAppProperties()

quandlURL="https://www.quandl.com/api/v3/datasets/NSE/ASHOKLEY.csv?api_key=" + pr['quandl.api.key']

print(quandlURL)

with urlopen(quandlURL) as response:
  for line in response:
    print(line)
