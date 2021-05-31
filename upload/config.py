# -*- coding: UTF-8 -*-
import json
import os
import qbittorrentapi
import sys
os.chdir(os.path.dirname(__file__))
QB_port=os.environ.get('PORT')


Username=os.environ.get('Username')
Password=os.environ.get('Password')

print(f"端口为{QB_port}")



def change():
    qbt_client = qbittorrentapi.Client(host=f'localhost:{QB_port}', username='admin', password='adminadmin')
# this are all the same attributes that are available as named in the
#  endpoints or the more pythonic names in Client (with or without 'app_' prepended)

    prefs = qbt_client.app.preferences
    prefs['web_ui_password'] = Password
    qbt_client.app.preferences = prefs
    prefs = qbt_client.app.preferences
    prefs['web_ui_username'] = Username
    qbt_client.app.preferences = prefs
    print(f"修改账号：{Username}\n修改密码为:{Password}\n")
    sys.stdout.flush()

def mkdir(path):
    # 引入模块
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        os.makedirs(path)
        print (path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False
try:
    mkdir("/config/rclone")
except:
    None
with open("/config/rclone/rclone.conf", "w") as f:
    
    f.close()

change()
with open("/upload/config.json", "r",encoding='utf-8-sig', errors='ignore') as jsonFile:
    data = json.load(jsonFile)
    jsonFile.close()

data["QB_port"] = QB_port
data["QB_username"]=Username
data["QB_password"]=Password



with open("/upload/config.json", "w") as jsonFile:
    json.dump(data, jsonFile,ensure_ascii=False)
    jsonFile.close()
