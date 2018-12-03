import fortunacommon

# --------------------------------------------------------
# Main program
# --------------------------------------------------------

pr=fortunacommon.loadAppProperties()
f = open('/home/ec2-user/fortuna/fortuna/data/pf.txt', 'r')
pfList = f.read().splitlines()
f.close()

i = 0
while i < len(pfList):
	print("==========================")
	print(str(i) + " : " + pfList[i])
	print(str(i) + " : " + pfList[i+2])
	print(str(i) + " : " + pfList[i+4])
	i += 5
print("-----------------------")
