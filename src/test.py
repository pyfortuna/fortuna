# Import Libraries
import pandas as pd
import re
from urllib.request import urlopen

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
				livePrice=m.group(1)
				#print("livePrice : " + livePrice)
			#elif 'compname_imp' in line:  # look for Company Name
			elif 'w135 gD_11 TAC brdtop PT10 MT10' in line:  # look for Company Name
				#m=re.search("value=\"(.*?)\"",line)
				m=re.search("<strong>(.*?)</strong>",line)
				companyName=m.group(1)
				#print("companyName : " + companyName)
	print(companyName + " : " + livePrice)
	liveData = {
	    "companyName": companyName,
	    "livePrice": livePrice
	}
	return liveData

# ---------------------------------------------
# Main Program
# ---------------------------------------------
dfPF = pd.read_csv("/home/ec2-user/plutus/pf.csv")[['companyName','currentValue']]
dfTarget = pd.read_csv("/home/ec2-user/fortuna/fortuna/target.csv")[['type','companyName','targetPrice']]
dfFinYr = pd.read_csv("/home/ec2-user/plutus/finYr.csv")[['companyShortName','livePriceURL','pl_coef','eps_coef']]

res=pd.merge(dfTarget, dfFinYr, left_on=['companyName'], right_on=['companyShortName'])
#res1=res.sort_values(by='eps_coef', ascending=False)
#print(res1)

for index, row in res.iterrows():
	try:
		l=getLivePrice(row['livePriceURL'])
		print(row['companyName'] + ":: P: " + l['livePrice'] + " TP: " + row['targetPrice'])
	except:
		pass
