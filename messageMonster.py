import datetime

# some global variables hard coded for now
# TODO move these out of this script and onto a file server or web api like a real world situation
# 3 messages, 1 sent OK and 2 pending, don't worry about how they got into the message queue right now
# in this scenario when the script is called it will process any pending messages to all users
messages = [
    {'sender_name': 'bob smith', 'sender_email': 'b@smith.uk', 'send_method': 'email', 'date_created': '2023-10-18 10:16', 'status': 'pending',  'subject': 'NAS 1234 cpu temp is 48C', 'body': 'Please fix it and report back'},
    {'sender_name': 'jane doe',  'sender_email': 'jane@d.com', 'send_method': 'email', 'date_created': '2023-10-05 16:25', 'status': 'pending',  'subject': 'CRM database going slow',  'body': 'Dave said it might be the sync broken again'},
    {'sender_name': 'john doe',  'sender_email': 'john@d.com', 'send_method': 'mqtt',  'date_created': '2023-09-05 16:25', 'status': 'complete', 'subject': 'Lost network connection',  'body': 'The DNS server is playing up'} 
]

messages_sent = [] # empty right now but will contain these fields: {message_index, date_sent, txID, sender, recipients}

users = [
    {'id': 1234, 'first_name': 'andy', 'last_name': 'Mac', 'email': 'a@mac', 'phone': '+44 (0) 77777 223344', 'contact_method': 'mqtt', 'address': {'street': '101 high street', 'city': 'Nottingham', 'postcode': 'NG2 8PP'}},
    {'id': 5678,'first_name': 'andy', 'last_name': 'Maddock', 'email': 'a@Maddock', 'phone': '077777 445566', 'contact_method': 'email','address': {'street': '98 Hackers Ave', 'city': 'Nottingham', 'postcode': 'NG24 6QQ'}}
]

# All the functions go here
def get_bcc_list():
    bcc = []
    for user in users:
        bcc.append('{} <{}>'.format(user['email'], user['email']))
    
    return ', '.join(bcc)

def send_email(message):
    # send a mail to the sender and BCC all users
    email = {}
    email["From"]    =  '{} <{}>'.format(message['sender_name'], message['sender_email'])
    email["To"]      = message['sender_email']
    email["Subject"] = message['subject']
    email["Body"]    = message['body']
    email["Bcc"]     = get_bcc_list()
    # this will eventually be sent to an email server somewhere, either one we create or just use our gmail
    
    print('sending email: subject = ', email['Subject']) # we will connect to a server and post the message but print it for now
    txID = 'abcdef' # when we send mail the server will send back a transaction id or receipt
    return {'txID': txID, 'To': email['Bcc']} # we can store this in the sent list maybe

def send_mqtt(message):
    # TODO send a message to each user or group via mtqq
    print('sending mqtt message')

def print_sent_messages():
    print('\n\n=======')
    for msg in messages_sent:
        msgKey = msg['message_index']
        text = 'Message:\t{}\ntxID:\t\t{}\nSent:\t\t{}\nSubject:\t{}'.format(msgKey, msg['txID'], msg['date_sent'], messages[msgKey]['subject'] )
        print(text)
        print('=======')
    print()

# all functions go here
def send_pending_messages():
    # find all 'pending' messages and loop them
    pending = list(filter(lambda msg: msg['status'] == 'pending', messages))
    print('Found {} pending messages\n'.format(len(pending)))

    for index in range(len(pending)):
        if(messages[index]['send_method'] == 'email'):
            response = send_email(messages[index]) # the response has the tsID and the recipients

            # update the message as complete and record it in messages_sent
            messages[index]['status'] = 'complete'
            messages[index]['date_sent'] = datetime.datetime.now()

            # insert a new record in messages_sent
            new_message = {'message_index': index, 'txID': response['txID'], 'date_sent': messages[index]['date_sent'], 'To': response['To']}
            messages_sent.append(new_message)
        else:
            send_mqtt(messages[index])

def main():
    send_pending_messages()
    print_sent_messages()

main()