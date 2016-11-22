import os, json

with open(os.getcwd() + '/env.json') as json_data:
    env = json.load(json_data)

with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)

group = {}

group['groupName'] = 'streamonceintegrationtest1234'
group['groupKey'] = group['groupName'] + '@' + env['google']['domainName']
group['groupAdmin'] = account["User1"]
group['members'] = [account["User2"], account["User4"], account["User5"]]
