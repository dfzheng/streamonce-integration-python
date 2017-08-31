import json
import os

with open('env.json') as json_data:
    env = json.load(json_data)

with open('accounts.json') as json_data:
    account = json.load(json_data)

account["User1"]["username"] = os.environ.get("USER1_USERNAME")
account["User1"]["password"] = os.environ.get("USER1_PASSWORD")
account["User2"]["username"] = os.environ.get("USER2_USERNAME")
account["User2"]["password"] = os.environ.get("USER2_PASSWORD")
account["User3"]["username"] = os.environ.get("USER3_USERNAME")
account["User3"]["password"] = os.environ.get("USER3_PASSWORD")
account["User4"]["username"] = os.environ.get("USER4_USERNAME")
account["User4"]["password"] = os.environ.get("USER4_PASSWORD")
account["User5"]["username"] = os.environ.get("USER5_USERNAME")
account["User5"]["password"] = os.environ.get("USER5_PASSWORD")
account["jiveAdmin"]["username"] = os.environ.get("JIVE_ADMIN_USERNAME")
account["jiveAdmin"]["password"] = os.environ.get("JIVE_ADMIN_PASSWORD")
account["GoogleAdmin"]["username"] = os.environ.get("GOOGLE_ADMIN_USERNAME")
account["GoogleAdmin"]["password"] = os.environ.get("GOOGLE_ADMIN_PASSWORD")
account["User1"]["twoStep"] = os.environ.get("SECURITY_ANSWER")
account["User2"]["twoStep"] = os.environ.get("SECURITY_ANSWER")
account["User3"]["twoStep"] = os.environ.get("SECURITY_ANSWER")
account["User4"]["twoStep"] = os.environ.get("SECURITY_ANSWER")
account["User5"]["twoStep"] = os.environ.get("SECURITY_ANSWER")







group = {}
group['groupName'] = 'dafu-automation'
group['groupKey'] = group['groupName'] + '@' + env['google']['domainName']
group['groupAdmin'] = account["User1"]
group['members'] = [account["User2"], account["User5"]]

