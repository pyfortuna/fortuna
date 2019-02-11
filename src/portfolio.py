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
		self.salDr = 0	# Sales (DR)
		self.salCr = 0	# Sales (CR)
		self.cogDr = 0	# Cost of Goods (DR)
		self.cogCr = 0	# Cost of Goods (CR)
	def addCapital (self, amount):
		self.capCr += amount
		self.trdDr += amount
	def buy (self, buyPrice, qty, brokerage):
		self.trdCr += (buyPrice*qty) + brokerage
		self.invDr += (buyPrice*qty)
		self.brkDr += brokerage
	def sell(self, buyPrice,sellPrice,qty,brokerage):
		self.trdDr += (sellPrice*qty)
		self.brkDr += brokerage
		self.cogDr += (buyPrice*qty)
		self.salCr += (sellPrice*qty)
		self.trdCr += brokerage
		self.invCr += (buyPrice*qty)
	def getBalance(self):
		capBal = self.capDr - self.capCr
		trdBal = self.trdDr - self.trdCr
		brkBal = self.brkDr - self.brkCr
		invBal = self.invDr - self.invCr			
		salBal = self.salDr - self.salCr
		cogBal = self.cogDr - self.cogCr
		totBal = capBal + trdBal + brkBal + invBal + salBal + cogBal
		return int(totBal)
	def getcashBalance(self):
		cashBalance = (self.capCr + self.salCr) - (self.invDr + self.brkDr)
		return cashBalance
	def getResults(self):
		grossPL = self.salCr - self.cogDr
		netPL = grossPL - self.brkDr
		return grossPL, netPL

if __name__ == "__main__":
	pf = Portfolio()
	pf.addCapital(10000)
	pf.buy(460,5,2.34)
	pf.sell(460,490,5,2.36)
	b=pf.getBalance()
	if(b==0):
		print('BALANCESHEET : OK')
	else:
		print('BALANCESHEET : ERROR')
	g,n=pf.getResults()
	c=pf.getcashBalance()
	print('GROSS P/L    : %6.2f' % g)
	print('NET P/L      : %6.2f' % n)
	print('CASH BALANCE : %6.2f' % c)
	
