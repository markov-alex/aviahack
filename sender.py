import smtplib, ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_mail(send_from, send_to, subject, text, files, server):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, 'rb') as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    server.sendmail(send_from, send_to, msg.as_string())
    server.close()



def send_files(send_to, subject, text, files):

    port = 465  # For SSL
    password = 'wealllovesamsung'

# Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.ehlo()
        server.login("samscomp2@gmail.com", password)
        send_mail("samscomp2@gmail.com", send_to, subject, text, files, server)
        print ('successfully sent the mail')

#send_files(["redpixelforce@gmail.com"], "example", 'example', ['1.txt'])