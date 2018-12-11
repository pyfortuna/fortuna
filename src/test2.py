import datetime
import time


now = datetime.datetime.now()
print(now)
#d1 = datetime.date.today())
d1 = datetime.datetime.now()
print(d1)
d2 = d1 - datetime.timedelta(days=365)
print(d2)



start=d2
end=d1
difference = (end - start).days
if difference > 100:
  curr_end = start + datetime.timedelta(days=100)
  while curr_end < end:
    start_fmt=start.strftime("%d-%m-%Y")
    end_fmt=curr_end.strftime("%d-%m-%Y")
    print(start_fmt + " to " + end_fmt)
    start = curr_end + datetime.timedelta(days=1)
    curr_end += datetime.timedelta(days=100)
