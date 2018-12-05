import pandas as pd

dfPF = pd.read_csv("/home/ec2-user/plutus/pf.csv")
dfFinYr = pd.read_csv("/home/ec2-user/plutus/finYr.csv")
print(dfPF)
print(dfFinYr)

res=pd.merge(dfPF, dfFinYr, left_on=['companyName'], right_on=['companyShortName'])
print(res)
