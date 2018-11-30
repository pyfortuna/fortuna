import os

# -----------------------------------------------------------------------------
# Load property key/values from "fortuna.properties" file in "config" directory
# -----------------------------------------------------------------------------
def loadAppProperties():
  fileDir = os.path.dirname(os.path.abspath(__file__))
  propfile = os.path.join(fileDir, '../config/fortuna.properties')
  props = dict( l.rstrip().split('=') for l in open(propfile)
    if not l.startswith("#") )
  return props
