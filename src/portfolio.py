import pandas as pd

'''
	Class to manage portfolio & related transactions
'''
class Portfolio:
	def __init__ (self):
		self.capDr = 0	# Capital (DR)
		self.capCr = 0	# Capital (CR)
		self.trdDr = 0	# Trade (DR)
		self.trdCr = 0	# Trade (CR)
		self.brkDr = 0	# Brokerage (DR)
		self.brkCr = 0	# Brokerage (CR)
		self.invDr = 0	# Inventory (DR)
		self.invCr = 0	# Inventory (CR)
		self.invQty = 0	# Inventory (Qty)
		self.salDr = 0	# Sales (DR)
		self.salCr = 0	# Sales (CR)
		self.cogDr = 0	# Cost of Goods (DR)
		self.cogCr = 0	# Cost of Goods (CR)
		col_names =  ['ACC', 'DESCRIPTION', 'DR', 'CR']
		self.bsDF = pd.DataFrame(columns=col_names, inplace=True)
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
		self.bsDF=self.bsDF.append(tempDF)
	def addCapital (self, amount):
		self.capCr += amount
		self.trdDr += amount
		self.addBalanceSheetRecord({'ACC': 'CAP', 'DESCRIPTION': 'Adding Capital', 'DR': '', 'CR':amount})
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Adding Capital', 'DR': amount, 'CR':''})
	def buy (self, buyPrice, qty):
		brokerage = self.calculateBuyBrokerage(buyPrice, qty)
		buyAmt = (buyPrice*qty)
		self.trdCr += buyAmt + brokerage
		self.invDr += buyAmt
		self.brkDr += brokerage
		self.invQty += qty
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Buy', 'DR': '', 'CR':buyAmt})
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Brokerage', 'DR': '', 'CR':brokerage})
		self.addBalanceSheetRecord({'ACC': 'INV', 'DESCRIPTION': 'Buy', 'DR': buyAmt, 'CR':''})
		self.addBalanceSheetRecord({'ACC': 'BRK', 'DESCRIPTION': 'Brokerage', 'DR': brokerage, 'CR':''})
	def sell(self, buyPrice, sellPrice, qty):
		brokerage = self.calculateSellBrokerage(sellPrice, qty)
		sellAmt = (sellPrice*qty)
		buyAmt = (buyPrice*qty)
		self.trdDr += sellAmt
		self.brkDr += brokerage
		self.cogDr += buyAmt
		self.salCr += sellAmt
		self.trdCr += brokerage
		self.invCr += buyAmt
		self.invQty -= qty
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Sell', 'DR': sellAmt, 'CR':''})
		self.addBalanceSheetRecord({'ACC': 'BRK', 'DESCRIPTION': 'Sell (Brokerage)', 'DR': brokerage, 'CR':''})
		self.addBalanceSheetRecord({'ACC': 'COG', 'DESCRIPTION': 'Sell', 'DR': buyAmt, 'CR':''})
		self.addBalanceSheetRecord({'ACC': 'SAL', 'DESCRIPTION': 'Sell', 'DR': '', 'CR':sellAmt})
		self.addBalanceSheetRecord({'ACC': 'TRD', 'DESCRIPTION': 'Sell (Brokerage)', 'DR': '', 'CR':brokerage})
		self.addBalanceSheetRecord({'ACC': 'INV', 'DESCRIPTION': 'Sell', 'DR': '', 'CR':buyAmt})
	def getBalance(self):
		capBal = self.capDr - self.capCr
		trdBal = self.trdDr - self.trdCr
		brkBal = self.brkDr - self.brkCr
		invBal = self.invDr - self.invCr			
		salBal = self.salDr - self.salCr
		cogBal = self.cogDr - self.cogCr
		totBal = capBal + trdBal + brkBal + invBal + salBal + cogBal
		return int(totBal)
	def getInventoryBalance(self):
		return int(self.invQty)
	def getcashBalance(self):
		cashBalance = (self.capCr + self.salCr) - (self.invDr + self.brkDr)
		return cashBalance
	def getResults(self):
		grossPL = self.salCr - self.cogDr
		netPL = grossPL - self.brkDr
		return grossPL, netPL
	def printBalanceSheet(self):
		print(self.bsDF)
'''
	Test program
'''
if __name__ == "__main__":
	pf = Portfolio()
	pf.addCapital(5000)
	pf.buy(460,5)
	pf.sell(460,490,5)
	pf.printBalanceSheet()
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
	
