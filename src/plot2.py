# Import libraries
import datetime
import nseUtil as nu
import fortunacommon as fc
import matplotlib.pyplot as plt
import pandas as pd

# Configure parameters
companyCode='ASHOKLEY'
e = datetime.datetime.now()
s = e - datetime.timedelta(days=365)

# Data preparation
history_df = nu.getHistoricPrice(companyCode,s,e)
boll_df=history_df[['close']]
sma200 = history_df['close'].rolling(200).mean()
history_df=history_df.assign(sma200=sma200)
history_df=history_df.dropna()
print(history_df.head())
print(history_df.tail())
history_df = history_df.reset_index()
history_df = history_df['sma200','close']
print(history_df.head())
print(history_df.tail())

# Plot chart
#plt.plot( y='sma200', data=history_df, color='skyblue', linewidth=4)
#plt.plot( y='close', data=history_df, color='olive', linewidth=2)
plt.plot(kind='line',x=history_df.index.values,y=history_df['sma200'])
plt.plot(kind='line',x=history_df.index.values,y=history_df['close'])
plt.savefig('/home/ec2-user/plutus/plotsample001.png', dpi=96, bbox_inches='tight')

# Send mail
fc.sendMail('Plot','Plot','/home/ec2-user/plutus/plotsample001.png')
