import os
import sys
import time
import pathlib
import shutil
from datetime import datetime


qde_title='ide-7.1-workspace - Momentics IDE'
qde_dialog='Error loading SDKs'
qde_cmd='~/qnxmomenticside/qde &'


def active_window(title):
    os.system('xdotool search --name "{}" windowactivate'.format(title))

def close_window(title):
    os.system('xdotool search --name "{}" windowclose'.format(title))

def send_keys(key_code,repeat=1,delay=0.8):
    for i in range(0,repeat):
        time.sleep(delay)
        os.system('xdotool key ' + key_code)

def qde_autokey():
    os.system(qde_cmd)
    time.sleep(10)
    send_keys('Return')

    send_keys('F5',1,2)
    send_keys('Right',1,1)
    send_keys('End',1)
    send_keys('Right',1,1)
    send_keys('Down')
    send_keys('Return')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: input log file(*.kev) not specified')
        sys.exit()
    input_kev_file=sys.argv[1]
    home_dir=str(pathlib.Path.home())
    qde_workspace_dir=home_dir+"/ide-7.1-workspace/tracelog"

    temp_kev_dir=qde_workspace_dir + "/kev"
    if os.path.exists(temp_kev_dir):
        os.removedirs(temp_kev_dir)
    os.makedirs(temp_kev_dir)
    shutil.copy(input_kev_file, temp_kev_dir)
    print("temp_kev_dir: ", temp_kev_dir)
    qde_autokey()


