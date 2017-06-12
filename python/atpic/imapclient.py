#!/usr/bin/python3
"""
the mail server acepst the mails and is sent to a mail box

a notify triggers this scripts which parse the mail and dispatches it to the correct directory


"""
import imaplib
import email
import re
server = imaplib.IMAP4("madon.net")
server.login(b"someatpicuser",b"somepasswd")

# get the list of mail boxes
mboxes = server.list()[1]
for mbox in mboxes:
    print(mbox)
    # pass

