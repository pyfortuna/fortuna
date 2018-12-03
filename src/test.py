import fortunacommon

# --------------------------------------------------------
# Main program
# --------------------------------------------------------

pr=fortunacommon.loadAppProperties()
f = open('/user/ec2-user/fortuna/fortuna/data/pf.txt', 'r')
pfList = f.read().splitlines()
f.close()

i = 0
while i < len(pfList):
	print("=========================="])
	print(i + " : " + pfList[i])
	print(i + " : " + pfList[i+2])
	print(i + " : " + pfList[i+4])
	i += 5
