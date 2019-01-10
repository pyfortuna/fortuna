# Import libraries
import datetime
import nseUtil as nu
import fortunacommon as fc
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import candleplot as cp
import smaplot as sp

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

cList=[]
c=processCompany('ASHOKLEY')
cList.append(c)
c=processCompany('DABUR')
cList.append(c)
dfPDFData = pd.DataFrame(cList)
print(dfPDFData)
