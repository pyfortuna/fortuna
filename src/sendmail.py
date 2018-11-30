# Import libraries
import fortunacommon

# ------------
# Main program
# ------------
pr=fortunacommon.loadAppProperties()
subject="[Fortuna]: Yearly Financial results"
body="This is an automated e-mail message sent from Fortuna."
attachmentFilename = pr['finyr.output.filename']
fortunacommon.sendMail(subject,body,attachmentFilename)
