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
	print(str(i) + " : " + pfList[i])
	if re.search(companyNameRegex,str(pfList[i])):
		m=re.search(companyNameRegex,pfList[i])
		companyName=m.group(1)
		print("Company : " + companyName)
	print(str(i) + " : " + pfList[i+2])
	sector=pfList[i+2]
	print("Sector : " + sector)
	print(str(i) + " : " + pfList[i+4])
	l=pfList[i+4].split("\t")
	print(str(l))
	i += 5
print("-----------------------")
