from config import group
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper.googleHelper import GoogleHelper
from test.helper.jiveHelper import jiveHelper
from test.helper.userHelper import UserHelper

def createEmailTestGroup():
    print('create email test group', group['groupName'])
    UserHelper.startDriver()
    UserHelper.login(group['groupAdmin'])
    UserHelper.createGroup(group['groupName'])
    UserHelper.addMembersToGroup(group['groupName'], group['members'])
    UserHelper.stopDriver()

def deleteEmailTestGroup():
    jiveGroup = jiveHelper.getGroupByName(group['groupName'])

    if jiveGroup is not None:
        print('found jive group to delete')
        jiveHelper.deleteGroupByPlaceID(jiveGroup["placeID"])
    else:
        print('cannot find jive group to delete')

    GoogleHelper.deleteGroup(group['groupKey'])

    print('delete email test group', group['groupName'])
    # delete user emails
    CheckEmailHelper.deleteEmails(group['groupAdmin'], to=group['groupKey'])

    for member in group['members']:
        CheckEmailHelper.deleteEmails(member, to=group['groupName'])
    print('delete all test emails', group['groupName'])
