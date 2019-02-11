class Portfolio:
	def __init__ (self):
		self.capDr = 0
		self.capCr = 0
		self.trdDr = 0
		self.trdCr = 0
		self.brkDr = 0
		self.brkCr = 0
		self.invDr = 0
		self.invCr = 0
		self.salDr = 0
		self.salCr = 0
		self.cogDr = 0
		self.cogCr = 0
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
		return totBal
	def getResults(self):
		grossPL = self.salCr - self.cogDr
		netPL = grossPL - self.brkDr
		cashBalance = (self.capCr + self.salCr) - (self.invDr + self.brkDr)
		return grossPL, netPL, cashBalance

if __name__ == "__main__":
	pf = Portfolio()
	pf.addCapital(10000)
	pf.buy(460,5,2.34)
	brk=2.36+15.93
	pf.sell(460,490,5,brk)
	b=pf.getBalance()
	print('BALANCE : %6.2f' % b)
	g,n,c=pf.getResults()
	print('GROSS P/L : %6.2f' % g)
	print('NET P/L : %6.2f' % n)
	print('CASH BALANCE : %6.2f' % c)
	
