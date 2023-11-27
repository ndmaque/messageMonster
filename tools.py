from datetime import datetime
import json
import httpx
import re
import os


# makes an http post = create a new record on the api and save it
def post_api_data(url, data):
    data = json.dumps(data) # turn the python object to json string
    headers = {'Content-Type': 'application/json; charset=utf-8'}   # set the headers content type
    res = httpx.post(url, data=data, headers=headers) # post and store the api response

    if res.status_code == httpx.codes.OK:
        # print('post OK response: ', res.status_code, res.json())
        # our api will return the updated messages but we won't use it as we already have them all
        return res.json()
    else:
        # print('Api Error http ', res.status_code)
        return False


def get_api_data(url):
    res = httpx.get(url)
    if res.status_code == httpx.codes.OK:
        return res.json()
    else:
        print('Error http ', res.status_code)
        return []

 
# helper func: gets rid of multiple white spaces before creating an array from space seperated topics
# returns an array of topics to publish on
def string_to_topics_array(line):
    line = re.sub(r' +(?= )', '', line.strip())
    topics = line.split(' ')
    return topics

# processes the first file into a message format and posts it to the api server which saves it to the Dbase aka json array
# when it is saved on the api it then deletes the file from inbox
# To put files into the inbox while running py, drag and drop from ui or cp -r example_msgs/* inbox
# NB: this function is being called from a permanent loop in python main()
def process_inbox_messages(messages, api_url):
    folder = 'inbox/'
    # get a list of all files (that are not folders!)
    file_names = [fn for fn in os.listdir(folder) if os.path.isfile(folder + fn) and fn !='.gitignore']
    # check if we found a file name
    if(len(file_names) > 0) :
        # only process one file at a time, always the zeroeth one because we are in a loop and brb
        file_path = folder + file_names[0] # get the full file path to the zeroeth file in the files list
        message = parse_inbox_message(file_path) # read the file and see if it is valid

        if message:
            messages.append(message) # add it into the current messages array we loaded on boot
            res = post_api_data(api_url+'message', message)
            if res:
                print('Message sent OK')
                os.remove(file_path) # if the api was good delete the processed file           
        else: 
            print('Error: moved to inbox_rejects')
            os.rename(file_path, "inbox_rejects/{}.bad".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))


# helper func to open a msg file and transform to message format: sender, topics, message
# returns an object 
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