import os
import sys
import time
import pathlib
import shutil
import cv2
import numpy as np
import Xlib.display as display
import Xlib.X as X
import Xlib.Xutil as Xutil
import Xlib.ext.xtest as xtest
from datetime import datetime


qde_title='ide-7.1-workspace - Momentics IDE'
qde_dialog='Error loading SDKs'
qde_cmd='~/qnxmomenticside/qde &'


def active_window(title):
    os.system('xdotool search --name "{}" windowactivate'.format(title))

def close_window(title):
    os.system('xdotool search --name "{}" windowclose'.format(title))

def send_keys(key_code,repeat=1,delay=1.2):
    for i in range(0,repeat):
        time.sleep(delay)
        os.system('xdotool key ' + key_code)

def find_image_on_screen(image_path):
    target = cv2.imread(image_path)
    target = cv2.convertScaleAbs(target)
    th, tw = target.shape[:2]

    disp = display.Display()
    screen = disp.screen()
    root = screen.root
    width = root.get_geometry().width
    height = root.get_geometry().height

    raw = root.get_image(0, 0, width, height, X.ZPixmap, 0xffffffff)
    image = np.frombuffer(raw.data, dtype='uint8').reshape(height, width, 4)
    image = image[:, :, :3]
    result = cv2.matchTemplate(image, target, cv2.TM_CCOEFF_NORMED)
    threshold = 0.75
    yloc, xloc = np.where(result >= threshold)
    for (x, y) in zip(xloc, yloc):
        return (x + tw / 2, y + th / 2)

    return None

def mouse_click(x, y,button=1):
    print(f'mouse_click pos:({x}, {y})')
    os.system('xdotool mousemove {} {} click {}'.format(x,y,button))

def click_image(image_path, delay_time=1.0,x_offset=0,y_offset=0,button=1):
    time.sleep(delay_time)
    pos = find_image_on_screen(image_path)
    if pos is not None:
        print(f'find image pos:({pos[0]}, {pos[1]})')
        mouse_click(pos[0]+x_offset, pos[1]+y_offset,button)
    else:
        print('not find image!')

def qde_autokey():
    # launch qde
    os.system(qde_cmd)
    time.sleep(10)
    send_keys('Return')
    # open kev
    send_keys('F5',1,2)
    send_keys('Right',1,1)
    send_keys('End',1)
    send_keys('Right',1,1)
    send_keys('Down')
    send_keys('Return')

    # mouse click icon
    click_image('images/ClientServerTab.png',65)
    click_image('images/ClientServerTools.png',1,-23)
    click_image('images/ClientServerTools.png',3,23)
    send_keys('Down',2)
    send_keys('Return')
    click_image('images/ClientServerTools.png',10,23)
    send_keys('Down',3)
    send_keys('Return')
    send_keys('Tab',3)
    send_keys('Right')
    send_keys('End')
    send_keys('Up')
    send_keys('Return',3)
    click_image('images/CloseTab.png',1,23,0,2)
    send_keys('Down')
    send_keys('Return')
    close_window(qde_title)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: input log file(*.kev) not specified')
        sys.exit()
    input_kev_file=sys.argv[1]
    home_dir=str(pathlib.Path.home())
    qde_workspace_dir=home_dir+"/ide-7.1-workspace/tracelog"

    temp_kev_dir=qde_workspace_dir + "/kev"
    if os.path.exists(temp_kev_dir):
        shutil.rmtree(temp_kev_dir)
    os.makedirs(temp_kev_dir)
    shutil.copy(input_kev_file, temp_kev_dir)
    print("temp_kev_dir: ", temp_kev_dir)
    
    temp_csv_dir=qde_workspace_dir + "/csv"
    if os.path.exists(temp_csv_dir):
        shutil.rmtree(temp_csv_dir)
    os.makedirs(temp_csv_dir)

    qde_autokey()

    csv_temp_file=qde_workspace_dir + "/csv/output.csv"
    (input_path, input_filename)=os.path.split(input_kev_file)
    input_filename = input_filename.replace('.kev', '.csv')
    shutil.copy(csv_temp_file, input_path)
    shutil.move(input_path+"/output.csv", input_path+"/"+input_filename)




