import os
import sys

fileDir = os.path.dirname(os.path.realpath('__file__'))
print(fileDir)
print(os.path.join(fileDir, '../config/fortuna.properties'))
print(os.getcwd())
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(sys.executable))

props = dict( l.rstrip().split('=') for l in open("/home/ec2-user/fortuna/fortuna/config/fortuna.properties")
  if not l.startswith("#") )
print (props);
