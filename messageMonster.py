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
import time
import os
# we had to run the python package installer pip for this library playsound:
# pip install playsound
from playsound import playsound

import tools # imports our own custom functions to save clutter in this script


# declare and populate global variables
users = tools.get_data('users')
messages = tools.get_data('messages')
messages_sent = tools.get_data('messages_sent')


# TODO move to tools.py
def add_message(sender_email, subject, body):
    # get the current date as an object
    now = datetime.now()
    # create a string in Y-m-D H:M:S  NB: %m = month  %M = mins
    date_created = now.strftime("%Y-%m-%d %H:%M:%S") 

    msg = {
        'sender_name': '', 
        'sender_email': sender_email, 
        'send_method': 'email', 
        'date_created': date_created, 
        'status': 'pending',  
        'subject': subject, 
        'body': body
    }
    print('adding inbox message to pending')
    messages.append(msg)

    # save messages array into the json file
    tools.save_data('messages', messages)

# TODO move to tools.py
def parse_inbox_message(file_path):
    content = open(file_path, 'r')
    lines = content.read().split('\n')

    # always make sure data makes sense before processing it
    if len(lines)-1 > 2:
        message = {}
        message['sender_email'] = lines[0]
        message['subject'] = lines[1]
        message['body'] = '\n'.join(lines[2: len(lines)]) # join all the other lines 
        return message
    else: 
        return False 

# looks for the first file, processes it into a message then deletes it
def check_for_new_messages():
    folder = 'inbox/'
    # get a list of all files that are not folders
    files = [fn for fn in os.listdir(folder) if os.path.isfile(folder + fn)]
    
    if(len(files) > 0) :
        #playsound('sound_files/submarine_ping.mp3')
        file_name = files[0]
        file_path = folder + file_name
        message = parse_inbox_message(file_path)

        if message:
            add_message(message['sender_email'], message['subject'], message['body'])
            os.remove(file_path)
            
        else: 
            print('bad message: do something')
            os.remove(file_path)

def main():
    # run forever checking for new files 
    while True:
        check_for_new_messages()
        time.sleep(2)

main()

# what we learnt today is:
# data should not be hard coded in the script but stored externally
# and most of our 'helper' functions don't need to be in here either, just the core code
# json is a common language that everyone speaks
# we saved our data and left it open for other systems to read and write without python skills
# how to use pip to install other libraries or packages

# NB: the add_message() method could also go into tools but will need a tweak
# Tip: open a terminal and tail the json files to see changes
#      tail -f files/messages.json

