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

'''
cftest = [(datetime.datetime.strptime("25-Sep-2017","%d-%b-%Y"), -10001), (datetime.datetime.strptime("27-Dec-2018","%d-%b-%Y"), 11140)]
print(cftest)
print(xirr(cftest))
'''

def getData(df):
	currentDate = datetime.datetime.now().strftime("%d-%b-%y")
	xirrList=[]
	for index, row in df.iterrows():
		buy=row['unitPrice'] * row['qty'] * -1
		sell=row['cmp'] * row['qty']
		xirrBuyData = {
			"date": row['buyDate'],
			"value": buy
		}
		xirrSellData = {
			"date": currentDate,
			"value": sell
		}
		xirrList.append(xirrBuyData)
		xirrList.append(xirrSellData)
	dfOut=pd.DataFrame(xirrList)
	return dfOut

# ------------
# MAIN PROGRAM
# ------------
df1=getDataFromFile("/home/ec2-user/fortuna/fortuna/data/pfdata.tsv")
df2=df1[['company','buyDate','unitPrice','qty','cmp']]
companyList=df2.company.unique().tolist()
for companyName in companyList:
	df3=df2[df2.company==companyName]
	print("===== ",companyName," =====")
	print(df3)
	xirrList=getData(df3)
	print(xirrList)
    
