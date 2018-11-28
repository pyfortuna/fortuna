import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
print(fileDir)

props = dict( l.rstrip().split('=') for l in open("/home/ec2-user/fortuna/fortuna/config/fortuna.properties")
  if not l.startswith("#") )
print (props);
