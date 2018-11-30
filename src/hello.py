# Import libraries
import fortunacommon
import re   # for Regex
import csv  # for CSV file creation

# Regular expressions
companyNameRegex="<H1 class=\"b_42 PT20\">(.*)</H1>"
compdetailsRegex="<div class=\"FL gry10\">BSE: (.*?)<span class=\"PR7 PL7\">\|</span>NSE: (.*?)<span class=\"PR7 PL7\">\|</span>ISIN: (.*?)<span class=\"PR7 PL7\">\|</span>SECTOR: (.*?)</div>"
nsePriceRegex="<span id=\"Nse_Prc_tick\" class=\"PA2\"><strong>(.*?)</strong>"
monthListRegex="<tr height=\"22px\"><td colspan=\"1\" class=\"detb\" width=\"40%\"></td>(.*?)</tr>"
monthRegex="<td align=\"right\" class=\"detb\">(.*?)</td>"
plListRegex="<tr height=\"22px\"><td colspan=\"1\" class=\"det\" width=\"40%\">Net Profit/\(Loss\) For the Period</td>(.*?)</tr>"
plRegex="<td align=\"right\" class=\"det\">(.*?)</td>"
epsListRegex="<tr height=\"22px\"><td colspan=\"1\" class=\"det\" width=\"40%\">Basic EPS</td>(.*?)</tr>"
epsRegex="<td align=\"right\" class=\"det\">(.*?)</td>"

# Start processing
def parseFinYrFile(iFilename):
  # Read file
  # http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html
  fYrFinData= open(iFilename,"r", encoding="ascii", errors="surrogateescape")
  yrFinData=""
  yrFinDataList = fYrFinData.read().splitlines()
  fYrFinData.close()

  # Remove linefeeds
  for yrFinDataListItem in yrFinDataList:
    yrFinData+=yrFinDataListItem.strip()

  # Search using regex
  if re.search(companyNameRegex, yrFinData):
    m=re.search(companyNameRegex, yrFinData)
    companyName=m.group(1)

  if re.search(compdetailsRegex, yrFinData):
    m=re.search(compdetailsRegex, yrFinData)
    bseId=m.group(1)
    nseId=m.group(2)
    isin=m.group(3)
    sector=m.group(4)

  if re.search(nsePriceRegex, yrFinData):
    m=re.search(nsePriceRegex, yrFinData)
    nsePrice=m.group(1)

  if re.search(monthListRegex, yrFinData):
    m=re.search(monthListRegex, yrFinData)
    monthList=m.group(1)

  monthName1,monthName2,monthName3,monthName4,monthName5="","","","",""
  pattern = re.compile(monthRegex)
  for (idx, monthName) in enumerate(re.findall(pattern, monthList), start=1):
      if idx==1:
        monthName1=monthName
      elif idx==2:
        monthName2=monthName
      elif idx==3:
        monthName3=monthName
      elif idx==4:
        monthName4=monthName
      elif idx==5:
        monthName5=monthName      

  if re.search(plListRegex, yrFinData):
    m=re.search(plListRegex, yrFinData)
    plList=m.group(1)

  pl1,pl2,pl3,pl4,pl5="","","","",""
  pattern = re.compile(plRegex)
  for (idx, pl) in enumerate(re.findall(pattern, plList), start=1):
      if idx==1:
        pl1=pl
      elif idx==2:
        pl2=pl
      elif idx==3:
        pl3=pl
      elif idx==4:
        pl4=pl
      elif idx==5:
        pl5=pl

  if re.search(epsListRegex, yrFinData):
    m=re.search(epsListRegex, yrFinData)
    epsList=m.group(1)

  eps1,eps2,eps3,eps4,eps5="","","","",""
  pattern = re.compile(epsRegex)
  for (idx, eps) in enumerate(re.findall(pattern, epsList), start=1):
      if idx==1:
        eps1=eps
      elif idx==2:
        eps2=eps
      elif idx==3:
        eps3=eps
      elif idx==4:
        eps4=eps
      elif idx==5:
        eps5=eps

  companydata = {
    "companyName": companyName,
    "bseId": bseId,
    "nseId": nseId,
    "isin": isin,
    "sector": sector,
    "nsePrice": nsePrice,
    "monthName1": monthName1,
    "monthName2": monthName2,
    "monthName3": monthName3,
    "monthName4": monthName4,
    "monthName5": monthName5,
    "pl1": pl1,
    "pl2": pl2,
    "pl3": pl3,
    "pl4": pl4,
    "pl5": pl5,
    "eps1": eps1,
    "eps2": eps2,
    "eps3": eps3,
    "eps4": eps4,
    "eps5": eps5
  }
  return companydata
# --------------------------------

pr=fortunacommon.loadAppProperties()

with open(pr['finyr.output.filename'], 'w') as csvfile:
  fieldnames = ['companyName', 'bseId', 'nseId', 'isin', 'sector', 'nsePrice','monthName1','monthName2','monthName3','monthName4','monthName5','pl1','pl2','pl3','pl4','pl5','eps1','eps2','eps3','eps4','eps5']
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
  writer.writeheader()
  fList = fortunacommon.getFiles("/home/ec2-user/plutus",".*\.html")
  for fListItem in fList:
    print("Processing : " + fListItem)
    c=parseFinYrFile(fListItem)
    writer.writerow({'companyName':c["companyName"], 'bseId':c["bseId"], 'nseId':c["nseId"], 'isin':c["isin"], 'sector':c["sector"], 'nsePrice':c["nsePrice"],'monthName1':c["monthName1"],'monthName2':c["monthName2"],'monthName3':c["monthName3"],'monthName4':c["monthName4"],'monthName5':c["monthName5"],'pl1':c["pl1"],'pl2':c["pl2"],'pl3':c["pl3"],'pl4':c["pl4"],'pl5':c["pl5"],'eps1':c["eps1"],'eps2':c["eps2"],'eps3':c["eps3"],'eps4':c["eps4"],'eps5':c["eps5"]})

print("*** Completed ***")
