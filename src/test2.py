'''
  References:
    https://stackoverflow.com/questions/11492656/create-list-of-dictionary-python
'''
import datetime
import time

def get100DayList(start, end):
  NSE_DATE_FMT="%d-%m-%Y"
  dates={}
  datesList = []
  difference = (end - start).days
  if difference > 100:
    curr_end = start + datetime.timedelta(days=100)
    while curr_end < end:
      dates['start']=start.strftime(NSE_DATE_FMT)
      dates['end']=curr_end.strftime(NSE_DATE_FMT)
      datesList.append(dates.copy())
      start = curr_end + datetime.timedelta(days=1)
      curr_end += datetime.timedelta(days=100)
    if curr_end > end:
      dates['start']=start.strftime(NSE_DATE_FMT)
      dates['end']=end.strftime(NSE_DATE_FMT)
      datesList.append(dates.copy())
  else:
    dates['start']=start.strftime(NSE_DATE_FMT)
    dates['end']=curr_end.strftime(NSE_DATE_FMT)
    datesList.append(dates.copy())
  return datesList


e = datetime.datetime.now()
s = e - datetime.timedelta(days=365)
x = get100DayList(s,e)
print(x)
