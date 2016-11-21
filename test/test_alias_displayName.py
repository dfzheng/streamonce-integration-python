import datetime
from time import sleep
import unittest
from test.config import group, account
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper.jiveHelper import jiveHelper
from test.helper.sendMailHelper import SendEmail


class aliasTest(unittest.TestCase):
    def test_shouldJiveShowCreatorDisplayNameAndSyncEmailToRestOfGroupMemberWhenSendEmailUseAlias(self):
        subject = 'send Gmail with alias ' + datetime.datetime.now().isoformat()
        # subject = 'Email send to Group Email address 3.141'
        to = [group['groupKey']]
        htmlTitle = "Email send to Group Email with alias"
        htmlContent = "Current Time : " + datetime.datetime.now().isoformat()
        # htmlContent = "Current Time : 20161117"
        HTML = """
        <html>
        <head></head>
        <body>
            <div><font size="6"> %s </font></div>
            <div><font size="4"> %s </font></div>
        </body>
        </html>
        """ % (htmlTitle, htmlContent)

        SendEmail(Subject=subject, From=account["User4"], HTML=HTML, To=to, useAlias=True)
        sleep(180)
        content = jiveHelper.findContentBySubject(subject)

        AUTHOR_NAME =content['onBehalfOf'].get('name') or content['author']['displayName']

        self.assertNotEqual(content, None, "Could not find Content")
        self.assertEqual(content['subject'], subject, 'content title not matched')
        self.assertEqual(AUTHOR_NAME, account['User4']['displayName'],
                         "Content Creator not correct")

        Mail1 = CheckEmailHelper.findEmailBySubject(account["User1"], subject, to=group['groupKey'])
        Mail2 = CheckEmailHelper.findEmailBySubject(account["User2"], subject, to=group['groupKey'])
        Mail4 = CheckEmailHelper.findEmailBySubject(account["User4"], subject, to=group['groupKey'])
        Mail5 = CheckEmailHelper.findEmailBySubject(account["User5"], subject, to=group['groupKey'])

        self.assertEqual(Mail1['Subject'], subject)
        self.assertEqual(Mail2['Subject'], subject)
        self.assertEqual(Mail4, None)
        self.assertEqual(Mail5['Subject'], subject)