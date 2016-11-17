import requests
from requests.auth import HTTPBasicAuth
import os
import json
import time
import pdb

with open(os.getcwd() + '/env.json') as json_data:
    env = json.load(json_data)
    apiUrl = env["jive"]["apiBaseUrl"]


with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)

BasicAuth=HTTPBasicAuth(account["jiveAdmin"]["username"], account["jiveAdmin"]["password"])

class jiveHelper:
    @staticmethod
    def getGroupByName(groupName):
        url = env["jive"]["apiBaseUrl"] + '/search/places?filter=search({0})&filter=nameonly'.format(groupName)
        r = requests.get(url, auth=BasicAuth)
        assert r.status_code == 200, "could not find group"

        if len(r.json()["list"]) != 1:
            print ("group %s not found or found more than one : %d" % (groupName, len(r.json()["list"])))
            return None

        placeID = r.json()["list"][0]["placeID"]
        url = env["jive"]["apiBaseUrl"] + '/places/{0}'.format(placeID)
        r = requests.get(url, auth=BasicAuth)
        assert r.status_code == 200, "get group failed with code %d" % (r.status_code)
        assert r.json()["name"] == groupName
        return r.json()

    @staticmethod
    def deleteGroupByPlaceID(placeID):
        url = env["jive"]["apiBaseUrl"] + '/places/{0}'.format(placeID)
        r = requests.delete(url, auth=BasicAuth)
        assert r.status_code == 204, "delete group failed with code %d" % (r.status_code)

    @staticmethod
    def createGroup(groupName):
        url = apiUrl + '/places/'
        body = {
            "type": "group",
            "displayName": groupName,
            "name": groupName,
            "groupType": "PRIVATE"
        }
        r = requests.post(url, json=body, auth=BasicAuth)
        print(json.dumps(body), r.status_code)
        assert r.status_code == 201, "create group failed with code %d" % (r.status_code)
        return r.json()

    @staticmethod
    def createContent(
            groupName="",
            user=account["jiveAdmin"],
            title="Sample Content for SO Test",
            contentType="discussion",
            text="""
<div>
    <h1>hello discuss</h1>
    <p>Some interesting text to discuss</p>
</div>
            """):
        place = jiveHelper.getGroupByName(groupName)
        url = apiUrl + '/places/' + place["placeID"] + "/contents"

        headers = {
            "Content-Type": "application/json",
            "X-Jive-Run-As": "userid " + str(user["id"])
        }

        body = {
            "type" : contentType,
            "status" : "published",
            "subject" : title,
            "content" : {
              "type" : "text/html",
              "text" : text
            }
        }

        r = requests.post(url, headers=headers, json=body, auth=BasicAuth)
        assert r.status_code == 201
        content = r.json()
        assert title == content['subject'], "Title Created not match"
        assert user['displayName'] == content['author']['displayName'], "User Created not match"

        return content

    @staticmethod
    def getGroupContents(groupName):
        place = jiveHelper.getGroupByName(groupName)
        url = apiUrl + '/places/%s/contents' % place["placeID"]
        r = requests.get(url, auth=BasicAuth)
        assert r.status_code == 200
        print(r.json())
        contents = r.json()['list']
        return r.json()

if __name__ == "__main__":
    groupName = 'streamonceintegrationtest4'
    place = jiveHelper.createGroup(groupName)
    time.sleep(60)
    place = jiveHelper.getGroupByName(groupName)
    jiveHelper.deleteGroupByPlaceID(place["placeID"])
    print(jiveHelper.createContent(groupName="streamonceintegrationtest4", user=account['User2'], title='SP 1'))
    r = jiveHelper.getGroupContents(groupName)