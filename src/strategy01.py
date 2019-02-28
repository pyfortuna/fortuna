import nseUtil as nu
import datetime
import pandas as pd

class Strategy01:
	def executeStrategy(self,param,df):
		# -----------
		# Paramters
		# -----------
		SMA_DAYS = param['smaDays']
		TREND_STRENGTH = param['trendStrength']
		capital = param['capital']
		START_DATE = datetime.datetime.strptime('2018-01-01', '%Y-%m-%d')
		# -----------
		# Pre-process
		# -----------
		sma = df['close'].rolling(SMA_DAYS).mean()
		df=df.assign(sma=sma)
		df=df.dropna()
		# print start date
		print('-'*25)
		print(df.index.values[0])
		df=df.loc[df.index>=START_DATE]
		print(df.index.values[0])
		print('-'*25)
		
		# Create Trend List
		smaList=list(df['sma'])
		trendList = []
		trendList.append('-')
		i = 1
		while i < len(smaList):
			if smaList[i] > smaList[i-1]:
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
		s1 = pd.Series(trendList)
		df['trend'] = s1.values
		s2 = pd.Series(trendStrengthList)
		df['strength'] = s2.values
		lastDate = df.index[-1].strftime('%Y-%m-%d')
		lastPrice = df['close'][-1]
		# -----------
		# Process
		# -----------
		dfRes=df.loc[(df['strength'] == TREND_STRENGTH)][['close','sma','trend']]
		#print('-'*25)
		#print(dfRes)
		txnList=[]
		invQty=0
		balance=capital
		for index, row in dfRes.iterrows():
			i += 1
			if(row['trend']=='D'): # BUY
				price = row['close']
				buffer = 50
				qty=int((balance-buffer)/price)
				if(qty>0):
					balance -= (qty * price)
					invQty += qty
					txn = {'txnType': 'BUY', 'date':row.name.strftime('%Y-%m-%d'), 'price': price, 'qty': qty}
					txnList.append(txn)
			elif(row['trend']=='U' and invQty>0): # SELL
				price = row['close']
				qty=invQty
				balance += (qty * price)
				invQty = 0
				txn = {'txnType': 'SELL', 'date':row.name.strftime('%Y-%m-%d'), 'price': price, 'qty': qty}
				txnList.append(txn)
		if (invQty>0):
			txn = {'txnType': 'SELL', 'date':lastDate, 'price': lastPrice, 'qty': invQty}
			txnList.append(txn)
		return txnList
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
	param = {'capital':capital,'smaDays':5,'trendStrength':5}
	txnList = s1.executeStrategy(param,df)
	print(txnList)
