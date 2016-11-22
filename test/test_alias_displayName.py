import datetime
from time import sleep
import unittest
from test.config import group, account
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper.jiveHelper import jiveHelper
from test.helper.sendMailHelper import SendEmail, ReplyEmail
import re


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

    def test_shouldJiveShowCreatorDisplayNameAndSyncSyncCommentFromJiveWhenReplyEmailUseAlias(self):
        # subject = 'Discussion from Jive 2.23'
        subject = 'Gmail Reply Discussion Use alias ' + datetime.datetime.now().isoformat()

        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text="""
<div>
    <h1>Origin Discussion created By User2 from Jive</h1>
    <p>Some interesting text to discuss</p>
</div>
"""
        )
        self.assertEqual(content['subject'], subject, 'Subject not Matched')
        contentID = content['contentID']

        sleep(60)

        topicEmails = CheckEmailHelper.findEmailListBySubject(account["User4"], subject, to=group['groupKey'])

        original = topicEmails[0]

        TEXT = "reply from User 4 with alias on time: " + datetime.datetime.now().isoformat()
        HTML = "<div> %s </div>" % (TEXT)

        ReplyEmail(Subject=subject,
                   From=account["User4"],
                   To=[group['groupKey']],
                   ReplyTo=[group['groupKey']],
                   HTML=HTML,
                   Origin=original,
                   useAlias=True
                   )

        sleep(30)

        # check other group members can recieve email reply

        User1RecievedMail = \
            CheckEmailHelper.findEmailListBySubject(account["User1"], subject, to=group['groupKey'])[-1]
        User2RecievedMail = \
            CheckEmailHelper.findEmailListBySubject(account["User2"], subject, to=group['groupKey'])[-1]
        User5RecievedMail = \
            CheckEmailHelper.findEmailListBySubject(account["User5"], subject, to=group['groupKey'])[-1]

        textMail1 = User1RecievedMail.get_payload()[0].get_payload()
        textMail2 = User2RecievedMail.get_payload()[0].get_payload()
        textMail5 = User5RecievedMail.get_payload()[0].get_payload()

        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail1))
        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail2))
        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail5))

        # check comment replyed on Jive

        sleep(180)

        comment = jiveHelper.findAllCommentsByContentID(contentID)[0]
        AUTHOR_NAME = comment['onBehalfOf'].get('name') or comment['author']['displayName']

        self.assertNotEqual(comment, None, "Could not find Content")
        self.assertIsNotNone(re.search(r'%s' % 'reply from User 4', comment['content']['text']))
        self.assertEqual(AUTHOR_NAME, account['User4']['displayName'],
                         "Comment Creator not correct")
