import pandas as pd

dfPF = pd.read_csv("/home/ec2-user/plutus/pf.csv")[['companyName','currentValue']]
dfFinYr = pd.read_csv("/home/ec2-user/plutus/finYr.csv")[['companyShortName','pl_coef','eps_coef']]
print(dfPF)
print(dfFinYr)

res=pd.merge(dfPF, dfFinYr, left_on=['companyName'], right_on=['companyShortName'])
res1=res.sort_values(by='eps_coef', ascending=False)
print(res1)
