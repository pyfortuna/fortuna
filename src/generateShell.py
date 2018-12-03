import fortunacommon

# --------------------------------------------------------
# Main program
# --------------------------------------------------------

pr=fortunacommon.loadAppProperties()
f = open(pr['genshell.input.filename'], 'r')
mcList = f.read().splitlines()
f.close()

fYrFin= open(pr['genshell.output.finyr.filename'],"w+")

for mcListItem in mcList:
  mc = fortunacommon.Moneycontrol(mcListItem)
  yrFinGetCommand = "wget " + mc.getYrFinURL() + " -O " + pr['finyr.input.directory'] + mc.getCompanyName() + ".html" + "\n"
  fYrFin.write(yrFinGetCommand)

fYrFin.write("exit\n")
fYrFin.close()
# --------------------------------------------------------


