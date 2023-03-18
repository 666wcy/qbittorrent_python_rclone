#!/usr/bin/python
# -*- coding: UTF-8 -*-
from subprocess import Popen, PIPE
import os
import sys

import json
os.chdir(os.path.dirname(__file__))
with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.loads(f.read())
    f.close()



def start_upload_move(dir,folder,Remote,Upload):
    print(folder)
    dir=str(dir).replace("\\\\","\\")
    dir = dir.rstrip('\\')
    dir = dir.rstrip('/')

    folder=str(folder).replace("\\","/")
    folder=str(folder).replace("//","/")
    folder= folder.rstrip('\\')
    folder = folder.rstrip('\\')

    print(folder)
    if folder!="":
        print("上传判断，文件夹")
        if Remote == "":
            command = f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Upload}/{folder}\"  -v --stats=1s --stats-one-line   "
        else:

            command=f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Remote}:{Upload}/{folder}\"  -v --stats=1s --stats-one-line   "
        print(command)
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        print(f"运行结果:{data}")
        sys.stdout.flush()
        return f"{Remote}:{Upload}/{folder}"
    else:
        if Remote == "":
            command=f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Upload}\"  -v --stats=1s --stats-one-line "
        else:
            command=f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Remote}:{Upload}\"  -v --stats=1s --stats-one-line "
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        print(f"运行结果:{data}")
        sys.stdout.flush()
        if Remote == "":
            return f"{Upload}"
        else:
            return f"{Remote}:{Upload}"


def start_upload(dir,folder,Remote,Upload):
    print(folder)
    dir=str(dir).replace("\\\\","\\")
    dir = dir.rstrip('\\')
    dir = dir.rstrip('/')

    folder=str(folder).replace("\\","/")
    folder=str(folder).replace("//","/")
    folder= folder.rstrip('\\')
    folder = folder.rstrip('\\')
    print(folder)
    if folder!="":
        print("上传判断，文件夹")
        os.system(f"ls \"{dir}\"")
        if Remote == "":
            command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}/\"  \"{Upload}/{folder}\"  -v --stats=1s --stats-one-line "
        else:
            command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}/\"  \"{Remote}:{Upload}/{folder}\"  -v --stats=1s --stats-one-line "
        print(command)
        sys.stdout.flush()
        os.system(command)

        return f"{Remote}:{Upload}/{folder}"
    else:
        os.system(f"ls \"{dir}\"")
        if Remote == "":
            command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}\"  \"{Upload}\"  -v --stats=1s --stats-one-line "
        else:
            command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}\"  \"{Remote}:{Upload}\"  -v --stats=1s --stats-one-line "
        print(command)
        os.system(command)
        if Remote == "":
            return f"{Upload}"
        else:
            return f"{Remote}:{Upload}"



if __name__ == '__main__':
    '''dir="D:\\BaiduNetdiskDownload\\xmind"
    start_upload(dir)'''
    print()