from imapclient import IMAPClient
import email
import os, json

with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)

HOST = 'imap.gmail.com'
USERNAME = account["User2"]["email"]
PASSWORD = account["User2"]["password"]

server = IMAPClient(HOST, use_uid=True, ssl=True, port=993)
server.login(USERNAME,PASSWORD)

select_info = server.select_folder('INBOX')
print('%d messages in INBOX' % select_info[b'EXISTS'])

messages = server.search(['NOT', 'DELETED'])
print('%d messages that not SEEN' % len(messages))
print(messages)

response = server.fetch(messages[-1:], ['FLAGS', 'body[]'])

bstring = response[messages[-1]][b'BODY[]']

print(bstring)

msg = email.message_from_bytes(bstring)

print(msg['To'])
# https://docs.python.org/3/library/email.message.html#email.message.Message
# msg.get_payload()[3].get_payload()
