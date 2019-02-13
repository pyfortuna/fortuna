import nseUtil as nu
import datetime
import pandas as pd
import strategy01 as s01
import portfolio as p

'''
	Test program
'''
if __name__ == "__main__":
	capital=10000
	companyCode='RELIANCE'	
	e = datetime.datetime.now()
	s = e - datetime.timedelta(days=700)
	df = nu.getHistoricPrice(companyCode,s,e)
	param1 = {'capital':capital,'smaDays':5,'trendStrength':5}
	
	# get recommendation
	s1 = s01.Strategy01()
	txnList = s1.executeStrategy(param1,df)
	# test recommendation
	pf = p.Portfolio()
	pf.addCapital('2017-01-01',capital)
	pf.processTxnList(txnList)
	pf.printSummary()
	#pf.printBalanceSheet()
	pf.printBalanceSheet('TRD')
	resultDF=pf.getResult()
	print(resultDF)
