# Import Libraries
import pandas as pd
import re
import fortunacommon
from urllib.request import urlopen
'''
# ---------------------------------------------
# Function to print Company Name and Live Price
# ---------------------------------------------
def getLivePrice(livePriceURL):
	# https://docs.python.org/dev/tutorial/stdlib.html#internet-access
	with urlopen(livePriceURL) as response:
		for line in response:
			line = line.decode('utf-8')  # Decoding the binary data to text.
			if 'Nse_Prc_tick' in line:  # look for NSE Price
				m=re.search("<strong>(.*?)</strong>",line)
				livePrice=float(m.group(1))
				#print("livePrice : " + livePrice)
			#elif 'compname_imp' in line:  # look for Company Name
			elif 'w135 gD_11 TAC brdtop PT10 MT10' in line:  # look for Company Name
				#m=re.search("value=\"(.*?)\"",line)
				m=re.search("<strong>(.*?)</strong>",line)
				companyName=m.group(1)
				#print("companyName : " + companyName)
	#print(companyName + " : " + livePrice)
	liveData = {
	    "companyName": companyName,
	    "livePrice": livePrice
	}
	return liveData
'''
# ---------------------------------------------
# Main Program
# ---------------------------------------------

#dfPF = pd.read_csv("/home/ec2-user/plutus/pf.csv")[['companyName','currentValue']]
dfTarget = pd.read_csv("/home/ec2-user/fortuna/fortuna/data/target.csv")[['type','companyName','targetPrice']]
dfFinYr = pd.read_csv("/home/ec2-user/plutus/finYr.csv")[['companyShortName','livePriceURL']]

res=pd.merge(dfTarget, dfFinYr, left_on=['companyName'], right_on=['companyShortName'])
#res1=res.sort_values(by='eps_coef', ascending=False)
#print(res)

for index, row in res.iterrows():
	try:
		#print("DEBUG : (a) " + row['companyName'])
		#print("DEBUG : (b) " + str(row['targetPrice']))
		#print("DEBUG : (c) " + row['livePriceURL'])
		mc=fortunacommon.Moneycontrol(str(row['livePriceURL']))
		l=mc.getLivePrice()
		#print("DEBUG : (d) " + l['livePrice'])
		if row['type'] == "Buy":
			if l['livePrice'] <= row['targetPrice']:
				reco="[ BUY  ]"
			else:
				reco="[ WAIT ]"
		elif row['type'] == "Sell":
			if l['livePrice'] >= row['targetPrice']:
				reco="[ SELL ]"
			else:
				reco="[ WAIT ]"
		print(reco + " : " + row['companyName'] + " : P: " + str(l['livePrice']) + " TGT: " + str(row['targetPrice']))
	except Exception as ex:
		print(ex)
		#print(row['companyName'] + " : ERROR")
		pass
