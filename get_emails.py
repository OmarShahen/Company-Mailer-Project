
import imaplib, email



def get_inbox(username, userAppPassword):
    
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, userAppPassword)
    _, mailbox = mail.select("inbox")
    N = 100
    mailbox = int(mailbox[0])
    print(mailbox)

    email_data = {}
    my_messages = []
    counter = 0
    for i in range(mailbox, mailbox-N, -1):
        _, data = mail.fetch(str(i), "(RFC822)")
        _, b = data[0]
        email_message = email.message_from_bytes(b)

        for header in ['Subject', 'to', 'from', 'date']:
            email_data[header] = email_message[header]
        
        for part in email_message.walk():
            if part.get_content_type()  == "text/plain":
                body = part.get_payload(decode = True)
                email_data['body'] = body.decode()
                my_messages.append(email_data)
        counter += 1
    
    print("Counter: ", counter)

        
        
    return my_messages






