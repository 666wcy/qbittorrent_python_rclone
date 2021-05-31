#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os, sys, stat
import sqlite3
import json
import time
from rclone import *
from link import *
from mover import *
from qb import *
import telebot
import datetime
import shutil
from pathlib import Path
os.chdir(os.path.dirname(__file__))
print("开始上传")
sys.stdout.flush()
Torrents_name = sys.argv[1]         #名称

Torrents_category = sys.argv[2]     #类别
Torrents_tag = sys.argv[3]          #标签
Torrents_content_dir = sys.argv[4]  #内容路径
Torrents_root_dir = sys.argv[5]  #根路径
Torrents_save_dir = sys.argv[6]  #保存路径
Torrents_num = sys.argv[7]  #文件数
Torrents_size = sys.argv[8] #种子大小
Torrents_hash = sys.argv[9] #种子hash值
Torrents_category=str(Torrents_category).replace("temp ","")
Torrents_tag=str(Torrents_tag).replace("temp ","")

with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.loads(f.read())
    f.close()
Telegram_bot_api=conf["Telegram_bot_api"]
Telegram_user_id=conf["Telegram_user_id"]
Rule_list=conf["Rule"]
Download_dir=conf["Download_dir"]

def hum_convert(value):
    value=float(value)
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size

def send_telegram(upload_dir,upload_time):
    if Telegram_bot_api !="":
        print()
        m, s = divmod(int(upload_time), 60)
        h, m = divmod(m, 60)
        print ("%02d时%02d分%02d秒" % (h, m, s))
        if h !=0 :
            last_time="%d时%d分%d秒" % (h, m, s)
        elif h==0 and m!=0:
            last_time="%d分%d秒" % ( m, s)
        else:
            last_time="%d秒" % s
        bot = telebot.TeleBot(Telegram_bot_api)
        log = f"种子名称：`{Torrents_name}`\n" \
              f"种子类别：`{Torrents_category}`\n" \
              f"种子标签：`{Torrents_tag}`\n" \
              f"内容路径：`{Torrents_content_dir}`\n" \
              f"根目录：`{Torrents_root_dir}`\n" \
              f"保存路径：`{Torrents_save_dir}`\n" \
              f"文件数：`{Torrents_num}`\n" \
              f"文件大小：`{hum_convert(Torrents_size)}`\n" \
              f"HASH:`{Torrents_hash}`\n" \
              f"上传地址:`{upload_dir}`\n" \
              f"上传用时:`{last_time}`\n"
        bot.send_message(chat_id=Telegram_user_id,text=log,parse_mode='Markdown')

    else:
        return


