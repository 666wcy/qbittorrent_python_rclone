#!/usr/bin/python
# -*- coding: UTF-8 -*-
from subprocess import Popen, PIPE
import os

import json
os.chdir(os.path.dirname(__file__))
with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.loads(f.read())
    f.close()
Remote=conf["Remote"]
Upload=conf["Upload"]


def start_upload_move(dir,folder):
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
        command=f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Remote}:{Upload}/{folder}\"  --stats=5s --stats-one-line --stats-log-level NOTICE --log-file=\"rclone_upload.log\" "
        print(command)
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}/{folder}"
    else:
        command=f"rclone --config /config/rclone/rclone.conf move  \"{dir}\"  \"{Remote}:{Upload}\"  --stats=5s --stats-one-line --stats-log-level NOTICE --log-file=\"rclone_upload.log\" "
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}"


def start_upload(dir,folder):
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
        command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}\"  \"{Remote}:{Upload}/{folder}\"  --stats=5s --stats-one-line --stats-log-level NOTICE --log-file=\"rclone_upload.log\" "
        print(command)
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}/{folder}"
    else:
        command=f"rclone --config /config/rclone/rclone.conf copy  \"{dir}\"  \"{Remote}:{Upload}\"  --stats=5s --stats-one-line --stats-log-level NOTICE --log-file=\"rclone_upload.log\" "
        print(command)
        resultsCommond = Popen(command,stdout=PIPE,
                               stderr=PIPE,stdin=PIPE,shell=True)
        data = resultsCommond.stdout.read()
        return f"{Remote}:{Upload}"



if __name__ == '__main__':
    '''dir="D:\\BaiduNetdiskDownload\\xmind"
    start_upload(dir)'''
    print()