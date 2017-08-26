import smtplib
import os
import json
from email.mime.image       import MIMEImage
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText
from email.mime.message     import MIMEMessage
from email.mime.application import MIMEApplication
import sys
sys.path.insert(0,'../..')
from test.helper import CheckEmailHelper
from os.path import basename
from test.helper import config
import email
import uuid
import pdb
import re
from bs4 import BeautifulSoup


HOST = 'imap.gmail.com'

with open('env.json') as json_data:  # os.getcwd() Return the current working directory
    env = json.load(json_data)

with open('accounts.json') as json_data:
    account = json.load(json_data)


def SendEmail(Subject="[SO-TEST] Template", From=account["User1"], To=[], Preamble="", TEXT="", Attachment=[], HTML="", ReplyTo=[], useAlias=False):
    if len(To) == 0:
        raise Exception("no reciever")

    print('Sending mail From: %s , Subject: %s' % (From["email"], Subject))

    # To = ", ".join(To)

    msg = MIMEMultipart()
    msg['Subject'] = Subject
    msg['To'] = To
    msg['To'] = msg['To'].replace(","," ")
    msg['Delivered-To'] = From["email"]

    if useAlias==False:
        msg['From'] =  From["displayName"] + " <"+From["email"] +">"
    else:
        msg['From'] = From["displayName"] + " <"+From["alias"] +">"



    if len(ReplyTo) > 0:
        msg.add_header('reply-to', ", ".join(ReplyTo))

    msg.preamble = Preamble

    if len(TEXT) > 0:
        msg.attach(MIMEText(TEXT, 'plain', 'utf-8'))
    if len(HTML) > 0:
        msg.attach(MIMEText(HTML, 'html', 'utf-8'))

    if len(TEXT) == 0 and len(HTML) == 0:
        msg.attach(MIMEText("Empty Email", 'plain', 'utf-8'))

    if len(Attachment) > 0:
        msg.add_header("Content-Disposition","attachment", filename=Attachment[0]["name"])
        msg.add_header('Content-Type','image/jpeg', name=Attachment[0]["name"])


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(From["email"], From["googlePassword"])
    server.send_message(msg)
    server.quit()

def ReplyEmailwithImage(Subject="[SO-TEST] Template", From=account["User1"], Cc=[], To=[],TEXT="", HTML="", Replyto=[], Origin=None, Images=[], useAlias=False):

    email.charset.add_charset('utf-8', email.charset.SHORTEST, email.charset.QP)
    new_text = ""
    new_html = ""

    if TEXT!="" and HTML!="":
        new_text = TEXT
        new_html = HTML
    else :
        import quopri as qp
        origin_html = str(qp.decodestring(Origin.get_payload()[0]._payload[1]._payload), 'utf-8')
        reply_html = HTML
        compressed_origin_html = '<div class="gmail_extra"><div class="gmail_quote"><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex">'
        compressed_origin_html += origin_html + '</blockquote></div></div>'
        new_html = reply_html + compressed_origin_html

        reply_doc = BeautifulSoup(reply_html, 'html.parser')   #BeautifulSoup is to pull data from HTML&XML

        origin_doc = BeautifulSoup(origin_html, 'html.parser')
        #拼回复信的所有text
        reply_text = reply_doc.text
        origin_text = re.sub('\n', '\n> ', "\n\n" + origin_doc.text)
        new_text = reply_text + origin_text


    text_block = MIMEText(new_text, 'plain', _charset='utf-8')
    html_block = MIMEText(new_html, 'html', 'utf-8')

    del html_block['Content-Transfer-Encoding']
    html_block['Content-Transfer-Encoding'] = 'quoted-printable'

    print('Sending mail From: %s , Subject: %s' % (From["email"], Origin["Subject"]))


    # for part in Origin.walk():
    #     if (part.get('Content-Disposition')
    #         and part.get('Content-Disposition').startswith("attachment")):
    #
    #         part.set_type("text/plain")
    #         part.set_payload("Attachment removed: %s (%s, %d bytes)"
    #                          %(part.get_filename(),
    #                            part.get_content_type(),
    #                            len(part.get_payload(decode=True))))
    #         del part["Content-Disposition"]
    #         del part["Content-Transfer-Encoding"]


    new_block = MIMEMultipart()
    new_block["Message-ID"] = email.utils.make_msgid()   #生成新的messageid
    new_block["In-Reply-To"] = Origin["Message-ID"]
    new_block["References"] = Origin["Message-ID"]
    new_block["Subject"] = "Re: "+Origin["Subject"]
    new_block["To"] = new_block["Reply-To"] = Origin["Reply-To"] or Origin["From"]
    new_block["From"] = From['email']
    new_block["Cc"] = Cc
    new_block["Delivered-To"] = From["email"]

    #add attachment
    part = MIMEApplication(open(Images[0]["path"],'rb').read(),'image/jpeg')
    part.add_header('Content-Disposition', 'attachment', filename=Images[0]["name"])
    del part['Content-Type']
    part.add_header('Content-Type','image/jpeg', name=Images[0]["name"])

    multi1 = MIMEMultipart('alternative')
    multi1.attach(text_block)
    multi1.attach(html_block)

    new_block.attach(multi1)
    new_block.attach(part)



    if useAlias==False:
        new_block["From"] =  From["displayName"] + " <"+From["email"] +">"
    else:
        new_block["From"] = From["displayName"] + " <"+From["alias"] +">"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(From["email"], From["googlePassword"])
    server.send_message(new_block)
    server.quit()

    return new_block["Subject"];

if __name__ == "__main__":
    SendEmail(
        Subject="This is from sendMailHelper",
        From=account["User1"],
        To=["one-plus@" + env["google"]["domainName"]],
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
