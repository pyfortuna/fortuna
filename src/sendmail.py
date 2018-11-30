import smtplib
import os
from os.path import basename
import fortunacommon
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pr=fortunacommon.loadAppProperties()
gmail_user=pr['mail.user.id']
gmail_password=pr['mail.user.password']
recipient_address=pr['mail.recepient.address']
subject="[Fortuna]: Yearly Financial results"
body="This is an automated e-mail message sent from Fortuna."

#email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (gmail_user, to, subject, body)

try:  
    msg = MIMEMultipart('alternative')
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    
    # Message
    msg['Subject'] = subject
    msg['From'] = gmail_user
    content = MIMEText(body, 'plain')
    msg.attach(content)
   
    # Attachment
    #attachmentFilename = pr['finyr.output.filename']
    #print(attachmentFilename)
    #attachmentFile = file(attachmentFilename)
    #print(attachmentFile)
    #attachment = MIMEText(attachmentFile.read())
    #attachment.add_header('Content-Disposition', 'attachment', filename=attachmentFilename)           
    #msg.attach(attachment)
    
    #
    f = pr['finyr.output.filename']
    print("f: " + f)
    with open(f, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(f)
        )
    print("[[[2]]]")
    # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
    print("[[[3]]]")
    msg.attach(part)
    print("[[[4]]]")
    
    server.sendmail(gmail_user, recipient_address, msg.as_string())
    server.close()    
    
    print('Email sent!')
except Exception, err:
    print('Something went wrong...')
    print Exception, err
