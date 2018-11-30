import re
import fortunacommon

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
# Main program
# --------------------------------------------------------

pr=fortunacommon.loadAppProperties()
f = open(pr['genshell.input.filename'], 'r')
mcList = f.read().splitlines()
f.close()

fYrFin= open(pr['genshell.output.finyr.filename'],"w+")

for mcListItem in mcList:
  mc = Moneycontrol(mcListItem)
  yrFinGetCommand = "wget " + mc.getYrFinURL() + r" -O ~/plutus/" + mc.getCompanyName() + ".html" + "\n"
  fYrFin.write(yrFinGetCommand)

fYrFin.write("exit\n")
fYrFin.close()
# --------------------------------------------------------


