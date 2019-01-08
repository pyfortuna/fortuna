# Import libraries
import datetime
import nseUtil as nu
import fortunacommon as fc
import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np #test
import matplotlib.dates as mdates

# Configure parameters
companyCode='ASHOKLEY'
e = datetime.datetime.now()
s = e - datetime.timedelta(days=500)


# Data preparation
history_df = nu.getHistoricPrice(companyCode,s,e)
boll_df=history_df[['close']]
sma200 = history_df['close'].rolling(200).mean()
history_df=history_df.assign(sma200=sma200)
history_df=history_df.dropna()
#print(history_df.head())
#print(history_df.tail())
#history_df = history_df.reset_index()
history_df = history_df[['sma200','close']]
print(history_df.head())
print(history_df.tail())


# Plot chart
# format the ticks
fig, ax = plt.subplots()
years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)
#plt.plot( y='sma200', data=history_df, color='skyblue', linewidth=4)
#plt.plot( y='close', data=history_df, color='olive', linewidth=2)
ax.plot(history_df.index.values,history_df['sma200'].values, color='skyblue', label='SMA/200')
ax.plot(history_df.index.values,history_df['close'].values, color='olive', label=companyCode)
ax.legend()
plt.savefig('/home/ec2-user/plutus/plotsample001.png')
'''
plt.plot(x,np.sin(x))
plt.plot(x,np.cos(x))
plt.savefig('/home/ec2-user/plutus/study001.png')
'''

# Send mail
fc.sendMail('Plot','Plot','/home/ec2-user/plutus/plotsample001.png')
