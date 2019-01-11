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
  print('DEBUG : Downloading NSE data for %s' % companyCode)
  df = nu.getHistoricPrice(companyCode,s,e)
  print('DEBUG : Calculating SMA for %s' % companyCode)
  sma200 = df['close'].rolling(200).mean()
  sma20 = df['close'].rolling(20).mean()
  mstd = df['close'].rolling(20).std()
  hband = sma20 + 2*mstd
  lband = sma20 - 2*mstd
  df=df.assign(sma200=sma200)
  df=df.assign(sma20=sma20)
  df=df.assign(hband=hband)
  df=df.assign(lband=lband)  
  
  print('DEBUG : Calculating MACD for %s' % companyCode)
  df['ema26'] = pd.ewma(df['close'], span=26)
  df['ema12'] = pd.ewma(df['close'], span=12)
  df['macd'] = (df['ema12'] - df['ema26'])
  print(df[['macd']].tail())
  
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

def processData(nseList, outputFilename):
  print(nseList)
  cList=[]
  for nseItem in nseList:
    print('PROCESSING : %s' % nseItem)
    '''try:
      c=processCompany(nseItem)
      cList.append(c)
    except:
       print('ERROR : %s' % nseItem)'''
    c=processCompany(nseItem)
    cList.append(c)

  dfPDFData = pd.DataFrame(cList)
  #print(dfPDFData)

  # Create PDF
  pdf = FPDF()
  for index, row in dfPDFData.iterrows():
    pdf.add_page()
    pdf.set_font("Arial", size=18)
    pdf.cell(20, 20, row['companyCode'])
    pdf.image( row['smaFilename'], x=20, y=40, w=170, h=110)
    pdf.image( row['candleFilename'], x=20, y=160, w=170, h=110)
  pdf.output(outputFilename)

# ------------------------------
# MAIN PROGRAM
# ------------------------------
outputFilename = '/home/ec2-user/plutus/reco.pdf'
dfTarget = pd.read_csv("/home/ec2-user/fortuna/fortuna/data/target.csv")[['type','companyName','targetPrice']]
dfFinYr = pd.read_csv("/home/ec2-user/fortuna/fortuna/data/finYr.csv")[['companyShortName','nseId']]
dfMerge=pd.merge(dfTarget, dfFinYr, left_on=['companyName'], right_on=['companyShortName'])
dfMerge=dfMerge[['nseId']].sort_values(by='nseId')
nseList=dfMerge['nseId'].unique()

nseList=['DABUR'] # TODO: Remove this

processData(nseList, outputFilename)

# Send Mail
fc.sendMail('Fortuna: Analysis Report','Analysis Report',outputFilename)

