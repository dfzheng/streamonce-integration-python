import os,sys
import json

directory ="/Users/wxji/Documents/Connect/streamonce-integration-python"
with open(directory + '/env.json') as json_data:  # os.getcwd() Return the current working directory
    env = json.load(json_data)

with open(directory + '/accounts.json') as json_data:
    account = json.load(json_data)

group = {}
group['groupName'] = 'streamonce-sissy-test'
group['groupKey'] = group['groupName'] + '@' + env['google']['domainName']
group['groupAdmin'] = account["User1"]
group['members'] = [account["User1"], account["User2"], account["User5"]]