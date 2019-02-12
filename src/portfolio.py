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
	def __init__ (self):
		col_names =  ['ACC', 'DESCRIPTION', 'DR', 'CR']
		self.bsDF = pd.DataFrame(columns=col_names)
		self.invList = InventoryList()
	def calculateBuyBrokerage (self, price, qty):
		totalTrade	= price * qty
		brokerage =	0.01
		exchangeTxnCharge = round(totalTrade*0.00325/100,2)
		gst = round((brokerage + exchangeTxnCharge)*18/100,2)
		securityTxnTax = round((totalTrade*0.001),0)
		sebiTurnoverFee = round(totalTrade*15/10000000,2)
		stampDuty=round((totalTrade*0.01/100),2)
		totalCharges = brokerage + exchangeTxnCharge + gst + securityTxnTax + sebiTurnoverFee + stampDuty
		return totalCharges
	def calculateSellBrokerage (self, price, qty):
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
	def addBalanceSheetRecord (self, drAccount, crAccount, description, amount):
		drRecord={'ACC': drAccount, 'DESCRIPTION': description, 'DR': amount, 'CR':0}
		crRecord={'ACC': crAccount, 'DESCRIPTION': description, 'DR': 0, 'CR':amount}
		tempDF=pd.DataFrame([drRecord,crRecord])
		self.bsDF=self.bsDF.append(tempDF, sort=True)
	def addCapital (self, amount):
		self.addBalanceSheetRecord ('TRD', 'CAP', 'Capital', amount)
	def buy (self, buyPrice, qty):
		brokerage = self.calculateBuyBrokerage(buyPrice, qty)
		buyAmt = (buyPrice*qty)
		self.invList.add(buyPrice, qty)
		self.addBalanceSheetRecord ('INV', 'TRD', 'Buy', buyAmt)
		self.addBalanceSheetRecord ('BRK', 'TRD', 'Brokerage (Buy)', brokerage)
	def sell(self, sellPrice, qty):
		brokerage = self.calculateSellBrokerage(sellPrice, qty)
		sellAmt = (sellPrice*qty)
		buyPrice=self.invList.remove(qty)
		buyAmt = (buyPrice*qty)
		self.addBalanceSheetRecord ('TRD', 'SAL', 'Sell', sellAmt)
		self.addBalanceSheetRecord ('COG', 'INV', 'Sell', buyAmt)
		self.addBalanceSheetRecord ('BRK', 'TRD', 'Brokerage (Sell)', brokerage)
	def getBalance(self):
		tempSerBal = self.bsDF['DR'] - self.bsDF['CR']
		totBal =int(tempSerBal.sum())
		return int(totBal)
	def getInventoryBalance(self):
		return self.invList.count()
	def getcashBalance(self):
		tempDF = self.bsDF.loc[self.bsDF['ACC'] == 'TRD'][['DR', 'CR']]
		tempDF['BAL'] = tempDF['DR'] - tempDF['CR']
		cashBalance =round(tempDF[['BAL']].sum(),2)
		return cashBalance
	def getResults(self):
		salCr = round(self.bsDF.loc[self.bsDF['ACC'] == 'SAL']['CR'].sum(),2)
		cogDr = round(self.bsDF.loc[self.bsDF['ACC'] == 'COG']['DR'].sum(),2)
		brkDr = round(self.bsDF.loc[self.bsDF['ACC'] == 'BRK']['DR'].sum(),2)
		grossPL = salCr - cogDr
		netPL = grossPL - brkDr
		return grossPL, netPL
	def printBalanceSheet(self, account='none'):
		if (account=='none'):
			print(self.bsDF[['ACC', 'DESCRIPTION', 'DR', 'CR']])
		else:
			tempDF = self.bsDF.loc[self.bsDF['ACC'] == account][['DESCRIPTION', 'DR', 'CR']]
			tempDF['BAL'] = tempDF['DR'].cumsum() - tempDF['CR'].cumsum()
			print(tempDF[['DESCRIPTION', 'DR', 'CR', 'BAL']].round(2).to_string())
	def printSummary(self):
		tempDF = self.bsDF[['ACC', 'DR', 'CR']]
		tempDF['BAL'] = tempDF['DR'] - tempDF['CR']
		print(tempDF.groupby(['ACC']).sum())

'''
	Test program
'''
if __name__ == "__main__":
	pf = Portfolio()
	pf.addCapital(5000)
	pf.buy(460,5)
	pf.sell(490,5)
	pf.printSummary()
	#pf.printBalanceSheet()
	#pf.printBalanceSheet('TRD')
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
	
