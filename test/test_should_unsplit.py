import datetime
from time import sleep
import unittest
import re
from test.config import group, account
from test.helper.jiveHelper import jiveHelper
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper.sendMailHelper import ReplyEmail


class UnsplitTest(unittest.TestCase):
    def test_shouldUnsplitOnJiveWhenCommentCountIsMoreThan100(self):
        # subject = 'SO Test Discussion 2016-11-21T11:41:41.284753'
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()
        content = jiveHelper.createContent(
            groupName=group['groupName'],
            user=account["User2"],
            title=subject,
            text="""t
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