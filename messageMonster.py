# Basics : Getting and posting data from a Web Api/REST server
# in a new terminal 
# $ cd messageMonster/api/
# there is new js file /api/api.js, it's a web server, to run it:
# the very first time you will need to run the installer which gets all the node packages or libraries
# puts them in a node_modules folder and we have a .gitignore entry to not inlude them
# $ npm install
# $ node api.js
# server is running check curl or browser...
# $ curl http://localhost:3000 
# http://localhost:3000/api/users           get all users
# http://localhost:3000/api/users/ABC       get user by id
# http://localhost:3000/api/messages        get all & post (create) a new message
# http://localhost:3000/api/messages_sent   get all sent
# http://localhost:3000                     an html page
# Yay node web server is running

# this script permanently scans the inbox looking for new files dropped in
# if a new file is found we read the content, build a message and post it to the api which stores it in messages as pending (not sent)
# when you run this script, nothing happens until you drop a file in the /inbox
# there are some test files we can copy to inbox 
# $ cp -r inbox_examples/* inbox
# today we will just process the messages and save them on the api server

# the files must have at least 3 lines
# 1 is the sender name or id/email so we know who created it, we will use email for today
# 2 the mqtt topic paths to publish, you could publish to many topics: msgs/it msgs/admin msgs/amaddock
# 3+ lines are the message itself

from datetime import datetime
import time
import os
import shutil
import re

import tools # imports our own custom functions


# node should be running the server in folder api/api.js
api_url = 'http://localhost:3000/api/'

# populate global variables from the api
users = tools.get_api_data(api_url + 'users')
messages = tools.get_api_data(api_url +'messages')
messages_sent = tools.get_api_data(api_url + 'messages_sent')

# helper func: gets rid of multiple white spaces before creating an array from space seperated topics
# returns an array of topics to publish on
def string_to_topics_array(line):
    line = re.sub(r' +(?= )', '', line.strip())
    topics = line.split(' ')
    return topics


# TODO move to tools.py
def parse_inbox_message(file_path):
    content = open(file_path, 'r')
    lines = content.read().split('\n')
    # should have at least 3 \n or new lines of text in this array
    # 1) sender, 2) mqtt topic, and the rest is the message which could be many lines
    # line 2 can be multiple topics space seperated, the message will get published to all
    # NB: we dont need the sender for mqtt but we store it in the messages array for traceability
    # Security: never trust user input, make sure it makes sense before processing it

    # valid if 3 or more lines
    if len(lines)-1 > 2:
        message = {}
        message['sender_email'] = lines[0].strip()
        message['topics'] = string_to_topics_array(lines[1])
        message['content'] = '\n'.join(lines[2: len(lines)]) # join all the other lines 
        message['date_created']: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message['status'] = 'pending'
        return message
    else: 
        return False 

# processes the first file into a message format and posts it to the api server which saves it into the json array
# when it is saved on the api it then deletes the file from inbox
# To put files into the inbox while running py, drag and drop from ui or cp -r example_msgs/* inbox
def process_inbox_messages():
    folder = 'inbox/'
    # get a list of all files (that are not folders!)
    file_names = [fn for fn in os.listdir(folder) if os.path.isfile(folder + fn)]
    # check we found more than one file name
    if(len(file_names) > 0) :
        # only process one file at a time, always the zeroeth one because we are in a loop
        file_path = folder + file_names[0] # get the full file path to the zeroeth file in the files list
        message = parse_inbox_message(file_path) # read the file and see if it is valid

        if message:
            messages.append(message) # add it into the current messages array
            res = tools.post_api_data(api_url+'message', message)
            if res:
                os.remove(file_path) # if the api was good delete the processed file           
        else: 
            print('bad message: moved to inbox_rejects')
            os.rename(file_path, "inbox_rejects/{}.bad".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))


def main():
    print('Api found: {} Users, {} Messages, {} Messages_Sent'.format(len(users), len(messages), len(messages_sent)))
    # copy some test message files into /inbox so we have something to process
    shutil.copytree('inbox_examples', 'inbox', dirs_exist_ok=True)

    # run forever checking for new files 
    while True:
        process_inbox_messages()
        time.sleep(1)

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

