# Import libraries
import datetime
import nseUtil as nu
import fortunacommon as fc
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Configure parameters
companyCode='ASHOKLEY'
numDays=700
e = datetime.datetime.now()
s = e - datetime.timedelta(days=numDays)

# Data preparation
df = nu.getHistoricPrice(companyCode,s,e)
sma200 = df['close'].rolling(200).mean()
sma20 = df['close'].rolling(20).mean()
df=df.assign(sma200=sma200)
df=df.assign(sma20=sma20)
df=df.dropna()
df = df[['sma200','sma20','close']]
#df['date'] = pd.to_datetime(df.index, format="%d-%b-%Y")
#df=df.set_index('date')
print(df.head())
#print(df.tail())

# Plot chart
fig, ax = plt.subplots()
ax.plot_date(df.index.values, df['sma200'].values, fmt='b-', linewidth=1, label='SMA/200')
ax.plot_date(df.index.values, df['sma20'].values, fmt='g-', linewidth=1, label='SMA/20')
ax.plot_date(df.index.values, df['close'].values, fmt='r-', linewidth=1, label=companyCode)
ax.legend()
ax.xaxis_date()
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
plt.savefig('/home/ec2-user/plutus/plotsample003.png', dpi=300)

# Send mail
fc.sendMail('Plot','Plot','/home/ec2-user/plutus/plotsample003.png')
