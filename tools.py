from datetime import datetime
import json
import httpx
import re
import os


# makes an http post = create a new record on the api and save it
def post_api_data(url, data):
    data = json.dumps(data) # turn the python object to json string
    headers = {'Content-Type': 'application/json; charset=utf-8'}   # set the headers content type

    # added exception handlers to stop crash when http api is down
    try:
        res = httpx.post(url, data=data, headers=headers) # post and store the api response
        if res.status_code == httpx.codes.OK:
            # print('post OK response: ', res.status_code, res.json())
            # our api will return the updated messages but we won't use it as we already have them all
            return res.json()
        else:
            return False
    except Exception:
        print('post_api_data() ', Exception)
        return False


def get_api_data(url):
    try:
        res = httpx.get(url)
        if res.status_code == httpx.codes.OK:
            return res.json()
        else:
            return []
    except Exception :
        print('get_api_data() ', Exception)
        return []

 
# helper func: replaces multiple white spaces with a single space between topics aka publish paths
# returns an array of topics to publish content on
def string_to_topics_array(line):
    line = re.sub(r' +(?= )', '', line.strip())
    topics = line.split(' ') # turn the space sep str into an array: msgs/admin msgs/andy
    return topics

# processes the first file into a message format and posts it to the api server which saves it to the Dbase aka json array
# when it is saved on the api it then deletes the file from inbox
# To put files into the inbox while running py, drag and drop from ui or cp -r example_msgs/* inbox
# NB: this function is being called from a permanent 1 second loop in python main()
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
            print('Bad Message: moved {} to inbox_rejects/'.format(file_path))
            os.rename(file_path, "inbox_rejects/{}.bad".format(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))


# helper func to open a msg file and transform to message format: sender, topics, message
# returns an object 
def parse_inbox_message(file_path):
    content = open(file_path, 'r')
    lines = content.read().split('\n')
    # should have at least 3 \n or new lines of text in the file
    # sender, topics and content is all the other lines 
    # topics is a space separated string of publish paths: msg/it msg/amaddock etc   
    # NB: we dont need the sender for mqtt but we store it in messages sender and add to end of message maybe
    # Security: never trust user input (the message file), check it's not malicous code and valid format

    # valid if 3 or more lines TODO check lines are not empty etc
    if len(lines)-1 > 2:
        message = {}
        message['sender'] = lines[0].strip()
        message['topics'] = string_to_topics_array(lines[1])
        message['content'] = '\n'.join(lines[2: len(lines)]).strip() # join all the other lines 
        message['created'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message['status'] = 'pending'
        return message
    else: 
        return False 