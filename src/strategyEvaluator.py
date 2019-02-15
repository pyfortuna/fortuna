import nseUtil as nu
import datetime
import pandas as pd
import strategy01 as s01
import portfolio as p

'''
	Test program
'''
if __name__ == "__main__":
	e = datetime.datetime.now()
	s = e - datetime.timedelta(days=700)
	res = pd.DataFrame()
	confDF = pd.read_table('/home/ec2-user/fortuna/fortuna/data/s01conf.tsv', header=0)
	companyList = confDF['companyCode'].unique()
	for companyCode in companyList:
		compConfDF = confDF.loc[confDF['companyCode']==companyCode][['id','capital','smaDays','trendStrength']]
		df = nu.getHistoricPrice(companyCode,s,e)		
		paramList = compConfDF.to_dict('records')
		for param in paramList:
			# get recommendation
			s1 = s01.Strategy01()
			txnList = s1.executeStrategy(param,df)
			# test recommendation
			pf = p.Portfolio("%s:%d" % (companyCode, param['id']))
			pf.addCapital('2017-01-01',param['capital'])
			pf.processTxnList(txnList)
			#pf.printSummary()
			#pf.printBalanceSheet()
			#pf.printBalanceSheet('TRD')
			resultDF=pf.getResult()
			res = res.append(resultDF)
	print(res)
