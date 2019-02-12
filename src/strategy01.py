import nseUtil as nu
import datetime

class Strategy01:
	def executeStrategy(capital,df):
		print(df.tail(20))
'''
	Test program
'''
if __name__ == "__main__":
	capital=10000
	companyCode='RELIANCE'	
	e = datetime.datetime.now()
	s = e - datetime.timedelta(days=700)
	df = nu.getHistoricPrice(companyCode,s,e)
	s1 = Strategy01()
	s1.executeStrategy(capital,df)
