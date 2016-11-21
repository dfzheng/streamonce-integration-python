import unittest
from test.helper.googleHelper import GoogleHelper
from test.helper.jiveHelper import jiveHelper
from test.test_email_notification import EmailNotificationTest
from test.config import group
from test.helper.userHelper import UserHelper


def createEmailTestGroup():
    print('create email test group', group['groupName'])
    UserHelper.startDriver()
    UserHelper.login(group['groupAdmin'])
    UserHelper.createGroup(group['groupName'])
    UserHelper.addMembersToGroup(group['groupName'], group['members'])
    UserHelper.stopDriver()

def deleteEmailTestGroup():
    print('delete email test group', group['groupName'])

    jiveGroup = jiveHelper.getGroupByName(group['groupName'])

    if jiveGroup != None:
        jiveHelper.deleteGroupByPlaceID(jiveGroup["placeID"])

    GoogleHelper.deleteGroup(group['groupKey'])

if __name__ == "__main__":
    suite = unittest.TestSuite()

    createEmailTestGroup()

    suite.addTest(EmailNotificationTest())

    try:
        unittest.main()
    except:
        print('finished')

    deleteEmailTestGroup()