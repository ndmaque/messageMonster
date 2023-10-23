# Basics 2: The separation of code and data

# 1) use json text files as a database so we can store data externally and not inside this script 
# 2) move some functions into another file and import them because all programs get messy eventually

# the users and message lists can and should be stored outside of the python script
# this will solve the problem that the script always starts with no sent messages
# we dont some novice hacking around inside our script and breaking the code just to add a new user

# json files are awesome and used everywhere, they store program arrays as a simple text file
# every language can read and write json, it is the universal way to send data from server to server
# NB: drag and drop a json file into any browser and see what happens!

# in reality the users list will be in a db or fetched from a server api such as http://corp-hq.uk/users/all
# today we will emulate that and just put the data in local files, it's just a tiny code tweak later to get it from a server api

# NB: there's a new folder called files/ in this branch 
#     and a new file called tools.py for our code separation


from datetime import datetime
import tools # imports our own custom functions to save clutter in this script

# declare and populate global variables
users = tools.get_data('users')
messages = tools.get_data('messages')
messages_sent = tools.get_data('messages_sent')


def add_message(sender_name, subject, body):
    # get the current date as an object
    now = datetime.now()
    # create a string in Y-m-D H:M:S  NB: %m = month  %M = mins
    date_created = now.strftime("%Y-%m-%d %H:%M:%S") 

    msg = {
        'sender_name': sender_name, 
        'sender_email': 'tl@corp_hq.uk', 
        'send_method': 'email', 
        'date_created': date_created, 
        'status': 'pending',  
        'subject': subject, 
        'body': body
    }
    messages.append(msg)

    # save all messages to file
    tools.save_data('messages', messages)

def main():
    print('message count A = {}'.format(len(messages)))
    add_message('Sarah Watts', 'Dog and duck tonight', '7pm sharp')
    print('message count B = {}'.format(len(messages)))

main()

# what we learnt today is:
# data should not be hard coded in the script but stored externally
# and most of our 'helper' functions don't need to be in here either, just the core code
# json is a common language that everyone speaks
# we saved our data and left it open for other systems to read and write without python skills

# NB: the add_message() method could also go into tools
# Tip: open a terminal and tail the json files to see changes
# tail -f files/messages.json

