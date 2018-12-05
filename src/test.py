# Import libraries
import fortunacommon
import re   # for Regex
from datetime import datetime # for date parsing and formatting

# Regular expressions
dataRegex="itemprop=\"name\">[\"Buy\"|\"Sell\"].*?</a></h3><time class=\"date-format\" data-time=\".*?\">"
itemRegex="itemprop=\"name\">(Buy|Sell)\s(.*?), target Rs\s(.*?)\:\s(.*)</a></h3><time class=\"date-format\" data-time=\"(.*?)\">"

# Read file
etrecoData=fortunacommon.fileToString("/home/ec2-user/plutus/etreco.html")

# Search using regex
pattern = re.compile(dataRegex)
for (idx, matchData) in enumerate(re.findall(pattern, etrecoData), start=1):
  if re.search(itemRegex, matchData):
    m=re.search(itemRegex, matchData)
    recoType=m.group(1).strip()
    companyName=m.group(2).strip()
    price=m.group(3).strip()
    recommender=m.group(4).strip()
    dateTimeStr=m.group(5).strip()
    datetime_object = datetime.strptime(dateTimeStr[0:-14], "%b %d, %Y")
    dateTimeVal = datetime_object.strftime("%d-%b-%Y")
    print(recoType + "\t" + companyName + "\t" + price + "\t" + recommender + "\t" + dateTimeVal)
