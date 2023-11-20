import json
import httpx

# Files 
files_folder = 'data_files/'

def get_data(file_name):
    file_name = files_folder + file_name + '.json'
    fh = open(file_name,'r') # open the file in Read Only mode 'r', you can't save this file
    data = json.load(fh)     # parse the text into a python object
    fh.close()
    return data

def save_data(file_name, data):
    file_name = files_folder + file_name + '.json'
    fh = open(file_name,'w')                # open the file in Write mode 'w'
    fh.write(json.dumps(data, indent = 4))  # convert to json text and overwrite existing file
    fh.close()


# api : api/users api/users/1 api/messages api/messages_sent
def post_api_data(url, data):
    r = httpx.post(url, data=json.dumps(data), headers = {'Content-Type': 'application/json; charset=utf-8'})
    if r.status_code == httpx.codes.OK:
        print('post OK response: ', r.status_code, r.json())
        return r.json()
    else:
        print('Error http ', r.status_code)


def get_api_data(url,  options):
    r = httpx.get(url)
    if r.status_code == httpx.codes.OK:
        return r.json()
    else:
        print('Error http ', r.status_code)
