import nseUtil as nu
import datetime
import pandas as pd

'''
	Test program
'''
if __name__ == "__main__":
	e = datetime.datetime.now()
	s = e - datetime.timedelta(days=700)
	res = pd.DataFrame()
	confDF = pd.read_table('/home/ec2-user/fortuna/fortuna/data/nselist.tsv', header=0)
	companyList = confDF['companyCode'].unique()
	companyList.sort()
	for companyCode in companyList:
		df = nu.getHistoricPrice(companyCode,s,e)
    		output_filename = '/home/ec2-user/plutus/nsedata/%s.csv' % companyCode
    		df.to_csv(output_filename)
    		print('DEBUG : Saved data for %s' % companyCode)
	print('DEBUG : Completed')
