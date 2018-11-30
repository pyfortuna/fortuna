import smtplib
import fortunacommon

pr=fortunacommon.loadAppProperties()
gmail_user=pr['mail.user.id']
gmail_password=pr['mail.user.password']
to=pr['mail.recepient.address']
subject="[Fortuna]: test mail"
body="This is an automated mail message."

email_text = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (gmail_user, to, subject, body)

try:  
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(gmail_user, to, email_text)
    server.close()

    print('Email sent!')
except:  
    print('Something went wrong...')
