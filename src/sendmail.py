import smtplib
import fortunacommon
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pr=fortunacommon.loadAppProperties()
gmail_user=pr['mail.user.id']
gmail_password=pr['mail.user.password']
recipient_address=pr['mail.recepient.address']
subject="[Fortuna]: test mail"
body="This is an automated mail message."

#email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (gmail_user, to, subject, body)

try:  
    msg = MIMEMultipart('alternative')
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    msg['Subject'] = subject
    msg['From'] = gmail_user
    content = MIMEText(body, 'plain')
    msg.attach(content)
    server.sendmail(gmail_user, recipient_address, msg.as_string())
    server.close()

    print('Email sent!')
except:  
    print('Something went wrong...')
