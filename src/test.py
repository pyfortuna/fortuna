# Import Libraries
import pandas as pd
import re
from urllib.request import urlopen

# ---------------------------------------------
# Function to print Company Name and Live Price
# ---------------------------------------------
def printPrice(livePriceURL):
	# https://docs.python.org/dev/tutorial/stdlib.html#internet-access
	with urlopen(livePriceURL) as response:
		for line in response:
			line = line.decode('utf-8')  # Decoding the binary data to text.
			if 'Nse_Prc_tick' in line:  # look for NSE Price
				m=re.search("<strong>(.*?)</strong>",line)
				livePrice=m.group(1)
				#print("livePrice : " + livePrice)
			elif 'compname_imp' in line:  # look for Company Name
				m=re.search("value=\"(.*?)\"",line)
				companyName=m.group(1)
				#print("companyName : " + companyName)
	print(companyName + " : " + livePrice)

# ---------------------------------------------
# Main Program
# ---------------------------------------------
dfPF = pd.read_csv("/home/ec2-user/plutus/pf.csv")[['companyName','currentValue']]
dfFinYr = pd.read_csv("/home/ec2-user/plutus/finYr.csv")[['companyShortName','livePriceURL','pl_coef','eps_coef']]

res=pd.merge(dfPF, dfFinYr, left_on=['companyName'], right_on=['companyShortName'])
res1=res.sort_values(by='eps_coef', ascending=False)
#print(res1)

urlList=res['livePriceURL']
for urlListItem in urlList:
    printPrice(urlListItem)
