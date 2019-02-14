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
	lastDate = df.index(-1)
	lastPrice = df['close'](-1)
	print('------------------')
	print(lastDate)
	print(lastPrice)
	print('------------------')
	
	paramList = []
	paramList.append({'id':1,'capital':capital,'smaDays':30,'trendStrength':5})
	paramList.append({'id':2,'capital':capital,'smaDays':50,'trendStrength':5})
	paramList.append({'id':3,'capital':capital,'smaDays':100,'trendStrength':5})
	paramList.append({'id':4,'capital':capital,'smaDays':150,'trendStrength':5})
	paramList.append({'id':5,'capital':capital,'smaDays':30,'trendStrength':10})
	paramList.append({'id':6,'capital':capital,'smaDays':50,'trendStrength':10})
	paramList.append({'id':7,'capital':capital,'smaDays':100,'trendStrength':10})
	paramList.append({'id':8,'capital':capital,'smaDays':150,'trendStrength':10})
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
