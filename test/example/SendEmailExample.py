import smtplib
from email.mime.image       import MIMEImage
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText

import os, json
import uuid

with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)

COMMA = ', '

msg = MIMEMultipart()
msg['Subject'] = 'Python Email Title'
msg['From'] = account["User1"]["email"]

recievers = [account["User4"]["email"], account["User5"]["email"]]
msg['To'] = COMMA.join(recievers)

msg.preamble = 'Should had an Image with HTML Content'


# attach Images
pngfiles = [os.getcwd() + '/test/asserts/image1.png',
            os.getcwd() + '/test/asserts/image2.png']

for file in pngfiles:
    with open(file, 'rb') as fp:
        img = MIMEImage(fp.read())
    msg.attach(img)


# attach plain and HTML content

text = "Hi\nHow are you?\nThis is plain Text with 中文\n\n"

html = """
<html>
    <head></head>
    <body>
        <p> Hi! </p>
        <h2> kind of title </h2>
        <p> This is a <b>html</b> <a href="https://www.baidu.com">content</a> </p>
    </body>
</html>
"""

part1 = MIMEText(text, 'plain', 'utf-8')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)

# attach inline Image

inlineImage= dict(title='inline', path=os.getcwd() + '/test/asserts/inline.png', cid=str(uuid.uuid4()))

htmlWithInlineImage = """
<html>
    <head></head>
    <body>
        <h2> Inline Image should display below </h2>
        <img src="cid:{cid}" alt="{alt}"> bad<br>
        <p> end of this part </p>
    </body>
</html>
""".format(alt=inlineImage['title'], **inlineImage)

part3 = MIMEText(htmlWithInlineImage, 'html', 'utf-8')
msg.attach(part3)

with open(inlineImage['path'], 'rb') as file:
    img = MIMEImage(file.read(), name=os.path.basename(inlineImage['path']))
    msg.attach(img)
    img.add_header('Content-ID', '<{0}>'.format(inlineImage['cid']))


server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(account["User1"]["email"], account["User1"]["password"])

server.send_message(msg)
server.quit()


