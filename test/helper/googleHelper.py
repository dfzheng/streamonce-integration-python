from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
import os, pdb, json
import time
import googleapiclient

with open(os.getcwd() + '/env.json') as json_data:
    env = json.load(json_data)

with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)

credentials = ServiceAccountCredentials.from_json_keyfile_name(env["google"]["keyFile"], env["google"]["scopes"])

delegated_credentials = credentials.create_delegated(env["google"]["delegate_user"])

http_auth = delegated_credentials.authorize(Http())

admin = build('admin','directory_v1', http=http_auth)

class GoogleHelper():
    @staticmethod
    def getGroup(groupName):
        return admin.groups().get(groupKey=groupName).execute()

    @staticmethod
    def deleteGroup(groupName):
        try:
            admin.groups().delete(groupKey=groupName).execute()
        except googleapiclient.errors.HttpError as err:
            print(err)

    @staticmethod
    def getMemebers(groupName):
        return admin.members().list(groupKey=groupName).execute()

    @staticmethod
    def deleteMember(groupKey, memberKey):
        return admin.members().delete(groupKey=groupKey, memberKey=memberKey).execute()

    @staticmethod
    def insertMember(groupName, userEmail):
        resp = admin.members().insert(groupKey=groupName, body={
            'email': userEmail,
            'role': 'MEMBER'
        }).execute()
        time.sleep(5)
        return resp

    @staticmethod
    def createGroup(groupName, description='', name=''):
        if name == '':
            name = groupName
        if description == '':
            description = name

        resp = admin.groups().insert(
            body = {
                'email' : groupName,
                'description': description,
                'name': name
            }
        ).execute()
        time.sleep(5)
        return resp

if __name__ == "__main__":
    groupKey = "streamonceintegrationtest4" + '@' + env["google"]["domainName"]
    memberKey = account["User2"]["email"]

    print(GoogleHelper.createGroup(groupKey))

    print(GoogleHelper.getGroup(groupKey))

    print(GoogleHelper.insertMember(groupKey, memberKey))

    print(GoogleHelper.getMemebers(groupKey))

    print(GoogleHelper.deleteMember(groupKey, memberKey))

    time.sleep(5)

    print(GoogleHelper.getMemebers(groupKey))

    print(GoogleHelper.deleteGroup(groupKey))
