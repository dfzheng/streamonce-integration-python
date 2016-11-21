import datetime
from time import sleep
import unittest
import re
from test.config import group, account
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper.jiveHelper import jiveHelper
from test.helper.utilHelper import decodeQP
from xml.sax.saxutils import unescape

class SpecialCharsTest(unittest.TestCase):
    def test_shouldSyncSpecialCharsFromJive(self):
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()
        # subject = 'SO Test Discussion 6.6'
        POST_TEXT = "Sample discuss 这是一个有趣的讨论 非常---有趣&nbsp;&nbsp;do you like it ?"
        POST_CONTENT = "<div> %s </div>" % (POST_TEXT)

        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text = POST_CONTENT
        )
        self.assertEqual(content['subject'], subject, 'Subject not Matched')

        sleep(180)

        Mail1 = CheckEmailHelper.findEmailBySubject(account["User1"], subject, to=group['groupKey'])
        Mail2 = CheckEmailHelper.findEmailBySubject(account["User2"], subject, to=group['groupKey'])
        Mail4 = CheckEmailHelper.findEmailBySubject(account["User4"], subject, to=group['groupKey'])
        Mail5 = CheckEmailHelper.findEmailBySubject(account["User5"], subject, to=group['groupKey'])

        self.assertEqual(Mail1['Subject'], subject)
        self.assertEqual(Mail2['Subject'], subject)
        self.assertEqual(Mail4['Subject'], subject)
        self.assertEqual(Mail5['Subject'], subject)

        MailContent1 = decodeQP(Mail1.get_payload())
        MailContent2 = decodeQP(Mail2.get_payload())
        MailContent4 = decodeQP(Mail4.get_payload())
        MailContent5 = decodeQP(Mail5.get_payload())

        self.assertIsNotNone(re.search(r'%s' % unescape(POST_TEXT), unescape(MailContent1)))
        self.assertIsNotNone(re.search(r'%s' % unescape(POST_TEXT), unescape(MailContent2)))
        self.assertIsNotNone(re.search(r'%s' % unescape(POST_TEXT), unescape(MailContent4)))
        self.assertIsNotNone(re.search(r'%s' % unescape(POST_TEXT), unescape(MailContent5)))
