import json
import httpx


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
