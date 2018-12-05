# Import libraries
import fortunacommon
import re   # for Regex
import csv  # for CSV file creation

# --------------------------------------------------------
# Main program
# --------------------------------------------------------

companyNameRegex="(.*)[\s\(\d{1,3}\)]{0,1}"

pr=fortunacommon.loadAppProperties()
f = open('/home/ec2-user/fortuna/fortuna/data/pf.txt', 'r')
pfList = f.read().splitlines()
f.close()

# process pf file and create csv file
with open('/home/ec2-user/plutus/pf.csv', 'w') as csvfile:
	fieldnames = ['companyName', 'sector', 'livePrice', 'priceChange', 'quantity', 'invPrice','daysGain','daysGainPercent','totalGain','totalGainPercent','currentValue']
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	# Read pf file
	i = 0
	while i < len(pfList):
		if re.search(companyNameRegex,str(pfList[i])):
			m=re.search(companyNameRegex,pfList[i])
			companyName=m.group(1)
		sector=pfList[i+2]
		l=pfList[i+4].split("\t")
		livePrice=l[0]
		priceChange=l[1].replace("+","")
		quantity=l[2]
		invPrice=l[3].replace(",","")
		daysGain=l[4].replace(",","")
		daysGainPercent=l[5]
		totalGain=l[6].replace(",","")
		totalGainPercent=l[7]
		currentValue=l[8].replace(",","")

		writer.writerow({'companyName':companyName,'sector':sector,'livePrice':livePrice,'priceChange':priceChange,'quantity':quantity,'invPrice':invPrice,'daysGain':daysGain,'daysGainPercent':daysGainPercent,'totalGain':totalGain,'totalGainPercent':totalGainPercent,'currentValue':currentValue})

		i += 5
print("FORTUNA: pf.csv file created")
