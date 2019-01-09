# Import libraries
import datetime
import nseUtil as nu
import fortunacommon as fc
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Configure parameters
companyCode='ASHOKLEY'
e = datetime.datetime.now()
s = e - datetime.timedelta(days=500)

# Data preparation
df = nu.getHistoricPrice(companyCode,s,e)
boll_df=df[['close']]
sma200 = df['close'].rolling(200).mean()
df=df.assign(sma200=sma200)
df=df.dropna()
#df = df.reset_index()
df = df[['sma200','close']]
print(df.head())
print(df.tail())

# Plot chart
fig, ax = plt.subplots()
ax.plot_date(df.index.values,df['sma200'].values, fmt='r-', label='SMA/200')
ax.plot_date(df.index.values,df['close'].values, fmt='v-', label=companyCode)
plt.savefig('/home/ec2-user/plutus/plotsample002.png')

# Send mail
fc.sendMail('Plot','Plot','/home/ec2-user/plutus/plotsample002.png')
