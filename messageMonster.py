# Basics : Simple Web Api server 
#
# in a new terminal 
# cd messageMonster/api/
# there is new js file, it's a web server, use node to run it
# node api.js
# check yr browser...
# http://localhost:3000/api/users 
# http://localhost:3000/api/users/1
# http://localhost:3000/api/messages
# http://localhost:3000/api/messages_sent
# http://localhost:3000 
# 


from datetime import datetime
import time
import os
import grequests
import requests
import httpx

import json
from playsound import playsound

import tools # imports our own custom functions to save clutter in this script

# node should be running the server in folder api/api.js
api_url = 'http://localhost:3000/api/'

# declare and populate global variables
# populate from web api 
users = requests.get(api_url + 'users').json()
messages = requests.get(api_url +'messages').json()
messages_sent = requests.get(api_url + 'messages_sent').json()


# TODO move to tools.py
def add_message(sender_email, subject, body):
    # get the current date as an object
    now = datetime.now()
    # create a string in Y-m-D H:M:S  NB: %m = month  %M = mins
    date_created = now.strftime("%Y-%m-%d %H:%M:%S") 

    msg = {
        'sender_name': '', 
        'sender_email': sender_email,
        'date_created': date_created, 
        'status': 'pending', 
        'topics': ['chat', 'users/msg'], 
        'subject': subject, 
        'body': body
    }
    print('adding inbox message to pending')
    messages.append(msg)

    # save messages array into the json file
    tools.post_api_data(api_url+'message', msg)

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
    print('{} Users\n{} Messages\n{} Sent'.format(len(users), len(messages), len(messages_sent)))
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

