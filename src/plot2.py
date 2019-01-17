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
  macdFilename='/home/ec2-user/plutus/MACD_%s.png' % companyCode

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
  
  # Calculate MACD
  print('DEBUG : Calculating MACD for %s' % companyCode)
  df['ema26'] = df['close'].ewm(span=26,min_periods=0,adjust=False,ignore_na=False).mean()
  df['ema12'] = df['close'].ewm(span=12,min_periods=0,adjust=False,ignore_na=False).mean()
  df['macd'] = (df['ema12'] - df['ema26'])
  df['signal'] = df['macd'].ewm(span=9,min_periods=0,adjust=False,ignore_na=False).mean()
  
  # Calculate MACD histogram
  df['macdhisto'] = (df['macd'] - df['signal'])
  valList=list(df['macdhisto'])
  diffList = []
  diffList.append(0) # First item: Cannot calculate difference
  i = 1
  while i < len(valList):
    diffList.append(valList[i] - valList[i-1]) # Calculate difference with previous row
    i += 1
  seHistoDiff = pd.Series(diffList)
  df['macdhistodiff'] = seHistoDiff.values
  
  # Calculate histogram colour
  #  - If larger that previous value, then GREEN, else RED
  df['macdhistocolor'] = df['macdhistodiff'].apply(lambda x: '#FF0000' if x < 0 else '#00FF00')

  #print(df[['macd']].tail())  
  df=df.dropna()
  #print(df.head())
  
  # Create charts
  print('DEBUG : Creating charts for %s' % companyCode)
  imgWin=6.69 # 170 x 80 mm = 6.69 x 3.15 in
  imgHin=3.15
  sp.plotSMA(df,smaFilename,imgWin,imgHin) 
  sp.plotMACD(df,macdFilename,imgWin,imgHin)
  dfCandle=df.tail(30)
  #cp.plotCandlestick(df1,candleFilename,'%Y-%m-%d')
  cp.plotCandlestick(dfCandle,candleFilename,imgWin,imgHin)
  
  plotData = {
    "companyCode": companyCode,
    "smaFilename": smaFilename,
    "candleFilename": candleFilename,
    "macdFilename": macdFilename
  }
  return plotData

def processData(nseList, outputFilename):
  print(nseList)
  cList=[]
  for nseItem in nseList:
    print('PROCESSING : %s' % nseItem)
    c=processCompany(nseItem)
    cList.append(c)
    '''
    try:
      c=processCompany(nseItem)
      cList.append(c)
    except:
       print('ERROR : %s' % nseItem)
    '''

  dfPDFData = pd.DataFrame(cList)
  #print(dfPDFData)

  # Create PDF
  print('DEBUG : Creating PDF')
  pdf = FPDF()
  for index, row in dfPDFData.iterrows():
    pdf.add_page()
    pdf.set_font("Arial", size=18)
    pdf.cell(20, 20, row['companyCode'])
    imgHmm=80
    imgWmm=170
    pdf.image( row['smaFilename'], x=20, y=30, w=imgWmm, h=imgHmm)
    pdf.image( row['macdFilename'], x=20, y=115, w=imgWmm, h=imgHmm)
    pdf.image( row['candleFilename'], x=20, y=205, w=imgWmm, h=imgHmm)
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
nseList=['ASHOKLEY','DABUR'] # TODO: Remove this

processData(nseList, outputFilename)

# Send Mail
print('DEBUG : Sending Email')
fc.sendMail('Fortuna: Analysis Report','Analysis Report',outputFilename)

