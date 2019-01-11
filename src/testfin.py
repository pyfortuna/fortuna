import pandas as pd
df=pd.read_html('https://www.moneycontrol.com/financials/abbindia/ratiosVI/ABB#ABB')[3]
df=df[df[0]=='Current Ratio (X)']
print(df)
