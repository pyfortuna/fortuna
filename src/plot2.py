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
s = e - datetime.timedelta(days=600)

# Data preparation
df = nu.getHistoricPrice(companyCode,s,e)
boll_df=df[['close']]
sma200 = df['close'].rolling(200).mean()
df=df.assign(sma200=sma200)
df=df.dropna()
#df = df.reset_index()
df = df[['sma200','close']]
df['date'] = pd.to_datetime(df.index, format="%d-%b-%Y")
df=df.set_index('date')

print(df.head())
print(df.tail())

# Plot chart
fig, ax = plt.subplots()
ax.plot_date(df.index.values,df['sma200'].values, fmt='b-', label='SMA/200')
ax.plot_date(df.index.values,df['close'].values, fmt='r-', label=companyCode)
ax.xaxis_date()
ax.xaxis.set_major_locator(plt.MaxNLocator(6))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
plt.savefig('/home/ec2-user/plutus/plotsample002.png')

# Send mail
fc.sendMail('Plot','Plot','/home/ec2-user/plutus/plotsample002.png')
