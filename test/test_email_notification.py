from test.helper.userHelper import UserHelper
from test.helper.jiveHelper import jiveHelper
from test.helper.googleHelper import GoogleHelper
from test.helper.CheckEmailHelper import CheckEmailHelper
import datetime
from time import sleep
from test.config import env, account
import unittest
import pdb

class EmailNotificationTest(unittest.TestCase):

    groupName = 'streamonceintegrationtest4'
    groupKey = groupName + '@' + env['google']['domainName']
    groupAdmin = account["User1"]
    members = [account["User2"], account["User4"], account["User5"]]

    @classmethod
    def setUpClass(cls):
        print("beforeAll")
        UserHelper.startDriver()
        UserHelper.login(cls.groupAdmin)
        UserHelper.createGroup(cls.groupName)
        UserHelper.addMembersToGroup(cls.groupName, cls.members)

    @classmethod
    def tearDownClass(cls):
        print("afterAll")
        UserHelper.stopDriver()
        jiveGroup = jiveHelper.getGroupByName(cls.groupName)

        if jiveGroup != None:
            jiveHelper.deleteGroupByPlaceID(jiveGroup["placeID"])

        GoogleHelper.deleteGroup(cls.groupKey)

    def test_shouldHaveEmailNotification(self):
        subject = 'SO Test Discussion ' + datetime.datetime.now().isoformat()
        # subject = 'SO Test Discussion 884434419'
        content = jiveHelper.createContent(
            groupName=EmailNotificationTest.groupName,
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

        Mail1 = CheckEmailHelper.findEmailBySubject(account["User1"], subject, to=EmailNotificationTest.groupKey)
        Mail2 = CheckEmailHelper.findEmailBySubject(account["User2"], subject, to=EmailNotificationTest.groupKey)
        Mail4 = CheckEmailHelper.findEmailBySubject(account["User4"], subject, to=EmailNotificationTest.groupKey)
        Mail5 = CheckEmailHelper.findEmailBySubject(account["User5"], subject, to=EmailNotificationTest.groupKey)

        self.assertEqual(Mail1['Subject'], subject)
        self.assertEqual(Mail2['Subject'], subject)
        self.assertEqual(Mail4['Subject'], subject)
        self.assertEqual(Mail5['Subject'], subject)

