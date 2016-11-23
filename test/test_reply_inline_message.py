import datetime
import pdb
import re
from test.helper.CheckEmailHelper import CheckEmailHelper
from test.helper.jiveHelper import jiveHelper
from test.config import group, account
from test.helper.sendMailHelper import ReplyEmail
import time

replyTEXTTemplate = """Reply at Beginning

On {timestamp}, {authorName} <
{googleAdminEmail}> wrote:

> *Star Trek:* First Contact is a 1996 American science fiction film
> released by Paramount Pictures. It is the eighth feature film in the Star
> Trek film franchise, and the second film in the series to star the cast of
> the television series Star Trek: The Next Generation. In the film's plot,
> the crew of the Starship USS Enterprise-E travel back in time to the
> mid-21st century to stop the cybernetic Borg from conquering Earth by
> changing the past.
>
>

Reply at Middle


> After the release of the seventh film, Star Trek Generations (1994),
> Paramount tasked writers Brannon Braga and Ronald D. Moore with developing
> a sequel. Braga and Moore wanted to feature the Borg in the plot, while
> producer Rick Berman wanted a story involving time travel. The writers
> combined the two ideas; they initially set the film during the European
> Renaissance, but changed the time period the Borg corrupted to the mid-21st
> century after fearing the Renaissance idea would be too kitsch. After two
> better-known directors turned down the job, cast member Jonathan Frakes was
> chosen to direct, to make sure the task fell to someone who understood Star
> Trek. It was Frakes' first theatrical film.
> View entire thread on Jive
> ------------------------------
> DISCUSSION
>

Reply at tail
"""

replyHTMLTemplate = """<div dir="ltr">Reply at Beginning<div class="gmail_extra"><br><div class="gmail_quote">On {timestamp}, {authorName} <span dir="ltr">&lt;<a href="mailto:{googleAdminEmail}" target="_blank">{googleAdminEmail}</a>&gt;</span> wrote:<br><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex"><div style="text-align:left;max-width:700px">
    <span style="font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;color:#222222;font-weight:lighter;line-height:1.35"><div>
 <div>

  <div>
   <div>
    <strong>Star Trek:</strong> First Contact is a 1996 American science fiction film released by Paramount Pictures. It is the eighth feature film in the Star Trek film franchise, and the second film in the series to star the cast of the television series Star Trek: The Next Generation. In the film&#39;s plot, the crew of the Starship USS Enterprise-E travel back in time to the mid-21st century to stop the cybernetic Borg from conquering Earth by changing the past.
   </div>
   <div style="min-height:8pt;padding:0px">
     </div></div></div></div></span></div></blockquote><div><br></div><div>Reply at Middle</div><div> </div><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex"><div style="text-align:left;max-width:700px"><span style="font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;color:#222222;font-weight:lighter;line-height:1.35"><div><div><div><div style="min-height:8pt;padding:0px">
   </div>
   <div>
    After the release of the seventh film, Star Trek Generations (1994), Paramount tasked writers Brannon Braga and Ronald D. Moore with developing a sequel. Braga and Moore wanted to feature the Borg in the plot, while producer Rick Berman wanted a story involving time travel. The writers combined the two ideas; they initially set the film during the European Renaissance, but changed the time period the Borg corrupted to the mid-21st century after fearing the Renaissance idea would be too kitsch. After two better-known directors turned down the job, cast member Jonathan Frakes was chosen to direct, to make sure the task fell to someone who understood Star Trek. It was Frakes&#39; first theatrical film.
   </div>
  </div>

 </div>
</div>
</span>
<div style="text-align:right"><span style="font-family:Arial,Helvetica,sans-serif;font-size:10pt;color:#999999;font-weight:lighter">View
entire thread on <a style="color:#59a8df;font-weight:bold;text-decoration:none" href="" target="_blank">Jive</a></span></div>
<hr style="height:1px;border:none;background-color:#a9a9a9;color:#a9a9a9"><span style="color:#fffffe">DISCUSSION</span>
</div>
</blockquote></div><br></div><div class="gmail_extra">Reply at tail</div></div>
"""

