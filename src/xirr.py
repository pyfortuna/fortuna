# https://codereview.stackexchange.com/questions/179099/user-defined-xirr-function-exception-handling

import datetime
from scipy import optimize
import pandas as pd

def xnpv(rate, cashflows):
    t0 = min(cashflows, key = lambda t: t[0])[0]
    return sum([cf/(1+rate)**((t-t0).days/365.0) for (t,cf) in cashflows])

def xirr(cashflows,guess=0.1):
    try:
        outc = optimize.newton(lambda r: xnpv(r, cashflows), guess, maxiter=100)
        if outc.imag == 0:
            return outc
        else:
            raise
    except (RuntimeError, OverflowError):
        try:
            outc = optimize.newton(lambda r: xnpv(r, cashflows), -guess, maxiter=100)
            if outc.imag == 0:
                return outc
            else:
                raise
        except (RuntimeError, OverflowError):
            return float("NaN")

def getDataFromFile(filePath):
    df=pd.read_table(filePath)
    return df

def getCashFlowData(df):
	currentDate = datetime.datetime.now() #.strftime("%d-%b-%y")
	xirrList=[]
	for index, row in df.iterrows():
		buy=row['unitPrice'] * row['qty'] * -1
		sell=row['cmp'] * row['qty']
		xirrList.append(tuple((datetime.datetime.strptime(row['buyDate'],"%d-%b-%y"), buy)))
		xirrList.append(tuple((currentDate, sell)))
	return xirrList

# ------------
# MAIN PROGRAM
# ------------

'''
cftest = [(datetime.datetime.strptime("25-Sep-17","%d-%b-%y"), -10001), (datetime.datetime.strptime("27-Dec-18","%d-%b-%y"), 11140)]
print(cftest)
print(xirr(cftest))
'''

df1=getDataFromFile("/home/ec2-user/fortuna/fortuna/data/pfdata.tsv")
df2=df1[['company','buyDate','unitPrice','qty','cmp']]
companyList=df2.company.unique().tolist()
xirrList=[]
for companyName in companyList:
	df3=df2[df2.company==companyName]
	cashflows=getCashFlowData(df3)
	x=round(xirr(cashflows)*100,2)
	xirrData = {
		"companyName": companyName,
		"xirr": x
		}
	xirrList.append(xirrData)
xirrDF=pd.DataFrame(xirrList)
xirrDF=xirrDF.set_index("companyName")
print(xirrDF)
print(xirrDF.sort_values(by=['companyName']))
