import os
import subprocess
import re
import time
import datetime
import json
import Quartz
import time


def read_conf(fp):
    data = dict()
    try:
        with open(fp, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(e)
    return data

LOG_FILE = 'data.log'
CONF_FILE = 'conf.json'
CONF = read_conf(CONF_FILE)


def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

def get_app_name():
    from AppKit import NSWorkspace
    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    return activeAppName

def get_is_locked():
    d = Quartz.CGSessionCopyCurrentDictionary()
    is_locked = d.get("CGSSessionScreenIsLocked", 0)
    return is_locked

def get_current_tab_url():
    result = subprocess.run(['chrome-cli', 'info'], stdout=subprocess.PIPE)
    res = str(result.stdout).split('\\n')
    for x in res:
        if re.search('Url: (.*?)', x, flags=re.IGNORECASE):
            url_data = x.split(': ')
            return url_data[1]


def write_log(data):
    d = datetime.datetime.now()
    with open(CONF['tasks_dir']+'/'+d.strftime("%Y_%m_%d_%H_%M")+'_'+LOG_FILE, 'a') as outfile:
        json.dump(data, outfile)
        outfile.write("\n")


starttime=time.time()


if not os.path.exists(CONF['tasks_dir']):
    os.mkdir(CONF['tasks_dir'])

# while True:
for x in range(10):
    app_name = get_app_name()
    is_locked = int(get_is_locked())
    data = dict(
        date=str(datetime.datetime.now()),
        app_name=app_name,
        is_locked=is_locked,
        url=get_current_tab_url(),
    )
    write_log(data)
    time.sleep(1.0 - ((time.time() - starttime) % 1.0))


print('finish main!')