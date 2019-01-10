# Import libraries
import datetime
import nseUtil as nu
import fortunacommon as fc
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import candleplot as cp
import smaplot as sp
from fpdf import FPDF

# Configure parameters
numDays=700

def processCompany(companyCode):
  candleFilename='/home/ec2-user/plutus/CDL_%s.png' % companyCode
  smaFilename='/home/ec2-user/plutus/SMA_%s.png' % companyCode

  # Data preparation
  e = datetime.datetime.now()
  s = e - datetime.timedelta(days=numDays)
  df = nu.getHistoricPrice(companyCode,s,e)
  sma200 = df['close'].rolling(200).mean()
  sma20 = df['close'].rolling(20).mean()
  mstd = df['close'].rolling(20).std()
  hband = sma20 + 2*mstd
  lband = sma20 - 2*mstd
  df=df.assign(sma200=sma200)
  df=df.assign(sma20=sma20)
  df=df.assign(hband=hband)
  df=df.assign(lband=lband)
  df=df.dropna()
  print(df.head())
  sp.plotSMA(df,smaFilename)

  dfCandle=df.tail(30)
  #cp.plotCandlestick(df1,candleFilename,'%Y-%m-%d')
  cp.plotCandlestick(dfCandle,candleFilename)
  
  plotData = {
    "companyCode": companyCode,
    "smaFilename": smaFilename,
    "candleFilename": candleFilename
  }
  return plotData

# ------------------------------
# MAIN PROGRAM
# ------------------------------
dfTarget = pd.read_csv("/home/ec2-user/fortuna/fortuna/data/target.csv")[['type','companyName','targetPrice']]
dfFinYr = pd.read_csv("/home/ec2-user/fortuna/fortuna/data/finYr.csv") #[['companyShortName','nseID']]
dfMerge=pd.merge(dfTarget, dfFinYr, left_on=['companyName'], right_on=['companyShortName'])
print(dfMerge)
nseList=dfMerge[['nseID']]
print(nseList)

for nseItem in nseList:
  print(nseItem)
  
cList=[]
c=processCompany('ASHOKLEY')
cList.append(c)
c=processCompany('DABUR')
cList.append(c)
dfPDFData = pd.DataFrame(cList)
print(dfPDFData)

# Create PDF
pdf = FPDF()
for index, row in dfPDFData.iterrows():
  pdf.add_page()
  pdf.set_font("Arial", size=18)
  pdf.cell(20, 20, row['companyCode'])
  pdf.image( row['smaFilename'], x=20, y=40, w=170, h=110)
  pdf.image( row['candleFilename'], x=20, y=160, w=170, h=110)
pdf.output('/home/ec2-user/plutus/testpdf.pdf')

# Send Mail
fc.sendMail('Fortuna: Analysis Report','Analysis Report','/home/ec2-user/plutus/testpdf.pdf')
