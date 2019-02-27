import requests
import os
import json
import time

def read_conf(fp):
    data = dict()
    try:
        with open(fp, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    return data

CONF_FILE = 'conf.json'
CONF = read_conf(CONF_FILE)

API_URL = CONF['api_url']

def send_file(file):
    with open(file, 'rb') as f:
        r = requests.post(API_URL, files={file: f})
        # print(r.content)
        code = r.status_code
        if code == 200:
            os.remove(file)

mypath = os.getcwd()+'/'+CONF['tasks_dir']
starttime=time.time()


for x in range(2):
    time.sleep(60)
    files = os.listdir(mypath)
    for f in files:
        file = mypath+'/'+f
        # print(file)
        send_file(file)

print('finish send!')