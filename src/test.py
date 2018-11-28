props = dict( l.rstrip().split('=') for l in open("../config/fortuna.properties")
  if not l.startswith("#") )
print (props);
