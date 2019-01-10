# Import libraries
import datetime
import nseUtil as nu
import fortunacommon as fc
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import candleplot as cp

# Configure parameters
companyCode='ASHOKLEY'
numDays=700
candleFilename='/home/ec2-user/plutus/candleplot003.png'
smaFilename='/home/ec2-user/plutus/smaplot003.png'

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
#df = df[['sma200','sma20','close']]
#df['date'] = pd.to_datetime(df.index, format="%d-%b-%Y")
#df=df.set_index('date')
print(df.head())
#print(df.tail())

# Plot chart
fig, ax = plt.subplots(figsize=(6.69,4.33)) # 170 x 110 mm = 6.69 x 4.33 in
ax.plot_date(df.index.values, df['sma200'].values, color='b', linestyle='solid', marker=',', linewidth=1, label='SMA/200')
ax.plot_date(df.index.values, df['sma20'].values, color='g', linestyle='solid', marker=',', linewidth=1, label='SMA/20')
ax.plot_date(df.index.values, df['close'].values, color='r', linestyle='solid', marker=',', linewidth=1, label=companyCode)
#ax.fill_between(df.index.values, df['hband'].values, df['lband'].values, color='blue', alpha=0.3)
ax.legend(frameon=False)
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
plt.savefig(smaFilename, dpi=300)

df1=df.tail(30)
#cp.plotCandlestick(df1,candleFilename,'%Y-%m-%d')
cp.plotCandlestick(df1,candleFilename)


# Send mail
#fc.sendMail('SMA','',smaFilename)
#fc.sendMail('Candle','',candleFilename)
