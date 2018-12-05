# Import libraries
import fortunacommon
import re   # for Regex
from datetime import datetime # for date parsing and formatting

# Regular expressions
dataRegex="itemprop=\"name\">[\"Buy\"|\"Sell\"].*?</a></h3><time class=\"date-format\" data-time=\".*?\">"
itemRegex="itemprop=\"name\">(Buy|Sell)\s(.*?), target Rs\s(.*?)\:\s(.*)</a></h3><time class=\"date-format\" data-time=\"(.*?)\">"

# Read file
# http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html
etrecoDataFile= open("/home/ec2-user/plutus/etreco.html","r", encoding="ascii", errors="surrogateescape")
etrecoData=""
etrecoDataLines = etrecoDataFile.read().splitlines()
etrecoDataFile.close()

# Remove linefeeds
for etrecoDataLine in etrecoDataLines:
  etrecoData+=etrecoDataLine.strip()

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
    datetime_object = datetime.strptime(dateTimeStr, "%b %d, %Y, %I:%M %p %Z")
    #dateTimeVal = datetime_object.strftime("%d-%b-%Y")
    print(recoType + "\t" + companyName + "\t" + price + "\t" + recommender + "\t" + dateTimeStr)
