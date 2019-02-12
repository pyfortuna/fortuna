import pandas as pd

'''
	Class to manage portfolio & related transactions
'''
class Portfolio:
	def __init__ (self):
		self.invQty = 0	# Inventory (Qty)
		col_names =  ['ACC', 'DESCRIPTION', 'DR', 'CR']
		self.bsDF = pd.DataFrame(columns=col_names)
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
	def addBalanceSheetRecord (self, record):
		tempDF=pd.DataFrame([record])
		self.bsDF=self.bsDF.append(tempDF, sort=True)
	def addCapital (self, amount):
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Capital', 'DR': amount, 'CR':0})
		self.addBalanceSheetRecord({'ACC': 'CAP', 'DESCRIPTION': 'Capital', 'DR': 0, 'CR':amount})
	def buy (self, buyPrice, qty):
		brokerage = self.calculateBuyBrokerage(buyPrice, qty)
		buyAmt = (buyPrice*qty)
		self.invQty += qty
		self.addBalanceSheetRecord({'ACC': 'INV', 'DESCRIPTION': 'Buy', 'DR': buyAmt, 'CR':0})
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Buy', 'DR': 0, 'CR':buyAmt})
		self.addBalanceSheetRecord({'ACC': 'BRK', 'DESCRIPTION': 'Brokerage (Buy)', 'DR': brokerage, 'CR':0})
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Brokerage (Buy)', 'DR': 0, 'CR':brokerage})
	def sell(self, buyPrice, sellPrice, qty):
		brokerage = self.calculateSellBrokerage(sellPrice, qty)
		sellAmt = (sellPrice*qty)
		buyAmt = (buyPrice*qty)
		self.invQty -= qty
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Sell', 'DR': sellAmt, 'CR':0})
		self.addBalanceSheetRecord({'ACC': 'SAL', 'DESCRIPTION': 'Sell', 'DR': 0, 'CR':sellAmt})
		self.addBalanceSheetRecord({'ACC': 'COG', 'DESCRIPTION': 'Sell', 'DR': buyAmt, 'CR':0})
		self.addBalanceSheetRecord({'ACC': 'INV', 'DESCRIPTION': 'Sell', 'DR': 0, 'CR':buyAmt})
		self.addBalanceSheetRecord({'ACC': 'BRK', 'DESCRIPTION': 'Brokerage (Sell)', 'DR': brokerage, 'CR':0})
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Brokerage (Sell)', 'DR': 0, 'CR':brokerage})
	def getBalance(self):
		#tempDF = self.bsDF[['DR', 'CR']]
		tempSerBal = self.bsDF['DR'] - self.bsDF['CR']
		#tempDF=tempDF.assign('BAL'=tempSerBal)
		totBal =int(tempSerBal.sum())
		return int(totBal)
	def getInventoryBalance(self):
		return int(self.invQty)
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
	pf.sell(460,490,5)
	pf.printSummary()
	pf.printBalanceSheet()
	pf.printBalanceSheet('TRD')
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
	
