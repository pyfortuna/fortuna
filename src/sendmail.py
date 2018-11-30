# Import libraries
import smtplib
import os
from os.path import basename
import fortunacommon
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def sendMail(subject,body,attachmentFilename):
    pr=fortunacommon.loadAppProperties()
    gmail_user=pr['mail.user.id']
    gmail_password=pr['mail.user.password']
    recipient_address=pr['mail.recepient.address']    

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)

        # Message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        content = MIMEText(body, 'plain')
        msg.attach(content)

        # Add attachment        
        with open(attachmentFilename, "rb") as attachmentFile:
            part = MIMEApplication(
                attachmentFile.read(),
                Name=basename(attachmentFilename)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachmentFilename)
        msg.attach(part)

        # Send mail
        server.sendmail(gmail_user, recipient_address, msg.as_string())
        server.close()    

        print('Email sent!')
    except:
        print('Something went wrong...')

# ------------
# Main program
# ------------
pr=fortunacommon.loadAppProperties()
subject="[Fortuna]: Yearly Financial results"
body="This is an automated e-mail message sent from Fortuna."
attachmentFilename = pr['finyr.output.filename']
sendMail(subject,body,attachmentFilename)
