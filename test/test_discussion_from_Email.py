import sys
sys.path.insert(0,'..')
from time import sleep
from test.helper.jiveHelper import jiveHelper
from test.helper import config
from test.helper import CheckEmailHelper
from test.helper import sendMailHelper
import unittest
import datetime
import pdb



class DiscussionFromEmail(unittest.TestCase):

    #Send an Email test
    def test_shouldHaveNotificationOnJive(self):

        testsubject = "Normal discussion by Email AUTO " + datetime.datetime.now().isoformat()
        preamble = "Should had anEmail(discussion)";
        text = '''
    <div>
       <h1>Sample discuss</h1>

       <p> After a growth interval, the polyp begins reproducing asexually by budding and, in the Scyphozoa, is called a segmenting polyp,
        or a scyphistoma. Budding produces more scyphistomae and also ephyrae. Budding sites vary by species; from the tentacle bulbs,
        the manubrium (above the mouth), or the gonads of hydromedusae.[51] Polyps asexually produce free-swimming ephyra,
        which then become a medusa. New specimens (usually only a millimeter or two across) swim away from the polyp and then grow.
        Some polyps can asexually produce a creeping frustule larval form, which then develops into another polyp.</p>

    </div>
        '''

        html="""
<html>
<body>
<div>
<p>

</p>
</div>
</body></html>"""

        account = config.account
        group = config.group
        #Send discussion in Email as User1
        sendMailHelper.SendEmail(Subject=testsubject, From=account["User1"], To=group['groupKey'], Preamble=preamble, TEXT=text, HTML=html, ReplyTo=[], useAlias=False);

        print ("Sleep 90 seconds, please wait for sync...")
        sleep(90);
        #Check on Jive with subject
        print ("Checking content on jive...")
        jive1 = jiveHelper.findContentBySubject(contentSubject=testsubject)

        if jive1 == None :
            print ("TestCaseFailed: NO discussion notification on jive...")
        else:

            #start to debug
            # pdb.set_trace()

            self.assertEqual(jive1['subject'],testsubject)
            print("Successfull~~~ !!!")


if __name__ == '__main__':
    unittest.main()