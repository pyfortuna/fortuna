import os
import re
import smtplib
import os
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from urllib.request import urlopen

# ----------------------------------
# Class for parsing Moneycontrol URL
# ----------------------------------
class Moneycontrol:
  def __init__(self, url):
    regex = r"http[s]{0,1}://www.moneycontrol.com/india/stockpricequote/(.*)/(.*)/(.*)"
    if re.search(regex, url):
      m=re.search(regex, url)
      self.category = m.group(1)
      self.companyname = m.group(2)
      self.companycode = m.group(3)
      self.url = "https://www.moneycontrol.com/india/stockpricequote/" + self.category + "/" + self.companyname + "/" + self.companycode
  
  # Function get URL for main page of the company
  def getURL(self):    
    return self.url
  
  # Function to get company name
  def getCompanyName(self):
    return self.companyname
  
  # Function get URL for Yearly Financial Results page of the company
  def getYrFinURL(self):
    yrFinURL = "https://www.moneycontrol.com/financials/" + self.companyname + "/results/yearly/" + self.companycode
    return yrFinURL
  
  # Function get URL for Quarterly Financial Results page of the company
  def getQtrFinURL(self):
    qtrFinURL = "https://www.moneycontrol.com/financials/" + self.companyname + "/results/quarterly-results/" + self.companycode
    return qtrFinURL
  
  # Function get URL for Fianancial Ratios page of the company
  def getRatioURL(self):
    ratioURL = "https://www.moneycontrol.com/financials/" + self.companyname + "/ratiosVI/" + self.companycode
    return ratioURL
  
  # Function to get company name and live price
  def getLivePrice():
    # https://docs.python.org/dev/tutorial/stdlib.html#internet-access
    with urlopen(self.url) as response:
      for line in response:
        line = line.decode('utf-8')  # Decoding the binary data to text.
        if 'Nse_Prc_tick' in line:  # look for NSE Price
          m=re.search("<strong>(.*?)</strong>",line)
          livePrice=float(m.group(1))
          #print("livePrice : " + livePrice)
        #elif 'compname_imp' in line:  # look for Company Name
        elif 'w135 gD_11 TAC brdtop PT10 MT10' in line:  # look for Company Name
          #m=re.search("value=\"(.*?)\"",line)
          m=re.search("<strong>(.*?)</strong>",line)
          companyName=m.group(1)
          #print("companyName : " + companyName)
    #print(companyName + " : " + livePrice)
    liveData = {
        "companyName": companyName,
        "livePrice": livePrice
    }
    return liveData

# -----------------------------------------------------------------------------
# Load property key/values from "fortuna.properties" file in "config" directory
# -----------------------------------------------------------------------------
def loadAppProperties():
  fileDir = os.path.dirname(os.path.abspath(__file__))
  propfile = os.path.join(fileDir, '../config/fortuna.properties')
  props = dict( l.rstrip().split('=') for l in open(propfile)
    if not l.startswith("#") )
  return props

# ---------------------------------------------------------------
# Get list of filenames in a directory which matches with pattern
# ---------------------------------------------------------------
def getFiles(inputDirectory,filenameRegexPattern):
  files = [f for f in os.listdir(inputDirectory) if re.match(filenameRegexPattern, f)]
  return files

# ------------------------------------------------------------------
# Send mail (with attachment)
# ------------------------------------------------------------------
def sendMail(subject,body,attachmentFilename):
    pr=loadAppProperties()
    gmail_user=pr['mail.user.id']
    gmail_password=pr['mail.user.password']
    recipient_address=pr['mail.recepient.address']    

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)

        # Message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        content = MIMEText(body, 'plain')
        msg.attach(content)

        # Add attachment        
        with open(attachmentFilename, "rb") as attachmentFile:
            part = MIMEApplication(
                attachmentFile.read(),
                Name=basename(attachmentFilename)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachmentFilename)
        msg.attach(part)

        # Send mail
        server.sendmail(gmail_user, recipient_address, msg.as_string())
        server.close()    

        print('Email sent to ' + recipient_address)
    except:
        print('Something went wrong...')

# ------------------------------------------------
# Read file content into String (remove linefeeds)
# ------------------------------------------------
def fileToString(dataFilename):
  # Read file
  # http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html
  dataFile= open(dataFilename,"r", encoding="ascii", errors="surrogateescape")
  data=""
  dataLines = dataFile.read().splitlines()
  dataFile.close()
  # Remove linefeeds and combine lines
  for dataLine in dataLines:
    data+=dataLine.strip()
  # Return data
  return data
