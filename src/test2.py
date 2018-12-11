import datetime
import time


now = datetime.datetime.now()
print(now)
d1 = datetime.date.today()
print(d1)
d2 = d1 - datetime.timedelta(days=365)
print(d2)



start=d2
end=d1
difference = (end - start).days
  if difference > 100:
    curr_end = start + timedelta(days=100)
    while curr_end < end:
      start_fmt=time.strftime("%d-%m-%Y", start)
      end_fmt=time.strftime("%d-%m-%Y", curr_end)
      print(start_fmt + " to " + end_fmt)
      start = curr_end + timedelta(days=1)
      curr_end += timedelta(days=100)
