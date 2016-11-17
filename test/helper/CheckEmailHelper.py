from imapclient import IMAPClient
import email
import os, json
import pdb

HOST = 'imap.gmail.com'

with open(os.getcwd() + '/env.json') as json_data:
    env = json.load(json_data)

with open(os.getcwd() + '/accounts.json') as json_data:
    account = json.load(json_data)

class CheckEmailHelper():
    @staticmethod
    def findEmailBySubject(user=account["jiveAdmin"], subject="Welcome", to=""):
        server = IMAPClient(HOST, use_uid=True, ssl=True, port=993)

        print("Checking Mail of User: %s, Subject: %s" % (user["username"], subject))

        server.login(user["email"], user["password"])
        select_info = server.select_folder('INBOX')

        ans = server.gmail_search('to:(%s) subject:(%s)' % (to, subject))

        if len(ans) == 1:
            resp = server.fetch(ans, ['body[]'])
            msg = email.message_from_bytes(resp[ans[0]][b'BODY[]'])
            server.shutdown()
            return msg
        elif len(ans) == 0:
            server.shutdown()
            return None
        else:
            server.shutdown()
            raise Exception("Got Multiple Email with this subject %s %s" % (user["username"], subject))


if __name__ == "__main__":
    subject = 'SO Test Discussion 884434419'
    Mail = CheckEmailHelper.findEmailBySubject(account['User2'], subject, to='streamonceintegrationtest4' + env["google"]["domainName"])
    print(Mail)

