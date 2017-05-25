from imapclient import IMAPClient
import email
import os, json
import pdb

# IMAPClient uses IMAPlib module, which is used for mail

HOST = 'imap.gmail.com'

directory ="/Users/wxji/Documents/Connect/streamonce-integration-python"
with open(directory + '/env.json') as json_data:  # os.getcwd() Return the current working directory
    env = json.load(json_data)

with open(directory + '/accounts.json') as json_data:
    account = json.load(json_data)

class CheckEmailHelper():
    @staticmethod
    def findEmailBySubject(user=account["jiveAdmin"], subject="Welcome", to=""):
        server = IMAPClient(HOST, use_uid=True, ssl=True, port=993)

        print("Checking Mail of User: %s, Subject: %s" % (user["username"], subject))

        server.login(user["email"], user["googlePassword"])
        select_info = server.select_folder('INBOX')

        ans = server.gmail_search('to:(%s) subject:(%s)' % (to, subject))

        if len(ans) == 1:
            resp = server.fetch(ans, ['body[]'])
            msg = email.message_from_bytes(resp[ans[0]][b'BODY[]'])  #return a message object structure
            server.shutdown()
            return msg
        elif len(ans) == 0:
            server.shutdown()
            return None
        else:
            server.shutdown()
            raise Exception("Got Multiple Email with this subject %s %s" % (user["username"], subject))

    @staticmethod
    def findEmailListBySubject(user=account["jiveAdmin"], subject="Welcome", to=""):
        server = IMAPClient(HOST, use_uid=True, ssl=True, port=993)

        print("Checking Mail of User: %s, Subject: %s" % (user["username"], subject))

        server.login(user["email"], user["googlePassword"])
        select_info = server.select_folder('INBOX')

        ans = server.gmail_search('to:(%s) subject:(%s)' % (to, subject))

        if len(ans) == 0:
            server.shutdown()
            return None
        else:
            resp = server.fetch(ans, ['body[]', 'bodystructure'])
            messages = []
            for uid in ans:
                messages.append(email.message_from_bytes(resp[uid][b'BODY[]']))

            server.shutdown()
            return messages

    @staticmethod
    def deleteEmails(user=account["jiveAdmin"], to=""):
        server = IMAPClient(HOST, use_uid=True, ssl=True, port=993)

        print("Checking Mail of User: %s " % user["username"])

        server.login(user["email"], user["googlePassword"])

        server.select_folder('INBOX')
        inbox_mails = server.gmail_search('in:inbox %s' % (to))
        server.delete_messages(inbox_mails)

        server.select_folder('[Gmail]/Sent Mail')
        send_mails = server.gmail_search('is:sent %s' % (to))
        server.delete_messages(send_mails)

        server.shutdown()

if __name__ == "__main__":
    subject = 'Begin test here'
    Mails = CheckEmailHelper.findEmailListBySubject(account['User1'], subject, to='one-plus@' + env["google"]["domainName"])
    print(Mails)

