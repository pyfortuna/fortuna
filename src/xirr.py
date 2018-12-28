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
	cfList=[]
	for index, row in df.iterrows():
		buy=round(-1 * row['unitPrice'] * row['qty'],2)
		sell=round(row['cmp'] * row['qty'],2)
		cfList.append(tuple((datetime.datetime.strptime(row['buyDate'],"%d-%b-%y"), buy)))
		cfList.append(tuple((currentDate, sell)))
	return cfList

def processPF(df):
	companyList=df.company.unique().tolist()
	companyList=['Reliance','TCS','Vakrangee']
	xirrList=[]
	for companyName in companyList:
		dfCF=df[df.company==companyName]
		print(dfCF)
		cashflows=getCashFlowData(dfCF)
		print(cashflows)
		x=xirr(cashflows)*100
		xirrData = {
			"companyName": companyName,
			"xirr": x
			}
		xirrList.append(xirrData)
	xirrDF=pd.DataFrame(xirrList)
	xirrDF=xirrDF.set_index("companyName")
	return xirrDF

# ------------
# MAIN PROGRAM
# ------------
df1=getDataFromFile("/home/ec2-user/fortuna/fortuna/data/pfdata.tsv")
df2=df1[['company','buyDate','unitPrice','qty','cmp']]
xirrDF=processPF(df2)
pd.options.display.float_format = '{:,.2f}'.format
print(xirrDF.sort_values(by=['xirr'],ascending=False))
