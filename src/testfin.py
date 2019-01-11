import pandas as pd
df=pd.read_html('https://www.moneycontrol.com/financials/abbindia/results/yearly/ABB#ABB')[3]
print(df)
