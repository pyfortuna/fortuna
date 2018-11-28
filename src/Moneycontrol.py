import re

class Moneycontrol:
  def __init__(self, url):
    self.url = url
    regex = r"http[s]{0,1}://www.moneycontrol.com/india/stockpricequote/(.*)/(.*)/(.*)"
    if re.search(regex, url):
      m=re.search(regex, url)
      self.category = m.group(1)
      self.companyname = m.group(2)
      self.companycode = m.group(3)
  def getURL(self):
    return self.url
  def getCompanyName(self):
    return self.companyname
  def getYrFinURL(self):
    yrFinURL = "https://www.moneycontrol.com/financials/" + self.companyname + "/results/yearly/" + self.companycode
    return yrFinURL
  def getQtrFinURL(self):
    qtrFinURL = "https://www.moneycontrol.com/financials/" + self.companyname + "/results/quarterly-results/" + self.companycode
    return qtrFinURL
  def getRatioURL(self):
    ratioURL = "https://www.moneycontrol.com/financials/" + self.companyname + "/ratiosVI/" + self.companycode
    return ratioURL

# --------------------------------------------------------
f = open('list.txt', 'r')
mcList = f.read().splitlines()
f.close()

fYrFin= open("/home/ec2-user/plutus/wgetYrFin.sh","w+")

for mcListItem in mcList:
  mc = Moneycontrol(mcListItem)
  yrFinGetCommand = "wget " + mc.getYrFinURL() + r" -O ~/plutus/" + mc.getCompanyName() + ".html" + "\n"
  fYrFin.write(yrFinGetCommand)

fYrFin.write("exit\n")
fYrFin.close()
# --------------------------------------------------------

fYrFinData= open("/home/ec2-user/plutus/biocon.html","r")
yrFinData=""
yrFinDataList = fYrFinData.read().splitlines()
fYrFinData.close()
companyNameRegex="<H1 class=\"b_42 PT20\">(.*)</H1>"

for yrFinDataListItem in yrFinDataList:
  yrFinData+=yrFinDataListItem.strip()

if re.search(companyNameRegex, yrFinData):
  m=re.search(companyNameRegex, yrFinData)
  companyName=m.group(1)
  print("**** [" + companyName + "] ****")

# --------------------------------------------------------
