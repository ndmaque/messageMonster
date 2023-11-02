import json
import os
from datetime import datetime
import time


class DataTools:

    def __init__(self):
        self.users = []
        self.messages = []
        self.messages_sent = []
        self.data_folder = 'data_files/'
        self.load_data()

    # files
    def load_data(self):
        self.messages = self.get_data('messages')
        self.messages_sent = self.get_data('messages_sent')
        self.users = self.get_data('users')

    def get_data(self, file_name):
        file_name = self.data_folder + file_name + '.json'
        fh = open(file_name,'r') 
        data = json.load(fh)     
        fh.close()
        return data

    def save_data(self, file_name, data):
        file_name = self.data_folder + file_name + '.json'
        fh = open(file_name,'w')
        fh.write(json.dumps(data, indent = 4))
        fh.close()


    # messages
    def get_inbox_message(self, file_path):
        file = open(file_path, 'r')
        lines = file.read().split('\n')
        sender = self.get_user('email', lines[0])
        topic = lines[1]
        message = False
        #print(file_path, lines)
      

        if len(lines) > 3 and sender:
            now = datetime.now()
            message = {}
            message['date_created'] = now.strftime('%Y-%m-%d %H:%M:%S')
            message['status'] = 'pending'
            message['sender'] = sender
            message['topic'] = topic
            message['body'] = '\n'.join(lines[2: len(lines)])

        os.remove(file_path)
        return message


    # looks for the first file, processes it into a message then deletes it
    def check_for_new_messages(self):
        folder = 'inbox/'
        files = [fn for fn in os.listdir(folder) if os.path.isfile(folder + fn)]
        
        if(len(files) > 0) :
            #new_message = self.get_inbox_message(folder + files[0])
            return folder + files[0]

    def send_message(self, file_path):

        new_message = self.get_inbox_message(file_path)
        os.remove(file_path)
        if(new_message):
            # every user for now
            # mqtt.pub(topic, msg)
            for user in self.users:
                print('')


    # data
    def get_user(self, field, value):

        user = next((item for item in self.users if item[field] == value), False) 
        return user

    def save_message(self, new_message):
        self.messages.append(new_message)
        # sync/overwrite the messages json file
        self.save_data('messages', self.messages)