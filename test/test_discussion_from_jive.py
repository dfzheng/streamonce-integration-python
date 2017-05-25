import sys
sys.path.insert(0,'..')
import datetime
from time import sleep
import unittest
import pdb
from helper.jiveHelper import jiveHelper
from helper.CheckEmailHelper import CheckEmailHelper
from helper.config import env, account, group
import json

class DiscussionFromJive(unittest.TestCase):

    #     self.test_shouldHaveEmailNotification()
    def test_shouldHaveEmailNotification(self):
        testSubject = "Normal discussion on jive AUTO " + datetime.datetime.now().isoformat()

        TEXT = '''
    <div>
       <h1>Sample discuss</h1>

       <p> After a growth interval, the polyp begins reproducing asexually by budding and, in the Scyphozoa, is called a segmenting polyp,
        or a scyphistoma. Budding produces more scyphistomae and also ephyrae. Budding sites vary by species; from the tentacle bulbs,
        the manubrium (above the mouth), or the gonads of hydromedusae.[51] Polyps asexually produce free-swimming ephyra,
        which then become a medusa. New specimens (usually only a millimeter or two across) swim away from the polyp and then grow.
        Some polyps can asexually produce a creeping frustule larval form, which then develops into another polyp.</p>

    </div>
        '''

        content = jiveHelper.createContent(groupName=group['groupName'], user=account['User2'], title= testSubject, contentType="discussion", text=TEXT, attachments=[])

        self.assertEqual(content['subject'], testSubject, 'Subject not Matched...')
        print ('sleep 60 seconds, please wait...')
        sleep(60)
        print ('Begin to check Email of group members...')
        Mail1 = CheckEmailHelper.findEmailBySubject(account["User1"], testSubject, to=group['groupKey'])
        Mail2 = CheckEmailHelper.findEmailBySubject(account["User2"], testSubject, to=group['groupKey'])
        Mail5 = CheckEmailHelper.findEmailBySubject(account["User5"], testSubject, to=group['groupKey'])
        print ("Check Email subject...")
        self.assertEqual(Mail1['Subject'], testSubject)
        self.assertEqual(Mail2['Subject'], testSubject)
        self.assertEqual(Mail5['Subject'], testSubject)
        print ('The end, successful!!!')

if __name__ == '__main__':
    unittest.main()
