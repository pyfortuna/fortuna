import datetime
import time


end=datetime.datetime.now()
start=end - datetime.timedelta(days=365)

dates = {}
datesList = []
difference = (end - start).days
if difference > 100:
  curr_end = start + datetime.timedelta(days=100)
  while curr_end < end:
    dates['start']=start.strftime("%d-%m-%Y")
    dates['end']=curr_end.strftime("%d-%m-%Y")
    datesList.append(dates)
    start = curr_end + datetime.timedelta(days=1)
    curr_end += datetime.timedelta(days=100)
  if curr_end > end:
    #start = curr_end + datetime.timedelta(days=1)
    dates['start']=start.strftime("%d-%m-%Y")
    dates['end']=curr_end.strftime("%d-%m-%Y")
    datesList.append(dates)
else:
  dates['start']=start.strftime("%d-%m-%Y")
  dates['end']=curr_end.strftime("%d-%m-%Y")
  datesList.append(dates)
  
print(datesList)
