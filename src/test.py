import os
import sys

fileDir = os.path.dirname(os.path.abspath(__file__))
print(fileDir)
propfile = os.path.join(fileDir, '../config/fortuna.properties')
print(propfile)

props = dict( l.rstrip().split('=') for l in open(propfile)
  if not l.startswith("#") )
print (props);
