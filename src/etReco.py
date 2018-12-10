# Import libraries
import fortunacommon
import re   # for Regex evaluation
import csv  # for CSV file output
from datetime import datetime # for Date parsing and formatting

# Initialize
recoList=[]

# Regular expressions
dataRegex="itemprop=\"name\">[\"Buy\"|\"Sell\"|\"Hold\"].*?</a></h3><time class=\"date-format\" data-time=\".*?\">"
itemRegex="itemprop=\"name\">(Buy|Sell|Hold)\s(.*?), target Rs\s(.*?)\:\s(.*)</a></h3><time class=\"date-format\" data-time=\"(.*?)\">"

# Read file
#etrecoData=fortunacommon.fileToString("/home/ec2-user/plutus/etreco.html")
etrecoData=fortunacommon.getWebpageData("https://economictimes.indiatimes.com/markets/stocks/recos")

# Search using regex
pattern = re.compile(dataRegex)
for (idx, matchData) in enumerate(re.findall(pattern, etrecoData), start=1):
  if re.search(itemRegex, matchData):
    m=re.search(itemRegex, matchData)
    recoType=m.group(1).strip()
    companyName=m.group(2).strip()
    price=m.group(3).strip().replace(",","")
    recommender=m.group(4).strip()
    dateTimeStr=m.group(5).strip()
    datetime_object = datetime.strptime(dateTimeStr[0:-14], "%b %d, %Y")
    dateTimeVal = datetime_object.strftime("%d-%b-%Y")
    #print(recoType + "\t" + companyName + "\t" + price + "\t" + recommender + "\t" + dateTimeVal)
    recoData = {
      "recoType": recoType,
      "companyName": companyName,
      "price": price,
      "recommender": recommender,
      "dateTimeVal": dateTimeVal
      }
    recoList.append(recoData)

  # Write output file
  with open("/home/ec2-user/plutus/etreco.csv", 'w') as csvfile:
    fieldnames = ['recoType', 'companyName', 'price', 'recommender', 'dateTimeVal']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for r in recoList:
      writer.writerow({'recoType':r['recoType'], 'companyName':r['companyName'], 'price':r['price'], 'recommender':r['recommender'], 'dateTimeVal':r['dateTimeVal']})

print("FORTUNA: etreco.csv file created")
