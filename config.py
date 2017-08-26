import json

with open('env.json') as json_data:
    env = json.load(json_data)

with open('accounts.json') as json_data:
    account = json.load(json_data)

group = {}
group['groupName'] = 'taohui-automation'
group['groupKey'] = group['groupName'] + '@' + env['google']['domainName']
group['groupAdmin'] = account["User1"]
group['members'] = [account["User2"], account["User5"]]