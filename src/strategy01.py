import nseUtil as nu
import datetime
import pandas as pd

def units(amount, price):
	return int(amount/price)

class Strategy01:
	def executeStrategy(self,capital,df):
		# -----------
		# Paramters
		# -----------
		SMA_DAYS = 50
		# -----------
		# Pre-process
		# -----------
		sma = df['close'].rolling(SMA_DAYS).mean()
		df=df.assign(sma=sma)
		df=df.dropna()
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
		se1 = pd.Series(trendList)
		df['trend'] = se1.values
		se2 = pd.Series(trendStrengthList)
		df['strength'] = se2.values
		print(df.tail(20))
		# -----------
		# Process
		# -----------
		#dfBuy=df.loc[(df['trend'] == 'U') & (df['strength'] == 5)]
		#dfSell=df.loc[(df['trend'] == 'D') & (df['strength'] == 5)]
		dfRes=df.loc[(df['strength'] == 5)][['close','sma','trend']]
		print('-'*25)
		print(dfRes)
		#print('-'*25)
		#print(dfSell)
		#print('-'*25)
		txnList=[]
		invQty=0
		balance=capital
		for index, row in dfRes.iterrows():
			if(row['trend']=='D'): # BUY
				price = row['close']
				qty=units(balance,price)
				balance -= (qty * price)
				invQty += qty
				txn = {'txnType': 'BUY', 'date':row.name.strftime('%Y-%m-%d'), 'price': price, 'qty': qty}
				txnList.append(txn)
			elif(row['trend']=='S' and invQty>0): # SELL
				price = row['close']
				qty=invQty
				balance += (qty * price)
				invQty = 0
				txn = {'txnType': 'SELL', 'date':row.name.strftime('%Y-%m-%d'), 'price': price, 'qty': qty}
				txnList.append(txn)
		print(txnList)
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
