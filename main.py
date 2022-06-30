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

    # print(NSWorkspace.sharedWorkspace())
    return activeAppName


def get_app_id():
    from AppKit import NSWorkspace
    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationBundleIdentifier']
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
    with open(CONF['tasks_dir'] + '/' + d.strftime("%Y_%m_%d_%H_%M") + '_' + LOG_FILE, 'a') as outfile:
        # json.dump(data, outfile)
        # outfile.write("\n")
        data = data.values()
        outfile.write('\t'.join(data) + '\n')


starttime = time.time()

if not os.path.exists(CONF['tasks_dir']):
    os.mkdir(CONF['tasks_dir'])

while True:
    # for x in range(10):
    app_id = get_app_id().lower()
    is_locked = int(get_is_locked())

    if app_id == 'com.google.chrome':
        current_url = get_current_tab_url()
    else:
        current_url = ''
    data = dict(
        date=str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        user_id=str(CONF['user_id']),
        app_id=app_id,
        app_name=get_app_name(),
        is_locked=str(is_locked),
        url=current_url
    )
    # print(data)
    if (is_locked == 0):
        write_log(data)
    time.sleep(1.0 - ((time.time() - starttime) % 1.0))
