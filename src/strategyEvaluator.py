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
	# get recommendation
	s1 = s01.Strategy01()
	txnList = s1.executeStrategy(capital,df)
	# test recommendation
	pf = p.Portfolio()
	pf.addCapital('2017-01-01',capital)
	pf.processTxnList(txnList)
	pf.printSummary()
	pf.printBalanceSheet()
	pf.printBalanceSheet('TRD')
	b=pf.getBalance()
	if(b==0):
		print('BALANCESHEET : OK')
	else:
		print('BALANCESHEET : ERROR')
	g,n=pf.getResults()
	c=pf.getcashBalance()
	i=pf.getInventoryBalance()
	print('GROSS P/L    : %6.2f' % g)
	print('NET P/L      : %6.2f' % n)
	print('CASH BALANCE : %6.2f' % c)
	print('INV BALANCE  : %6.2f' % i)
