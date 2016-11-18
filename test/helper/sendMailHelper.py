import smtplib
from email.mime.image       import MIMEImage
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from email.mime.message     import MIMEMessage
import email

import os, json
import uuid
import pdb
import re
from bs4 import BeautifulSoup

with open(os.getcwd() + '/env.json') as json_data:
    env = json.load(json_data)

with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)


def SendEmail(Subject="[SO-TEST] Template", From=account["User1"], To=[], Preamble="", TEXT="", HTML="", ReplyTo=[]):
    if len(To) == 0:
        raise Exception("no reciever")

    print('Sending mail From: %s , Subject: %s' % (From["email"], Subject))

    To = ", ".join(To)

    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['From'] = From["email"]
    msg['To'] = To

    if len(ReplyTo) > 0:
        msg.add_header('reply-to', ", ".join(ReplyTo))

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

def ReplyEmail(Subject="[SO-TEST] Template", From=account["User1"], To=[], HTML="", ReplyTo=[], Origin=None):
    origin_html = Origin.get_payload()
    reply_html = HTML
    compressed_origin_html = '<div class="gmail_extra"><div class="gmail_quote"><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex">'
    compressed_origin_html += origin_html + '</blockquote></div></div>'
    new_html = reply_html + compressed_origin_html

    reply_doc = BeautifulSoup(reply_html, 'html.parser')
    origin_doc = BeautifulSoup(origin_html, 'html.parser')

    reply_text = reply_doc.text
    origin_text = re.sub('\n', '\n> ', origin_doc.text)

    new_text = reply_text + origin_text

    email.charset.add_charset('utf-8', email.charset.SHORTEST, email.charset.QP)
    html_block = MIMEText(new_html, 'html', 'utf-8')
    del html_block['Content-Transfer-Encoding']
    html_block['Content-Transfer-Encoding'] = 'QUOTED-PRINTABLE'

    print(html_block)

    text_block = MIMEText(new_text, 'plain', _charset='utf-8')

    print('Sending mail From: %s , Subject: %s' % (From["email"], Subject))

    for part in Origin.walk():
        if (part.get('Content-Disposition')
            and part.get('Content-Disposition').startswith("attachment")):

            part.set_type("text/plain")
            part.set_payload("Attachment removed: %s (%s, %d bytes)"
                             %(part.get_filename(),
                               part.get_content_type(),
                               len(part.get_payload(decode=True))))
            del part["Content-Disposition"]
            del part["Content-Transfer-Encoding"]


    new_block = MIMEMultipart('alternative')
    new_block.attach(text_block)
    new_block.attach(html_block)

    new_block["Message-ID"] = email.utils.make_msgid()
    new_block["In-Reply-To"] = Origin["Message-ID"]
    new_block["References"] = Origin["Message-ID"]
    new_block["Subject"] = "Re: "+Origin["Subject"]
    new_block["To"] = new_block["Reply-To"] = Origin["Reply-To"] or Origin["From"]
    new_block["From"] = From["email"]

    print(new_block.as_string())

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(From["email"], From["password"])
    server.send_message(new_block)
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