ReplyReplyTextTemplate = """
Reply Reply First

On {timestamp}, <{replyEmail}> wrote:

> Reply at Beginning
>
> On {timestamp}, {authorName} <
> {googleAdminEmail}> wrote:
>
>> *Star Trek:* First Contact is a 1996 American science fiction film
>> released by Paramount Pictures. It is the eighth feature film in the Star
>> Trek film franchise, and the second film in the series to star the cast of
>> the television series Star Trek: The Next Generation. In the film's plot,
>> the crew of the Starship USS Enterprise-E travel back in time to the
>> mid-21st century to stop the cybernetic Borg from conquering Earth by
>> changing the past.
>>
>
> Reply at Middle
>

Reply Reply Second


> After the release of the seventh film, Star Trek Generations (1994),
>> Paramount tasked writers Brannon Braga and Ronald D. Moore with developing
>> a sequel. Braga and Moore wanted to feature the Borg in the plot, while
>> producer Rick Berman wanted a story involving time travel. The writers
>> combined the two ideas; they initially set the film during the European
>> Renaissance, but changed the time period the Borg corrupted to the mid-21st
>> century after fearing the Renaissance idea would be too kitsch. After two
>> better-known directors turned down the job, cast member Jonathan Frakes was
>> chosen to direct, to make sure the task fell to someone who understood Star
>> Trek. It was Frakes' first theatrical film.
>> View entire thread on Jive
>> ------------------------------
>> DISCUSSION
>>
>
> Reply at tail
>

Reply Reply Third
"""

ReplyReplyHtmlTemplate = """
<div dir="ltr">Reply Reply First<div class="gmail_extra"><br><div class="gmail_quote">On {timestamp},  <span dir="ltr">&lt;<a href="mailto:{replyEmail}" target="_blank">{replyEmail}</a>&gt;</span> wrote:<br><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex"><div dir="ltr">Reply at Beginning<div class="gmail_extra"><br><div class="gmail_quote"><span class="">On {timestamp}, <a href="mailto:{authorEmail}" target="_blank">{authorName}</a> <span dir="ltr">&lt;<a href="mailto:{googleAdminEmail}" target="_blank">{googleAdminEmail}</a>&gt;</span> wrote:<br><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex"><div style="text-align:left;max-width:700px">
    <span style="font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;color:#222222;font-weight:lighter;line-height:1.35"><div>
 <div>

  <div>
   <div>
    <strong>Star Trek:</strong> First Contact is a 1996 American science fiction film released by Paramount Pictures. It is the eighth feature film in the Star Trek film franchise, and the second film in the series to star the cast of the television series Star Trek: The Next Generation. In the film&#39;s plot, the crew of the Starship USS Enterprise-E travel back in time to the mid-21st century to stop the cybernetic Borg from conquering Earth by changing the past.
   </div>
   <div style="min-height:8pt;padding:0px">
     </div></div></div></div></span></div></blockquote><div><br></div></span><div>Reply at Middle</div></div></div></div></blockquote><div><br></div><div>Reply Reply Second</div><div> </div><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex"><div dir="ltr"><div class="gmail_extra"><div class="gmail_quote"><span class=""><div> </div><blockquote class="gmail_quote" style="margin:0 0 0 .8ex;border-left:1px #ccc solid;padding-left:1ex"><div style="text-align:left;max-width:700px"><span style="font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;color:#222222;font-weight:lighter;line-height:1.35"><div><div><div><div style="min-height:8pt;padding:0px">
   </div>
   <div>
    After the release of the seventh film, Star Trek Generations (1994), Paramount tasked writers Brannon Braga and Ronald D. Moore with developing a sequel. Braga and Moore wanted to feature the Borg in the plot, while producer Rick Berman wanted a story involving time travel. The writers combined the two ideas; they initially set the film during the European Renaissance, but changed the time period the Borg corrupted to the mid-21st century after fearing the Renaissance idea would be too kitsch. After two better-known directors turned down the job, cast member Jonathan Frakes was chosen to direct, to make sure the task fell to someone who understood Star Trek. It was Frakes&#39; first theatrical film.
   </div>
  </div>

 </div>
</div>
</span>
<div style="text-align:right"><span style="font-family:Arial,Helvetica,sans-serif;font-size:10pt;color:#999999;font-weight:lighter">View
entire thread on <a style="color:#59a8df;font-weight:bold;text-decoration:none" href="" target="_blank">Jive</a></span></div>
<hr style="height:1px;border:none;background-color:#a9a9a9;color:#a9a9a9"><span style="color:#fffffe">DISCUSSION</span>
</div>
</blockquote></span></div><br></div><div class="gmail_extra">Reply at tail</div></div>
</blockquote></div><br></div><div class="gmail_extra">Reply Reply Third</div></div>
"""

