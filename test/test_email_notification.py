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

class EmailNotificationTest(unittest.TestCase):

    def test_shouldHaveEmailNotification(self):
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()
        # subject = 'SO Test Discussion 884434419'
        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text = """
<div>
    <h1>Sample discuss</h1>
    <p>Some interesting text to discuss</p>
</div>
"""
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

    def test_shouldCreateContentOnJiveAndSyncEmailToRestOfGroupMember(self):
        subject = 'Email send to Group Email address ' + datetime.datetime.now().isoformat()
        # subject = 'Email send to Group Email address 3.141'
        to = group['groupKey']
        htmlTitle = "Email send to Group Email"
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

        SendEmail(Subject=subject, From=account["User2"], HTML=HTML, To=to)
        sleep(180)
        content = jiveHelper.findContentBySubject(subject)

        self.assertNotEqual(content, None, "Could not find Content")
        self.assertEqual(content['subject'], subject, 'content title not matched')
        self.assertEqual(content['author']['displayName'], account['User2']['displayName'], "Content Creator not correct")

        Mail1 = CheckEmailHelper.findEmailBySubject(account["User1"], subject, to=group['groupKey'])
        Mail2 = CheckEmailHelper.findEmailBySubject(account["User2"], subject, to=group['groupKey'])
        Mail4 = CheckEmailHelper.findEmailBySubject(account["User4"], subject, to=group['groupKey'])
        Mail5 = CheckEmailHelper.findEmailBySubject(account["User5"], subject, to=group['groupKey'])

        self.assertEqual(Mail1['Subject'], subject)
        self.assertEqual(Mail2, None)
        self.assertEqual(Mail4['Subject'], subject)
        self.assertEqual(Mail5['Subject'], subject)

    def test_shouldSyncCommentToRestOfGroupMember(self):
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()
        # subject = 'Discussion from Jive 2.2360'
        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text = """
<div>
    <h1>Origin Discussion created By User2 from Jive</h1>
    <p>For Comment from Jive Testing</p>
</div>
"""
        )
        self.assertEqual(content['subject'], subject, 'Subject not Matched')

        # contentID = content["discussion"].split('/')[-1]
        contentID = content['contentID']

        TEXT = 'Reply By CnC1 from Jive'
#
        jiveHelper.messageOnDiscussion(account["User1"], contentID,
"<body><h1>Success !</h1><p>%s</p></body>" % (TEXT))

        sleep(180)

        User1RecievedMail = CheckEmailHelper.findEmailListBySubject(account["User1"], subject, to=group['groupKey'])[-1]
        User2RecievedMail = CheckEmailHelper.findEmailListBySubject(account["User2"], subject, to=group['groupKey'])[-1]
        User4RecievedMail = CheckEmailHelper.findEmailListBySubject(account["User4"], subject, to=group['groupKey'])[-1]
        User5RecievedMail = CheckEmailHelper.findEmailListBySubject(account["User5"], subject, to=group['groupKey'])[-1]

        textMail1 = User1RecievedMail.get_payload()
        textMail2 = User2RecievedMail.get_payload()
        textMail4 = User4RecievedMail.get_payload()
        textMail5 = User5RecievedMail.get_payload()

        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail1))
        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail2))
        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail4))
        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail5))

    def test_ShouldSyncCommentFromJive(self):
        # subject = 'Discussion from Jive 2.23'
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()

        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text = """
<div>
    <h1>Origin Discussion created By User2 from Jive</h1>
    <p>Some interesting text to discuss</p>
</div>
"""
        )
        self.assertEqual(content['subject'], subject, 'Subject not Matched')

        sleep(60)

        topicEmails = CheckEmailHelper.findEmailListBySubject(account["User4"], subject, to=group['groupKey'])

        original = topicEmails[0]

        TEXT = "reply from User 4 on time: " + datetime.datetime.now().isoformat()
        HTML = "<div> %s </div>" % (TEXT)

        ReplyEmail(Subject=subject,
                  From=account["User4"],
                  To=[group['groupKey']],
                  ReplyTo=[group['groupKey']],
                  HTML=HTML,
                  Origin=original
                  )

        sleep(30)

        # check other group members can recieve email reply

        User1RecievedMail = CheckEmailHelper.findEmailListBySubject(account["User1"], subject, to=group['groupKey'])[-1]
        User2RecievedMail = CheckEmailHelper.findEmailListBySubject(account["User2"], subject, to=group['groupKey'])[-1]
        User5RecievedMail = CheckEmailHelper.findEmailListBySubject(account["User5"], subject, to=group['groupKey'])[-1]

        textMail1 = User1RecievedMail.get_payload()[0].get_payload()
        textMail2 = User2RecievedMail.get_payload()[0].get_payload()
        textMail5 = User5RecievedMail.get_payload()[0].get_payload()

        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail1))
        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail2))
        self.assertIsNotNone(re.search(r'%s' % TEXT, textMail5))

        # check comment replyed on Jive

        sleep(180)

        discussion = jiveHelper.findDisussionBySubject(subject)
        self.assertIsNotNone(re.search(r'%s' % TEXT, discussion[0]['content']['text']))


    def test_shouldSyncSpecialCharsFromJive(self):
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()
        POST_TEXT = "Sample discuss 这是一个有趣的讨论 非常---有趣&nbsp;&nbsp;do you like it ?"
        POST_CONTENT = "<div> %s </div>" % (POST_TEXT)

        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text = POST_CONTENT
        )
        self.assertEqual(content['subject'], subject, 'Subject not Matched')

        sleep(120)

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


    def test_shouldUnsplitOnJiveWhenCommentCountIsMoreThan100(self):
        # subject = 'SO Test Discussion 2016-11-21T11:41:41.284753'
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()
        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text="""
        <div>
            <h1>Origin Discussion created By User2 from Jive</h1>
            <p>For Comment from Jive Testing</p>
        </div>
        """
        )
        self.assertEqual(content['subject'], subject, 'Subject not Matched')

        # contentID = content["discussion"].split('/')[-1]
        contentID = content['contentID']

        for idx in range(102):
            REPLAY_TEXT = 'Reply By CnC4 from Jive' + str(idx)
            #
            jiveHelper.messageOnDiscussion(account["User4"], contentID,
                                           "<body><h1>Success !</h1><p>%s</p></body>" % (REPLAY_TEXT))


        originCommentsCount = len(jiveHelper.findAllCommentsByContentID(contentID))

        sleep(180)

        topicEmails = CheckEmailHelper.findEmailListBySubject(account["User2"], subject,
                                                              to=group['groupKey'])

        original = topicEmails[0]

        TEXT = "reply the long thread from User 2 on time: " + datetime.datetime.now().isoformat()
        HTML = "<div> %s </div>" % (TEXT)

        ReplyEmail(Subject=subject,
                   From=account["User2"],
                   To=[group['groupKey']],
                   ReplyTo=[group['groupKey']],
                   HTML=HTML,
                   Origin=original
                   )

        sleep(180)

        allComments = jiveHelper.findAllCommentsByContentID(contentID)

        self.assertIsNotNone(re.search(r'%s' % TEXT, allComments[-1]['content']['text']))
        self.assertEqual(len(allComments), originCommentsCount+1)