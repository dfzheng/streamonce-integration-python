from test.helper.userHelper import UserHelper
from test.helper.jiveHelper import jiveHelper
from test.helper.googleHelper import GoogleHelper
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper.sendMailHelper import SendEmail, ReplyEmail
from test.helper.utilHelper import *
import datetime
from time import sleep
from xml.sax.saxutils import escape, unescape
from test.config import env, account, group
import unittest
import pdb
import re

class AttachmentTest(unittest.TestCase):
    def test_shouldHaveEmailNotificationWithAttachment(self):
        subject = 'SO Test Discussion With Attachment ' + datetime.datetime.now().isoformat()
        # subject = 'SO Test Discussion With Attachment 2017-01-10T14:53:37.027608'
        attachmentName = "attachment1.jpg";
        attachments = [{
            "doUpload": True,
            "name": attachmentName,
            "url": "http://pics.sc.chinaz.com/files/pic/pic9/201508/apic14052.jpg"
      }]
        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text="""
<div>
    <h1>Sample discuss</h1>
    <p>Some interesting text to discuss</p>
</div>
""",
            attachments=attachments
        )
        self.assertEqual(content['subject'], subject, 'Subject not Matched')

        sleep(60)

        Mail1 = CheckEmailHelper.findEmailBySubject(account["User1"], subject, to=group['groupKey'])
        Mail2 = CheckEmailHelper.findEmailBySubject(account["User2"], subject, to=group['groupKey'])
        Mail4 = CheckEmailHelper.findEmailBySubject(account["User4"], subject, to=group['groupKey'])
        Mail5 = CheckEmailHelper.findEmailBySubject(account["User5"], subject, to=group['groupKey'])

        self.assertEqual(Mail1['Subject'], subject)
        self.assertEqual(Mail2['Subject'], subject)
        self.assertEqual(Mail4['Subject'], subject)
        self.assertEqual(Mail5['Subject'], subject)

        self.assertEqual(Mail1.get_payload()[0]["Content-Disposition"], 'attachment; filename='+attachmentName)
        self.assertEqual(Mail2.get_payload()[0]["Content-Disposition"], 'attachment; filename='+attachmentName)
        self.assertEqual(Mail4.get_payload()[0]["Content-Disposition"], 'attachment; filename='+attachmentName)
        self.assertEqual(Mail5.get_payload()[0]["Content-Disposition"], 'attachment; filename='+attachmentName)