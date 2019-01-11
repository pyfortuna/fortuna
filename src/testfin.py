import pandas as pd
dfList=pd.read_html('https://www.moneycontrol.com/financials/abbindia/results/yearly/ABB#ABB')
for df in dfList:
  print(list(df))
  print(df.head())
