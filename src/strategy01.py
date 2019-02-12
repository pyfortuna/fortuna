import nseUtil as nu
import datetime
import pandas as pd

class Strategy01:
	def executeStrategy(self,capital,df):
		sma200 = df['close'].rolling(200).mean()
		df=df.assign(sma200=sma200)
		df=df.dropna()
		# Create Trend List
		sma200List=list(df['sma200'])
		trendList = []
		trendList.append('-')
		i = 1
		while i < len(sma200List):
			if sma200List[i] > sma200List[i-1]:
				trendList.append('U')
			else:
				trendList.append('D')
			i += 1
		# Create Trend Strength List
		trendStrengthList = []
		trendStrengthList.append(0)
		i = 1
		while i < len(trendList):
			if trendList[i] != trendList[i-1]:
				trendStrengthList.append(1)
			else:
				trendStrengthList.append(trendStrengthList[i-1]+1)
			i += 1
		se1 = pd.Series(trendList)
		df['trend'] = se1.values
		se2 = pd.Series(trendStrengthList)
		df['strength'] = se2.values
		print(df[['close','sma200','trend','strength']].to_string())
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
