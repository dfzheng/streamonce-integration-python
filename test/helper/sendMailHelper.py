import smtplib
from email.mime.image       import MIMEImage
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText

import os, json
import uuid

with open(os.getcwd() + '/env.json') as json_data:
    env = json.load(json_data)

with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)


def SendEmail(Subject="[SO-TEST] Template", From=account["User1"], To=[], Preamble="", TEXT="", HTML=""):
    if len(To) == 0:
        raise Exception("no reciever")

    print('Sending mail From: %s , Subject: %s' % (From["email"], Subject))

    To = ", ".join(To)

    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = From["email"]
    msg['To'] = To
    msg.preamble = Preamble

    if len(TEXT) > 0:
        msg.attach(MIMEText(TEXT, 'plain', 'utf-8'))
    if len(HTML) > 0:
        msg.attach(MIMEText(HTML, 'html', 'utf-8'))

    if len(TEXT) == 0 and len(HTML) == 0:
        msg.attach(MIMEText("Empty Email", 'plain', 'utf-8'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(From["email"], From["password"])
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    SendEmail(
        Subject="This is from sendMailHelper",
        From=account["User1"],
        To=["streamonceintegrationtest2" + env["google"]["domainName"]],
        Preamble="Ok, Ok",
        TEXT="Text Yes",
        HTML="""
<html>
<head></head>
<body>
    <h2> HTML <h2>
    <p> Ok </p>
</body>
</html>
"""
    )
