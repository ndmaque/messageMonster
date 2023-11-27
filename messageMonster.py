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
import shutil
from shutil import copytree, ignore_patterns

import tools # imports tools.py with our custom functions to save clutter
import glob

# absolute path to search all text files inside a specific folder
path = r'inbox_examples/*.txt'
files = glob.glob(path)
print(files[0])


# node should be running the server in folder api/api.js
api_url = 'http://localhost:3000/api/'

# fetch and populate global variables from the http api
users = tools.get_api_data(api_url + 'users')
messages = tools.get_api_data(api_url +'messages')
messages_sent = tools.get_api_data(api_url + 'messages_sent')



def main():
    print('Api found: {} Users, {} Messages, {} Messages_Sent'.format(len(users), len(messages), len(messages_sent)))
    # Load dummy data: copy the /inbox_examples files to /inbox so we have something to process
    shutil.copytree('inbox_examples', 'inbox', ignore=ignore_patterns('\.git*'), dirs_exist_ok=True)

    # loop forever checking for new files to read and post to the api storage 
    while True:
        tools.process_inbox_messages(messages, api_url)
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