def creat_db():
    #如果db文件不存在则创建
    if not os.path.exists("Info.db"):
        conn = sqlite3.connect("Info.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE INFO
                    (Torrents_name TEXT  NOT NULL,
                    Torrents_category TEXT  NOT NULL,
                    Torrents_tag TEXT  NOT NULL,
                    Torrents_content_dir TEXT  NOT NULL,
                    Torrents_root_dir TEXT  NOT NULL,
                    Torrents_save_dir TEXT  NOT NULL,
                    Torrents_num TEXT  NOT NULL,
                    Torrents_size TEXT  NOT NULL,
                    Torrents_hash  TEXT   NOT NULL,
                    Upload_status  TEXT   NOT NULL);''')
        conn.commit()
        conn.close()
        os.chmod("Info.db", stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        #连接数据库，没有会自动创建文件，数据结构还是要上面定义
        '''    conn = sqlite3.connect("Info.db")
        c = conn.cursor()
        #首先删除表中所有数据
        c.execute("delete from INFO;")
        #添加数据
    
        conn.commit()'''
    else:
        return

def save_log():
    print(f"种子名称：{Torrents_name}\n"
          f"种子类别：{Torrents_category}\n"
          f"种子标签：{Torrents_tag}\n"
          f"内容路径：{Torrents_content_dir}\n"
          f"根目录：{Torrents_root_dir}\n"
          f"保存路径：{Torrents_save_dir}\n"
          f"文件数：{Torrents_num}\n"
          f"文件大小：{hum_convert(Torrents_size)}\n"
          f"HASH:{Torrents_hash}\n")

    print(f"python upload.py \"{Torrents_name}\" \"{Torrents_category}\" \"{Torrents_tag}\" \"{Torrents_content_dir}\" \"{Torrents_root_dir}\" \"{Torrents_save_dir}\" \"{Torrents_num}\" \"{Torrents_size}\" \"{Torrents_hash}\"")

    with open('upload.log','a',encoding='utf-8') as f:
        log = f"种子名称：{Torrents_name}\n" \
              f"种子类别：{Torrents_category}\n" \
              f"种子标签：{Torrents_tag}\n" \
              f"内容路径：{Torrents_content_dir}\n" \
              f"根目录：{Torrents_root_dir}\n" \
              f"保存路径：{Torrents_save_dir}\n" \
              f"文件数：{Torrents_num}\n" \
              f"文件大小：{hum_convert(Torrents_size)}\n" \
              f"HASH:{Torrents_hash}\n\n"
        print(log)
        f.write(log)
        log=f"python upload.py \"{Torrents_name}\" \"{Torrents_category}\" \"{Torrents_tag}\" \"{Torrents_content_dir}\" \"{Torrents_root_dir}\" \"{Torrents_save_dir}\" \"{Torrents_num}\" \"{Torrents_size}\" \"{Torrents_hash}\""
        f.write(log)
    f.close()

def add_info():
    conn = sqlite3.connect("Info.db")
    c = conn.cursor()
    sql = "insert into INFO(Torrents_name,Torrents_category,Torrents_tag,Torrents_content_dir,Torrents_root_dir,Torrents_save_dir,Torrents_num,Torrents_size,Torrents_hash,Upload_status) values(?,?,?,?,?,?,?,?,?,?);"

    data = [Torrents_name,Torrents_category,Torrents_tag,Torrents_content_dir,Torrents_root_dir,Torrents_save_dir,Torrents_num,Torrents_size,Torrents_hash,"Waiting"]
    c.execute(sql, data)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    for  Rule in Rule_list:
        category= Rule["category"]
        share_rate=Rule["share_rate"]
        uptime=Rule["time"]
        tags=Rule["tags"]
        emby=Rule["emby"]
        delete=Rule["delete"]
        Remote_list=Rule["Remote"]
        Upload_list=Rule['Upload']
        if Torrents_category==category :
            print(category ,share_rate,time,tags,emby)
            sys.stdout.flush()
            if uptime=="0" and share_rate=="0" and emby=="false" :
                print("直接调用rclone")
                if int(Torrents_num)==1:
                    print(Torrents_content_dir)

                    for remote ,upload_lu in zip(Remote_list,Upload_list):
                        starttime = datetime.datetime.now()
                        remote_dir=start_upload(Torrents_content_dir,"",remote,upload_lu)  #单文件测试完成
                        save_log()
                        endtime = datetime.datetime.now()
                        send_telegram(remote_dir,str((endtime - starttime).seconds))

                    if delete=="true":
                        del_torrent(Torrents_hash)


                    break
                else:
                    print(Torrents_content_dir)
                    print(Download_dir)
                    temp_dir=str(Torrents_content_dir).replace(str(Download_dir),"")
                    print(temp_dir)
                    print(Torrents_content_dir,temp_dir)

                    for remote ,upload_lu in zip(Remote_list,Upload_list):
                        starttime = datetime.datetime.now()
                        remote_dir=start_upload(Torrents_content_dir,temp_dir,remote,upload_lu)  #单文件测试完成
                        save_log()
                        endtime = datetime.datetime.now()
                        send_telegram(remote_dir,str((endtime - starttime).seconds))

                    if delete=="true":
                        del_torrent(Torrents_hash)


                    break
            elif uptime=="0" and share_rate=="0" and emby=="true":
                print("emby后上传rclone")
                if int(Torrents_num)==1:
                    print("emby,单文件")
                    #temp_dir=str(os.path.splitext(Torrents_name)[0]).replace(str(Download_dir),"")
                    temp_dir=str(os.path.splitext(Torrents_content_dir)[0]).replace(str(Download_dir),"")
                    #temp_dir=str(Torrents_content_dir.replace(str(Download_dir),""))
                    print(temp_dir)

                    to_dir=os.path.join(Download_dir,"temp", temp_dir)
                    print(to_dir)

                    fu_folder=str(to_dir).replace(str(os.path.splitext(Torrents_name)[0]),"")
                    print(fu_folder)
                    print(Torrents_content_dir,to_dir)
                    my_file = Path(fu_folder)
                    while  my_file.is_dir():
                        time.sleep(10)
                        print("等待上传")
                        sys.stdout.flush()
                        #防止错误删除
                    print("文件夹不存在，不需要等待上传")
                    sys.stdout.flush()

                    creat_link(Torrents_content_dir,to_dir)

                    if "season_" in Torrents_category:
                        start_rename(fu_folder,int(str(Torrents_category).replace("season_","")))
                    else:
                        start_rename(fu_folder,int(Torrents_tag))


                    upload_dir=to_dir.replace(str(fu_folder),"")
                    print(fu_folder,upload_dir)
                    remote_folder=str(Torrents_save_dir).replace(Download_dir,"")
                    for remote ,upload_lu in zip(Remote_list,Upload_list):
                        starttime = datetime.datetime.now()

                        remote_dir=start_upload(fu_folder,remote_folder,remote,upload_lu)

                        save_log()
                        endtime = datetime.datetime.now()
                        send_telegram(remote_dir,str((endtime - starttime).seconds))


                    shutil.rmtree(fu_folder)
                    if delete=="true":
                        del_torrent(Torrents_hash)


                    break
                else:
                    print("emby,文件夹")
                    temp_dir=str(Torrents_content_dir).replace(str(Download_dir),"")
                    print(temp_dir)
                    to_dir=os.path.join(Download_dir,"temp", temp_dir)
                    print(to_dir)

                    fu_folder=str(to_dir).replace(str(Torrents_name),"")
                    print(fu_folder)

                    creat_link(Torrents_content_dir,fu_folder)

                    if "season_" in Torrents_category:
                        start_rename(fu_folder,int(str(Torrents_category).replace("season_","")))
                    else:
                        start_rename(fu_folder,int(Torrents_tag))

                    upload_dir=temp_dir.replace(str(Torrents_name),"")
                    print(fu_folder,upload_dir)

                    for remote ,upload_lu in zip(Remote_list,Upload_list):
                        starttime = datetime.datetime.now()
                        remote_dir=start_upload(fu_folder,upload_dir,remote,upload_lu)

                        save_log()
                        endtime = datetime.datetime.now()
                        send_telegram(remote_dir,str((endtime - starttime).seconds))

                    shutil.rmtree(fu_folder)
                    if delete=="true":
                        del_torrent(Torrents_hash)


                    break
            else:
                print("写入db用定时任务上传")
                creat_db()
                add_info()
                break