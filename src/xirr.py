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
		xirrBuyData = {
			"date": datetime.datetime.strptime(row['buyDate'],"%d-%b-%y"),
			"value": buy
		}
		xirrSellData = {
			"date": currentDate,
			"value": sell
		}
		xirrList.append(xirrBuyData)
		xirrList.append(xirrSellData)
	#dfCashFlow=pd.DataFrame(xirrList)
	return xirrList

# ------------
# MAIN PROGRAM
# ------------

'''
cftest = [(datetime.datetime.strptime("25-Sep-2017","%d-%b-%Y"), -10001), (datetime.datetime.strptime("27-Dec-2018","%d-%b-%Y"), 11140)]
print(cftest)
print(xirr(cftest))
'''
# Read portfolio data from file
df1=getDataFromFile("/home/ec2-user/fortuna/fortuna/data/pfdata.tsv")
# Use only required columns, and drop unwanted columns
df2=df1[['company','buyDate','unitPrice','qty','cmp']]
# Get Unique list of companies
companyList=df2.company.unique().tolist()
# Iterate for eac company
for companyName in companyList:
	# Filter rows for specific company
	df3=df2[df2.company==companyName]
	print("===== ",companyName," =====")
	print(df3)
	# Convert PF data to cash flow data
	cashflows=getCashFlowData(df3)
	print(cashflows)
	for (date,value) in cashflows:
		print("DATE: ",date," VAL: ",value)
	
    
