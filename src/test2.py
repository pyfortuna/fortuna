import datetime
import time


end=datetime.datetime.now()
start=end - datetime.timedelta(days=365)

difference = (end - start).days
if difference > 100:
  curr_end = start + datetime.timedelta(days=100)
  while curr_end < end:
    start_fmt=start.strftime("%d-%m-%Y")
    end_fmt=curr_end.strftime("%d-%m-%Y")
    print(start_fmt + " to " + end_fmt)
    start = curr_end + datetime.timedelta(days=1)
    curr_end += datetime.timedelta(days=100)
  if curr_end > end:
    #start = curr_end + datetime.timedelta(days=1)
    start_fmt=start.strftime("%d-%m-%Y")
    end_fmt=end.strftime("%d-%m-%Y")
    print(start_fmt + " to " + end_fmt)
else:
  start_fmt=start.strftime("%d-%m-%Y")
  end_fmt=end.strftime("%d-%m-%Y")
  print(start_fmt + " to " + end_fmt)
  
