import fortunacommon
import re

# --------------------------------------------------------
# Main program
# --------------------------------------------------------

companyNameRegex="(.*)\s\(\d{1,3}\)"

pr=fortunacommon.loadAppProperties()
f = open('/home/ec2-user/fortuna/fortuna/data/pf.txt', 'r')
pfList = f.read().splitlines()
f.close()

i = 0
while i < len(pfList):
	print("==========================")
	#print(str(i) + " : " + pfList[i])
	if re.search(companyNameRegex,str(pfList[i])):
		m=re.search(companyNameRegex,pfList[i])
		companyName=m.group(1)
		print("Company : " + companyName)
	#print(str(i) + " : " + pfList[i+2])
	sector=pfList[i+2]
	print("Sector : " + sector)
	#print(str(i) + " : " + pfList[i+4])
	l=pfList[i+4].split("\t")
	#print(str(l))
	livePrice=l[0]
	priceChange=l[1].replace("+","")
	quantity=l[2]
	invPrice=l[3].replace(",","")
	daysGain=l[4].replace(",","")
	daysGainPercent=l[5]
	totalGain=l[6].replace(",","")
	totalGainPercent=l[7]
	currentValue=l[8].replace(",","")
	print("Live Price : " + livePrice)
	print("Change : " + priceChange)
	print("Quantity : " + quantity)
	print("Investment Price : " + invPrice)
	print("Day's Gain : " + daysGain)
	print("Day's Gain % : " + daysGainPercent)
	print("Total Gain : " + totalGain)
	print("Total Gain % : " + totalGainPercent)
	print("Current Value : " + currentValue)
	
	i += 5
print("-----------------------")
