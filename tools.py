import json

files_folder = 'files/'

def get_data(file_name):
    file_name = files_folder + file_name + '.json'
    fh = open(file_name,'r') # open the file in Read Only mode 'r', you can't save this file
    data = json.load(fh)
    fh.close()
    return data

def save_data(file_name, data):
    file_name = files_folder + file_name + '.json'
    fh = open(file_name,'w') # open the file in Write mode 'w'
    fh.write(json.dumps(data, indent = 4))
    fh.close()