import os
import sys
import pathlib
import shutil
from datetime import datetime


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Error: input log file(*.kev) not specified')
        sys.exit()
    input_kev_file=sys.argv[1]
    home_dir=str(pathlib.Path.home())
    qde_workspace_dir=home_dir+"/ide-7.1-workspace/tracelog"
    dest_kev_dir=qde_workspace_dir + "/" + datetime.now().strftime("%Y%m%d")
    if not os.path.exists(dest_kev_dir):
        os.makedirs(dest_kev_dir)
    dirname,filename=os.path.split(input_kev_file)
    if os.path.exists(dest_kev_dir+"/"+filename):
        os.remove(dest_kev_dir+"/"+filename)
    shutil.move(input_kev_file, dest_kev_dir)
    print("dest_kev_dir: ", dest_kev_dir)

