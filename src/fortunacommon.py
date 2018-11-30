import os
import re

# -----------------------------------------------------------------------------
# Load property key/values from "fortuna.properties" file in "config" directory
# -----------------------------------------------------------------------------
def loadAppProperties():
  fileDir = os.path.dirname(os.path.abspath(__file__))
  propfile = os.path.join(fileDir, '../config/fortuna.properties')
  props = dict( l.rstrip().split('=') for l in open(propfile)
    if not l.startswith("#") )
  return props

# ---------------------------------------------------------------
# Get list of filenames in a directory which matches with pattern
# ---------------------------------------------------------------
def getFiles(inputDirectory,filenameRegexPattern):
  files = [f for f in os.listdir(inputDirectory) if re.match(filenameRegexPattern, f)]
  return files
