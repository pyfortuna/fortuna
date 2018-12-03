import os
import re
import smtplib
import os
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# ----------------------------------
# Class for parsing Moneycontrol URL
# ----------------------------------
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