ContentOnJiveTemplate = """<body><p><strong>Star Trek:</strong> First Contact is a 1996 American science fiction film released by Paramount Pictures. It is the eighth feature film in the Star Trek film franchise, and the second film in the series to star the cast of the television series Star Trek: The Next Generation. In the film\'s plot, the crew of the Starship USS Enterprise-E travel back in time to the mid-21st century to stop the cybernetic Borg from conquering Earth by changing the past.</p><p style=\"min-height: 8pt; padding: 0px;\">&#160;</p><p>After the release of the seventh film, Star Trek Generations (1994), Paramount tasked writers Brannon Braga and Ronald D. Moore with developing a sequel. Braga and Moore wanted to feature the Borg in the plot, while producer Rick Berman wanted a story involving time travel. The writers combined the two ideas; they initially set the film during the European Renaissance, but changed the time period the Borg corrupted to the mid-21st century after fearing the Renaissance idea would be too kitsch. After two better-known directors turned down the job, cast member Jonathan Frakes was chosen to direct, to make sure the task fell to someone who understood Star Trek. It was Frakes\' first theatrical film.</p></body>"""

ReplyFracs = ['Reply at Beginning', 'Reply at Middle', 'Reply at tail',
              'First Contact is a 1996', 'After the release of the seventh']

ReplyReplyFracs = ReplyFracs + ['Reply Reply First', 'Reply Reply Second', 'Reply Reply Third']

import unittest

class ReplyInline(unittest.TestCase):
    def test_inline_reply(self):

        Subject = "discussion for inline reply" + datetime.datetime.now().isoformat()
        # Subject = "discussion for inline reply 1.4"

        content = jiveHelper.createContent(groupName=group['groupName'],
                                 user=account['User4'],
                                 title=Subject,
                                 text=ContentOnJiveTemplate)

        print(content)
        time.sleep(180)

        recieved = CheckEmailHelper.findEmailBySubject(user=account["User2"],
                                            subject=Subject,
                                            to=group['groupName'])

        ReplyEmail(Subject=Subject,
                   From=account["User2"],
                   TEXT=replyTEXTTemplate.format(timestamp=datetime.datetime.now().ctime(), authorName = account['User4']['displayName'], googleAdminEmail=account['GoogleAdmin']['username']),
                   HTML=replyHTMLTemplate.format(timestamp=datetime.datetime.now().ctime(), authorName = account['User4']['displayName'], googleAdminEmail=account['GoogleAdmin']['username']),
                   ReplyTo=group['groupKey'],
                   Origin=recieved)

        print('inline reply')

        time.sleep(180)

        # content = jiveHelper.findDisussionBySubject(Subject)
        # contentID = content["discussion"].split('/')[-1]
        contentID = content['contentID']
        comments = jiveHelper.findAllCommentsByContentID(contentID)
        #
        self.assertEqual(len(comments), 1)
        #
        commentContent = comments[0]['content']['text']
        #
        for frac in ReplyFracs:
            self.assertIsNotNone(re.search(r'%s' % frac, commentContent))


        ### reply inline email

        recieved = CheckEmailHelper.findEmailListBySubject(
                                        user=account["User5"],
                                        subject=Subject,
                                        to=group['groupName'])[-1]

        ReplyEmail(Subject=Subject,
                   From=account["User5"],
                   ReplyTo=group['groupKey'],
                   Origin=recieved,
                   TEXT=ReplyReplyTextTemplate.format(
                       timestamp = datetime.datetime.now().ctime(),
                       replyEmail = account['User2']['email'],
                       authorName = account['User4']['displayName'],
                       googleAdminEmail = account['GoogleAdmin']['username']
                   ),
                   HTML=ReplyReplyHtmlTemplate.format(
                       timestamp = datetime.datetime.now().ctime(),
                       replyEmail = account['User2']['email'],
                       authorName = account['User4']['displayName'],
                       authorEmail = account['User4']['email'],
                       googleAdminEmail = account['GoogleAdmin']['username']
                   ))

        print('third')
        time.sleep(180)

        comments = jiveHelper.findAllCommentsByContentID(contentID)

        self.assertEqual(len(comments), 2)

        commentContent = comments[1]['content']['text']

        for frac in ReplyReplyFracs:
            self.assertIsNotNone(re.search(r'%s' % frac, commentContent))



