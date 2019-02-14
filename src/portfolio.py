from datetime import datetime
import pandas as pd

'''
	Base class for other exceptions
'''
class Error(Exception):
	pass

'''
	Raised on invalid transactions
'''
class InvalidTransaction(Error):
	pass

'''
	Class to manage price of inventory
'''
class InventoryList:
	def __init__(self):
		self.items = []
	def add(self, price, qty):
		if (qty < 0):
			raise InvalidTransaction
		for i in range(0, int(qty)):
			self.items.append(price) 
	def remove(self, qty):
		if (len(self.items) < qty) or (qty < 0):
			raise InvalidTransaction
		totalPrice = 0;
		for i in range(0, int(qty)):
			totalPrice += self.items.pop(0)
		avgPrice = round(totalPrice/qty,2)
		return avgPrice
	def count(self):
		return len(self.items)

'''
	Class to manage portfolio & related transactions
'''
class Portfolio:
	def __init__ (self,id):
		self.id = id
		col_names =  ['ACC', 'DATE', 'DESCRIPTION', 'DR', 'CR']
		self.bsDF = pd.DataFrame(columns=col_names)
		self.invList = InventoryList()
	def calculateBuyBrokerage(self, price, qty):
		totalTrade	= price * qty
		brokerage =	0.01
		exchangeTxnCharge = round(totalTrade*0.00325/100,2)
		gst = round((brokerage + exchangeTxnCharge)*18/100,2)
		securityTxnTax = round((totalTrade*0.001),0)
		sebiTurnoverFee = round(totalTrade*15/10000000,2)
		stampDuty=round((totalTrade*0.01/100),2)
		totalCharges = brokerage + exchangeTxnCharge + gst + securityTxnTax + sebiTurnoverFee + stampDuty
		return totalCharges
	def calculateSellBrokerage(self, price, qty):
		totalTrade	= price * qty
		brokerage =	0.01
		exchangeTxnCharge = round(totalTrade*0.00325/100,2)
		gst = round((brokerage + exchangeTxnCharge)*18/100,2)
		securityTxnTax = round((totalTrade*0.001),0)
		sebiTurnoverFee = round(totalTrade*15/10000000,2)
		stampDuty=round((totalTrade*0.01/100),2)
		dpCharges = 15.93
		totalCharges = brokerage + exchangeTxnCharge + gst + securityTxnTax + sebiTurnoverFee + stampDuty + dpCharges
		return totalCharges
	def addBalanceSheetRecord(self, date, drAccount, crAccount, description, amount):
		drRecord={'ACC': drAccount, 'DATE':datetime.strptime(date, '%Y-%m-%d'), 'DESCRIPTION': description, 'DR': amount, 'CR':0}
		crRecord={'ACC': crAccount, 'DATE':datetime.strptime(date, '%Y-%m-%d'), 'DESCRIPTION': description, 'DR': 0, 'CR':amount}
		tempDF=pd.DataFrame([drRecord,crRecord])
		self.bsDF=self.bsDF.append(tempDF, sort=True)
	def addCapital(self, date, amount):
		self.addBalanceSheetRecord (date, 'TRD', 'CAP', 'Capital', amount)
	def buy(self, date, buyPrice, qty):
		brokerage = self.calculateBuyBrokerage(buyPrice, qty)
		buyAmt = (buyPrice*qty)
		self.invList.add(buyPrice, qty)
		self.addBalanceSheetRecord (date, 'INV', 'TRD', 'Buy', buyAmt)
		self.addBalanceSheetRecord (date, 'BRK', 'TRD', 'Brokerage (Buy)', brokerage)
	def sell(self, date, sellPrice, qty):
		brokerage = self.calculateSellBrokerage(sellPrice, qty)
		sellAmt = (sellPrice*qty)
		buyPrice=self.invList.remove(qty)
		buyAmt = (buyPrice*qty)
		self.addBalanceSheetRecord (date, 'TRD', 'SAL', 'Sell', sellAmt)
		self.addBalanceSheetRecord (date, 'COG', 'INV', 'Sell', buyAmt)
		self.addBalanceSheetRecord (date, 'BRK', 'TRD', 'Brokerage (Sell)', brokerage)
	def processTxnList(self, txnList):
		for txn in txnList:
			if(txn['txnType']=='BUY'):
				self.buy(txn['date'],txn['price'],txn['qty'])
			elif(txn['txnType']=='SELL'):
				self.sell(txn['date'],txn['price'],txn['qty'])
	def getBalance(self):
		tempSerBal = self.bsDF['DR'] - self.bsDF['CR']
		totBal =int(tempSerBal.sum())
		return int(totBal)
	def getInventoryBalance(self):
		return self.invList.count()
	def getcashBalance(self):
		tempDF = self.bsDF.loc[self.bsDF['ACC'] == 'TRD'][['DR', 'CR']]
		tempDF['BAL'] = tempDF['DR'] - tempDF['CR']
		cashBalance =round(tempDF['BAL'].sum(),2)
		return cashBalance
	def getPL(self):
		salCr = round(self.bsDF.loc[self.bsDF['ACC'] == 'SAL']['CR'].sum(),2)
		cogDr = round(self.bsDF.loc[self.bsDF['ACC'] == 'COG']['DR'].sum(),2)
		brkDr = round(self.bsDF.loc[self.bsDF['ACC'] == 'BRK']['DR'].sum(),2)
		grossPL = salCr - cogDr
		netPL = grossPL - brkDr
		return grossPL, netPL
	def getRatio(self):
		sales = round(self.bsDF.loc[self.bsDF['ACC'] == 'SAL']['CR'].sum(),2)
		capital = round(self.bsDF.loc[self.bsDF['ACC'] == 'CAP']['CR'].sum(),2)
		grossPL, netPL = self.getPL()
		profitMargin = round(netPL/sales*100,2)
		roce = round(netPL/capital*100,2)
		capitalTurn = round(sales/capital,2)
		return profitMargin,roce,capitalTurn
	def printBalanceSheet(self, account='none'):
		if (account=='none'):
			print(self.bsDF[['ACC', 'DATE', 'DESCRIPTION', 'DR', 'CR']])
		else:
			tempDF = self.bsDF.loc[self.bsDF['ACC'] == account][['DATE', 'DESCRIPTION', 'DR', 'CR']]
			tempDF['BAL'] = tempDF['DR'].cumsum() - tempDF['CR'].cumsum()
			print(tempDF[['DATE', 'DESCRIPTION', 'DR', 'CR', 'BAL']].round(2).to_string())
	def printSummary(self):
		tempDF = self.bsDF[['ACC', 'DR', 'CR']]
		tempDF['BAL'] = tempDF['DR'] - tempDF['CR']
		print(tempDF.groupby(['ACC']).sum())
	def getResult(self):
		if(self.getBalance()==0):
			bs='OK'
		else:
			bs='ERROR'
		g,n=self.getPL()
		c=self.getcashBalance()
		i=self.getInventoryBalance()
		pm,roce,ctr = self.getRatio()
		result={'ID':self.id, 'STATUS':bs, 'GROSS_PL':round(g,2), 'NET_PL':round(n,2), 'CASH':c, 'INV':i, 'MARGIN':pm, 'ROCE':roce, 'TURN':ctr}
		resultDF=pd.DataFrame([result])
		resultDF = resultDF.reset_index(drop=True)
		return resultDF[['ID','STATUS','CASH','INV','GROSS_PL','NET_PL','MARGIN','ROCE',TURN']]

'''
	Test program
'''
if __name__ == "__main__":
	pf = Portfolio(1)
	pf.addCapital('2018-02-07',5000)
	pf.buy('2018-02-08',460,5)
	pf.sell('2018-02-14',490,5)	
	txnList = [{'txnType': 'BUY', 'date':'2018-03-01', 'price': 460, 'qty': 1},
				{'txnType': 'BUY', 'date':'2018-03-02', 'price': 460, 'qty': 2},
				{'txnType': 'SELL', 'date':'2018-03-05', 'price': 490, 'qty': 3}]
	pf.processTxnList(txnList)
	pf.printSummary()
	#pf.printBalanceSheet()
	pf.printBalanceSheet('TRD')
	resultDF=pf.getResult()
	print(resultDF)
	
