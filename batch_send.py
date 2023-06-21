import re
import ssl
import smtplib
import imaplib
import sys
import time
import traceback
import random

SUBJECT_REGEX = r"Subject\:\s*(?P<subject>.*)\s"
IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = "993"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "465"
ORIGINATING_EMAIL_ADDRESS = "otbeatreport@orangetheoryfitness.com"

def send(email_address, password, receiving_email_address, mailbox):
    try:
        ssl_context = ssl.create_default_context()
        imap4ssl = imaplib.IMAP4_SSL(host=IMAP_SERVER, port=IMAP_PORT, ssl_context=ssl_context)
        imap4ssl.login(email_address, password)
        if mailbox == "":
            imap4ssl.select()
        else:
            imap4ssl.select(mailbox)
        message_ids = imap4ssl.search(None, "FROM", ORIGINATING_EMAIL_ADDRESS)[1][0].split()
        print("Found " + str(len(message_ids)) + " matching messages")
        subject_pattern = re.compile(SUBJECT_REGEX)
        messages = []
        for message_id in message_ids:
            message = imap4ssl.fetch(message_id, "(RFC822)")[1][0][1].decode("utf-8")
            message = message[message.find("Content-Type: "):]
            messages.append(message)
        imap4ssl.close()
        imap4ssl.logout()
        smtpssl = smtplib.SMTP_SSL(host=SMTP_SERVER, port=SMTP_PORT, context=ssl_context)
        smtpssl.login(email_address, password)
        count = 1
        for message in messages:
            smtpssl.sendmail(email_address, receiving_email_address, message)
            print("Progress: {percentage:.2f}%".format(percentage=(count / len(messages) * 100)))
            count += 1
            delay = random.randrange(1, 5)
            time.sleep(delay)
        smtpssl.quit()
        print("Finished forwarding all mail")
    except Exception as e:
        raise Exception("Error interacting with mail server: " + str(e))
