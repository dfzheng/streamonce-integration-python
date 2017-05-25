import sys
sys.path.insert(0,'..')
import os
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import pdb

directory ="/Users/wxji/Documents/Connect/streamonce-integration-python"
with open(directory + '/env.json') as json_data:
    env = json.load(json_data)
    apiUrl = env["jive"]["apiBaseUrl"]


with open(directory + '/accounts.json') as json_data:
    account = json.load(json_data)

BasicAuth=HTTPBasicAuth(account["jiveAdmin"]["username"], account["jiveAdmin"]["password"])

class jiveHelper():
    @staticmethod
    def isOnlyResult(response):
        if len(response.json()["list"]) != 1:
            return False
        else :
            return True

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
        assert r.json()["name"].lower() == groupName
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
            """,
            attachments=[]):
        place = jiveHelper.getGroupByName(groupName)
        url = apiUrl + '/places/' + place["placeID"] + "/contents"

        headers = {
            "Content-Type": "application/json",
            # "X-Jive-Run-As": "userid " + str(user["id"])
            "X-Jive-Run-As": "email " + user["email"]
        }

        body = {
            "type" : contentType,
            "status" : "published",
            "subject" : title,
            "content" : {
              "type" : "text/html",
              "text" : text
            },
            "attachments": attachments
        }

        print("placeID:", place["placeID"], ",userID:", user["id"], ",admin:", account["jiveAdmin"]["username"])

        r = requests.post(url, headers=headers, json=body, auth=BasicAuth)
        assert r.status_code == 201, "result code is %s" % str(r.status_code)
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

    @staticmethod
    def findContentBySubject(contentSubject):
        url = apiUrl + "/search/contents?filter=search('%s')&filter=subjectonly(true)" % (contentSubject)
        r = requests.get(url, auth=BasicAuth)
        assert r.status_code == 200, "responsed code {0}".format(r.status_code)
        if not jiveHelper.isOnlyResult(r):
            print('findContentBySubject has no result or more than one')
            return None
        return r.json()['list'][0]


    @staticmethod
    def getReplybySubject(user=account["jiveAdmin"], contentSubject=""):
        url = apiUrl + "/search/contents?filter=search('%s')&filter=subjectonly(true)" % (contentSubject)
        r = requests.get(url, auth=BasicAuth)
        assert r.status_code == 200
        if not isOnlyResult(r):
           print('findContentBySubject has no result or more than one')
        commentHTML = r.json()['list'][1]['content']['text']
        comment = BeautifulSoup(commentHTML, 'html.parser').get_text()
        print (comment)
        return comment

    # content can only find by non-federated user, not normal account, so remove this function
    # @staticmethod
    # def findContentAsUserBySubject(user=account["jiveAdmin"], contentSubject=""):
    #     url = apiUrl + "/search/contents?filter=search('%s')&filter=subjectonly(true)" % (contentSubject)
    #     BasicAuth=HTTPBasicAuth(user["username"], user["password"])
    #     r = requests.get(url, auth=BasicAuth)
    #     assert r.status_code == 200
    #     if not jiveHelper.isOnlyResult(r):
    #         print('findContentBySubject has no result or more than one')
    #         return None
    #     return r.json()['list'][0]

    @staticmethod
    def findDisussionBySubject(contentSubject):
        url = apiUrl + "/search/contents?filter=search('%s')&filter=subjectonly(true)" % (contentSubject)
        r = requests.get(url, auth=BasicAuth)
        assert r.status_code == 200
        return r.json()['list']

    @staticmethod
    def findAllCommentsByContentID(contentID):
        url = apiUrl + "/messages/contents/%s" % (contentID)
        allComments = []

        while (url != None):
            resp = requests.get(url, auth=BasicAuth)
            assert resp.status_code == 200
            comments = resp.json()
            allComments.extend(comments['list'])

            if 'links' in comments and 'next' in comments['links']:
                url = comments['links']['next']
            else:
                url = None

        return sorted(allComments, key=lambda k: k['published'])


    @staticmethod
    def messageOnDiscussion(user, contentID, reply, attachments=[]):
        body = {
            "content": {"type": "text/html", "text": reply},
            "type": "message",
            "attachments": attachments
        }

        url = apiUrl + "/messages/contents/" + contentID

        headers = {
            "Content-Type": "application/json",
            # "X-Jive-Run-As": "userid " + str(user["id"]),
            "X-Jive-Run-As": "email " + user["email"],
        }

        print(url)

        r = requests.post(url, headers=headers, json=body, auth=BasicAuth)
        assert r.status_code == 201, str(r.status_code)

        return r.json()

if __name__ == "__main__":
    groupName = 'streamonceintegrationtest4'
    place = jiveHelper.createGroup(groupName)
    time.sleep(60)
    place = jiveHelper.getGroupByName(groupName)
    jiveHelper.deleteGroupByPlaceID(place["placeID"])
    print(jiveHelper.createContent(groupName="streamonceintegrationtest4", user=account['User2'], title='SP 1'))
    r = jiveHelper.getGroupContents(groupName)

    r = jiveHelper.findContentBySubject("SO Test Discussion 1.41")
    contentID = r["discussion"].split('/')[-1]
    contentID = "2029"
    comment = jiveHelper.messageOnDiscussion(account["User1"], contentID, """
<body><p>comment</p></body>
""")
    print(comment)
