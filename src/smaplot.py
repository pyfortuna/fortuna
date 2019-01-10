import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plotSMA(df,smaFilename):
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
