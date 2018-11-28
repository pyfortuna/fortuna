props = dict( l.rstrip().split('=') for l in open("/home/ec2-user/fortuna/fortuna/config/fortuna.properties")
  if not l.startswith("#") )
print (props);
