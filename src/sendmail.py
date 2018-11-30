import smtplib
import os
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
    attachmentFilename = pr['finyr.output.filename']
    print(attachmentFilename)
    attachmentFile = file(attachmentFilename)
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(open(attachmentFile, 'rb').read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachmentFile))
    msg.attach(attachment)

    
    server.sendmail(gmail_user, recipient_address, msg.as_string())
    server.close()    
    
    print('Email sent!')
except:  
    print('Something went wrong...')
