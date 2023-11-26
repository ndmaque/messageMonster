# Basics : Getting and posting data from a Web Api/REST server

# this .py script permanently scans the inbox folder looking for new files like a drop box or mail server
# if a new file is found we read the content, build a message and post it to the http api which stores it in messages as pending (not sent)
# the script main() will copy some example files into /inbox for testing other wise use cli while running this py
# $ cp -r inbox_examples/* inbox

# today we will just process the messages and save them on the api server as pending and not actually send them
# once we have mqtt running we will send or publish them 

# a valid message file must have at least 3 lines
# line 0 is the sender name or id/email whatever so we know who created it for the messages log, prolly use email for today
# line 1 the mqtt topic paths to publish, you could publish it to many topics: msgs/it msgs/admin msgs/amaddock
# lines 2+ is the message content itself, typically plain text or a json string


# Start the web server in a new terminal
# 
# $ cd messageMonster/api/
# note the api.js file, it's a web server, there is also a package.json which manages required packages etc
# the very first time only you will need to run the installer which gets all the node packages or libraries
# puts them in a node_modules folder and we have a .gitignore entry for this folder with thousands of files

# $ npm install
# only above once, np if you do tho
# now the packages are in place run the app
# $ node api.js

# server is running check curl or browser...
# $ curl http://localhost:3000 
# http://localhost:3000/api/users           get all users
# http://localhost:3000/api/users/ABC       get user by id
# http://localhost:3000/api/messages        get all messages & post (create) a new message
# http://localhost:3000/api/messages_sent   get all sent
# http://localhost:3000                     an html page
# Yay node web server is running


from datetime import datetime
import time
import os
import shutil
import re

import tools # imports tools.py with our custom functions to save clutter


# node should be running the server in folder api/api.js
api_url = 'http://localhost:3000/api/'

# populate global variables from the http api
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
    # sender, topics, content  all other lines 
    # topics is space seperated string of publish paths: msg/it msg/amaddock etc   
    # NB: we dont need the sender for mqtt but we store it in the messages array for traceability
    # Security: never trust user input (the message file), check it's not malicous code and valid format

    # valid if 3 or more lines
    if len(lines)-1 > 2:
        message = {}
        message['sender_email'] = lines[0].strip()
        message['topics'] = string_to_topics_array(lines[1])
        message['content'] = '\n'.join(lines[2: len(lines)]).strip() # join all the other lines 
        message['date_created']: datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message['status'] = 'pending'
        return message
    else: 
        return False 

# processes the first file into a message format and posts it to the api server which saves it to the Dbase aka json array
# when it is saved on the api it then deletes the file from inbox
# To put files into the inbox while running py, drag and drop from ui or cp -r example_msgs/* inbox
# NB: this function is being called from a permanent loop in python main()
def process_inbox_messages():
    folder = 'inbox/'
    # get a list of all files (that are not folders!)
    file_names = [fn for fn in os.listdir(folder) if os.path.isfile(folder + fn)]
    # check if we found a file name
    if(len(file_names) > 0) :
        # only process one file at a time, always the zeroeth one because we are in a loop and brb
        file_path = folder + file_names[0] # get the full file path to the zeroeth file in the files list
        message = parse_inbox_message(file_path) # read the file and see if it is valid

        if message:
            messages.append(message) # add it into the current messages array we loaded on boot
            res = tools.post_api_data(api_url+'message', message)
            if res:
                print('Message sent OK')
                os.remove(file_path) # if the api was good delete the processed file           
        else: 
            print('Error: moved to inbox_rejects')
            os.rename(file_path, "inbox_rejects/{}.bad".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))


def main():
    print('Api found: {} Users, {} Messages, {} Messages_Sent'.format(len(users), len(messages), len(messages_sent)))
    # copy the test message files to /inbox so we have something to process
    shutil.copytree('inbox_examples', 'inbox', dirs_exist_ok=True)

    # loop forever checking for new files 
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

