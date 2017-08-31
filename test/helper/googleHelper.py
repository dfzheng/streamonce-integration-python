from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from apiclient.discovery import build
import os, pdb, json
import time
import googleapiclient
import sys
import base64
sys.path.insert(0,'../..')

with open('env.json') as json_data:
    env = json.load(json_data)

with open('accounts.json') as json_data:
    account = json.load(json_data)

#credentials = ServiceAccountCredentials.from_json_keyfile_name(env["googleAuthData"]["keyFile"], env["googleAuthData"]["scopes"])

google_private_key = os.getenv('GOOGLE_PRIVATE_KEY_ENCODED')
decoded_google_private_key = google_private_key.decode('base64')

oauth_fields = {
    "type": "service_account",
    "project_id": "streamonce-testing",
    "private_key": decoded_google_private_key,
    "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID'),
    "client_email": "streamonce-testing@appspot.gserviceaccount.com",
    "client_id": "107495441022329297030",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/streamonce-testing%40appspot.gserviceaccount.com"
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(oauth_fields, scopes=env["googleAuthData"]["scopes"])

delegated_credentials = credentials.create_delegated(env["googleAuthData"]["delegate_user"])

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
    groupKey = "test-on-1221" + '@' + env["google"]["domainName"]
    memberKey = account["jiveAdmin"]["username"]

    memberKey = "cnctester5@dev.thoughtworks.com"

    # print(GoogleHelper.createGroup(groupKey))

    # print(GoogleHelper.getGroup(groupKey))

    print(GoogleHelper.insertMember(groupKey, memberKey))
    #
    print(GoogleHelper.getMemebers(groupKey))
    #
    # print(GoogleHelper.deleteMember(groupKey, memberKey))
    #
    # time.sleep(5)
    #
    # print(GoogleHelper.getMemebers(groupKey))
    #
    # print(GoogleHelper.deleteGroup(groupKey))
