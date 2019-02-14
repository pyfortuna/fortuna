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
	companyCode='PIDILITIND'	
	e = datetime.datetime.now()
	s = e - datetime.timedelta(days=700)
	df = nu.getHistoricPrice(companyCode,s,e)	
	confDF = pd.read_table('/home/ec2-user/fortuna/fortuna/data/s01conf.tsv', header=0)
	paramList = confDF.to_dict('records')
	res = pd.DataFrame()
	
	for param in paramList:
		# get recommendation
		s1 = s01.Strategy01()
		txnList = s1.executeStrategy(param,df)
		# test recommendation
		pf = p.Portfolio(param['id'])
		pf.addCapital('2017-01-01',capital)
		pf.processTxnList(txnList)
		pf.printSummary()
		#pf.printBalanceSheet()
		#pf.printBalanceSheet('TRD')
		resultDF=pf.getResult()
		res = res.append(resultDF)
	print(res)
