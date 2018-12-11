import datetime

now = datetime.datetime.now()
print(now)
d1 = datetime.date.today()
print(d1)
d2 = d1 - datetime.timedelta(days=365)
print(d2)

'''
start=
difference = (end - start).days
if difference > 100:
curr_end = start + timedelta(days=100)
while curr_end < end:
'''
