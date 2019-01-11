import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plotSMA(df,smaFilename,w,h):
  fig, ax = plt.subplots(figsize=(w,h))
  ax.plot_date(df.index.values, df['sma200'].values, color='b', linestyle='solid', marker=',', linewidth=1, label='SMA/200')
  ax.plot_date(df.index.values, df['sma20'].values, color='g', linestyle='solid', marker=',', linewidth=1, label='SMA/20')
  ax.plot_date(df.index.values, df['close'].values, color='#B72015', linestyle='solid', marker=',', linewidth=1, label='Price')
  #ax.fill_between(df.index.values, df['hband'].values, df['lband'].values, color='blue', alpha=0.3)
  ax.legend(frameon=False)
  ax.xaxis_date()
  ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
  plt.savefig(smaFilename, dpi=300, bbox_inches='tight', pad_inches=0)

def plotMACD(df,macdFilename,w,h):
  fig, ax = plt.subplots(figsize=(w,h))
  ax.plot_date(df.index.values, df['macd'].values, color='#B72015', linestyle='solid', marker=',', linewidth=1, label='MACD')
  ax.legend(frameon=False)
  ax.xaxis_date()
  ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[3,6,9,12]))
  ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
  plt.savefig(macdFilename, dpi=300, bbox_inches='tight', pad_inches=0)
