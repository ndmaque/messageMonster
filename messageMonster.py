# This how the framework might look after my first thoughts about the workflow
# There is a list of messages, think of it as a message queue
# Pending messages can be sent and successful messages details will be put into the sent list
# The original message status will be updated to 'complete' and stays where it is
# A new message can be added to the list and marked as 'pending', function not created yet

# The reason we use a message queue is because sometimes the mail or message server is down and will be auto sent later


# These global variables are hard coded for now but gives an idea what the data might look like.
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
    print('get_bcc_list() called: returns a list of recipients in BCC format')

def send_email(message):
    bccList = get_bcc_list()
    print('send_email() called: creates email with To, Subject, Body and BCC etc, sends it to a mail server which returns a transaction ID')

def send_mqtt(message):
    print('send_mqtt() called: IF the message type was mqtt it will format and send using a subscription service')

def print_sent_messages():
    print('print_sent_messages() called: prints a list of all sent message with date time txID Subject and Body etc')

def send_pending_messages():
    print('send_pending_messages() called: finds all messages with status=pending and sends them')
    # iterate for each pending...
    send_email('a subject and message array')
    

# main controls the entire show
def main():
    send_pending_messages()
    print_sent_messages()

# just run main()
main()