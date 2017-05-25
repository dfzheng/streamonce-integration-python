import sys
sys.path.insert(0,'..')
from time import sleep
from test.helper.jiveHelper import jiveHelper
from test.helper import sendMailHelper
from test.helper import config
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper import sendMailHelper
import unittest
import datetime
import pdb



class EmailwithAttachment(unittest.TestCase):

    testSubject = "Discussion and reply with attachment by Email" + datetime.datetime.now().isoformat()
    print ("0")
    #Send an Email with attachment test
    def test_shouldHaveNotificationOnJiveWithAttachment(self):
        print ("1")
        directory ="/Users/wxji/Documents/Connect/streamonce-integration-python"
        attachmentName = "attachmentDiscussion.jpg"
        attachments = [{
            "doUpload": True,
            "name": attachmentName,
            "path": directory+"/test/asserts/thumb.jpg"
            # "url": "http://pics.sc.chinaz.com/files/pic/pic9/201508/apic14052.jpg"
        }]

        preamble = "Should had an Attachment with Email(discussion)";
        text = '''
          After a growth interval, the polyp begins reproducing asexually by budding and, in the Scyphozoa, is called a segmenting polyp,
        or a scyphistoma. Budding produces more scyphistomae and also ephyrae. Budding sites vary by species; from the tentacle bulbs,
        the manubrium (above the mouth), or the gonads of hydromedusae.[51] Polyps asexually produce free-swimming ephyra,
        which then become a medusa. New specimens (usually only a millimeter or two across) swim away from the polyp and then grow.
        Some polyps can asexually produce a creeping frustule larval form, which then develops into another polyp.
        '''

        html="""
<html>
<body>
<div>
<p>

</p>
</div>
</body></html>"""
        print("2")
        account = config.account
        group = config.group

        #Send discussion in Email as User1
        sendMailHelper.SendEmail(Subject=EmailwithAttachment.testSubject, From=account["User1"], To=group['groupKey'], Preamble=preamble, Attachment=attachments, TEXT=text, HTML=html, ReplyTo=[], useAlias=False);
        print("sleep 90 sec, please wait...")
        sleep(90);

        #Check on Jive with subject & attachment
        jivecheck = jiveHelper.findContentBySubject(contentSubject=EmailwithAttachment.testSubject)
        print ("4")

        #start to debug
        # pdb.set_trace()
        #check subject and attachment are correct
        self.assertEqual(jivecheck['subject'],EmailwithAttachment.testSubject)
        print("5")
        print( jivecheck )
        # self.assertEqual(jivecheck.get_payload()[0]["Content-Disposition"], 'attachment; filename='+attachmentName)
        print("6")

    # reply with attachment test
    def test_shouldSyncCommentToJiveWithAttachment(self):

        account = config.account
        group = config.group
        directory ="/Users/wxji/Documents/Connect/streamonce-integration-python"
        ImageName = "thumb.jpg"
        images = [{
            "doUpload": True,
            "name": ImageName,
            "path": directory+"/test/asserts/thumb.jpg"
        }]
        html="""
             <html>
             <body>
             <div>
             <p>reply as tester1</p>
             </div>
             </body></html>"""
        Origin = CheckEmailHelper.findEmailBySubject(account["User1"],EmailwithAttachment.testSubject, group['groupKey'])

        #reply as User1, ReplySubject is subject of reply
        ReplySubject = sendMailHelper.ReplyEmailwithImage(Subject=EmailwithAttachment.testSubject, From=account["User2"], To=account["User1"], Cc=group['groupKey'], TEXT="", HTML=html, Images=images, Origin=None, useAlias=False)
        print("sleep 90 sec, please wait...")
        sleep(90);

        msg1 = jiveHelper.findContentBySubject(user=account["jiveAdmin"], subject=ReplySubject)

        if (msg1 != None)  :
              print ("Successful: reply email with image attachment received in Email!!!!!")
        else:
              print ("Failed: jive not receive reply email with image attachment!!!")

        # rep1 = jiveHelper.getReplybySubject(user=account["User1"], subject=EmailwithAttachment.testSubject)
        rep1 = jiveHelper.getReplybySubject(user=account["User1"], subject=ReplySubject)
        self.assertEqual(rep1,'reply as tester1')

        print("reply success!!!")


unittest.main()