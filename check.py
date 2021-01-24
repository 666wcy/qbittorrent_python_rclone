# -*- coding: UTF-8 -*-
import qbittorrentapi
import sqlite3
from rclone import *
from link import *
from mover import *
from qb import *
import telebot
import datetime
import os, sys, stat
import importlib
import io
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

os.chdir(os.path.dirname(__file__))
with open('/upload/config.json', 'r', encoding='utf-8') as f:
    conf = json.loads(f.read())
    f.close()
QB_host=conf["QB_host"]
QB_port=conf["QB_port"]
QB_username=conf["QB_username"]
QB_password=conf["QB_password"]
Telegram_bot_api=conf["Telegram_bot_api"]
Telegram_user_id=conf["Telegram_user_id"]
Rule_list=conf["Rule"]
Download_dir=conf["Download_dir"]


qbt_client = qbittorrentapi.Client(host=QB_host, port=QB_port, username=QB_username, password=QB_password)
try:
    qbt_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)



def send_telegram(upload_dir,upload_time,row):
    if Telegram_bot_api !="":
        Torrents_hash=row[8]
        Torrents_num=row[6]
        Torrents_content_dir=row[3]
        Torrents_name=row[0]
        Torrents_tag=row[2]
        Torrents_category=row[1]
        Torrents_root_dir=row[4]
        Torrents_save_dir=row[5]
        Torrents_size=row[7]
        m, s = divmod(int(upload_time), 60)
        h, m = divmod(m, 60)
        #print ("%02d时%02d分%02d秒" % (h, m, s))
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
              f"文件大小：`{Torrents_size}Bytes`\n" \
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
        #连接数据库，没有会自动创建文件，数据结构还是要上面定义
        '''    conn = sqlite3.connect("Info.db")
        c = conn.cursor()
        #首先删除表中所有数据
        c.execute("delete from INFO;")
        #添加数据
    
        conn.commit()'''
    else:
        return

def save_log(row):
    Torrents_hash=row[8]
    Torrents_num=row[6]
    Torrents_content_dir=row[3]
    Torrents_name=row[0]
    Torrents_tag=row[2]
    Torrents_category=row[1]
    Torrents_root_dir=row[4]
    Torrents_save_dir=row[5]
    Torrents_size=row[7]

    #print(f"python upload.py \"{Torrents_name}\" \"{Torrents_category}\" \"{Torrents_tag}\" \"{Torrents_content_dir}\" \"{Torrents_root_dir}\" \"{Torrents_save_dir}\" \"{Torrents_num}\" \"{Torrents_size}\" \"{Torrents_hash}\"")

    with open('upload.log','a',encoding='utf-8') as f:
        log = f"种子名称：{Torrents_name}\n" \
              f"种子类别：{Torrents_category}\n" \
              f"种子标签：{Torrents_tag}\n" \
              f"内容路径：{Torrents_content_dir}\n" \
              f"根目录：{Torrents_root_dir}\n" \
              f"保存路径：{Torrents_save_dir}\n" \
              f"文件数：{Torrents_num}\n" \
              f"文件大小：{Torrents_size}Bytes\n" \
              f"HASH:{Torrents_hash}\n\n"
        print(log)
        f.write(log)
        log=f"python upload.py \"{Torrents_name}\" \"{Torrents_category}\" \"{Torrents_tag}\" \"{Torrents_content_dir}\" \"{Torrents_root_dir}\" \"{Torrents_save_dir}\" \"{Torrents_num}\" \"{Torrents_size}\" \"{Torrents_hash}\""
        f.write(log)
    f.close()

def zhu():
    creat_db()
    conn = sqlite3.connect("Info.db")
    c =conn.cursor()
    ret = c.execute("select * from info")    #获取该表所有元素
    for row in ret:
        #print(row[8])
        Torrents_hash=row[8]
        Torrents_num=row[6]
        Torrents_content_dir=row[3]
        Torrents_name=row[0]
        Torrents_tag=row[2]
        Torrents_category=row[1]
        Upload_status=row[9]
        try:
            Torrents_info=qbt_client.torrents_info(torrent_hashes = Torrents_hash)[0]
            print(Torrents_info)
            #print(Torrents_info.name)
            Torrents_share_rate=Torrents_info.ratio
            #print(Torrents_share_rate)
            Torrents_time_active=Torrents_info.time_active
            #print(Torrents_time_active)

        except:
            print("该hash值无法找到种子")
            continue

        for  Rule in Rule_list:
            category= Rule["category"]
            share_rate=Rule["share_rate"]
            time=Rule["time"]
            tags=Rule["tags"]
            emby=Rule["emby"]
            delete=Rule["delete"]
            #print(Upload_status)
            if Torrents_category==category and int(Torrents_time_active)>= int(time) and float(Torrents_share_rate)>=float(share_rate) and Upload_status=="Waiting":
                #print("符合要求")
                sql=f"UPDATE Info SET Upload_status = 'Uploading' WHERE Torrents_hash = '{Torrents_hash}' "
                c.execute(sql)
                conn.commit()

                starttime = datetime.datetime.now()
                if  emby=="false" :
                    #print("直接调用rclone")
                    if int(Torrents_num)==1:
                        #print(Torrents_content_dir)


                        remote_dir=start_upload(Torrents_content_dir,"")  #单文件测试完成
                        save_log(row)
                        endtime = datetime.datetime.now()

                        sql=f"UPDATE Info SET Upload_status = 'Finished' WHERE Torrents_hash = '{Torrents_hash}' "
                        c.execute(sql)
                        conn.commit()

                        if delete=="true":
                            del_torrent(Torrents_hash)
                        send_telegram(remote_dir,str((endtime - starttime).seconds),row)
                        return
                    else:
                        #print(Torrents_content_dir)
                        #print(Download_dir)
                        temp_dir=str(Torrents_content_dir).replace(str(Download_dir),"")
                        #print(temp_dir)
                        #print(Torrents_content_dir,temp_dir)
                        remote_dir=start_upload(Torrents_content_dir,temp_dir)
                        save_log(row)
                        endtime = datetime.datetime.now()

                        sql=f"UPDATE Info SET Upload_status = 'Finished' WHERE Torrents_hash = '{Torrents_hash}' "
                        c.execute(sql)
                        conn.commit()

                        if delete=="true":
                            del_torrent(Torrents_hash)
                        send_telegram(remote_dir,str((endtime - starttime).seconds),row)
                        return

                elif emby=="true":
                    #print("emby后上传rclone")
                    if int(Torrents_num)==1:
                        #print("emby,单文件")
                        temp_dir=str(os.path.splitext(Torrents_name)[0]).replace(str(Download_dir),"")
                        #print(temp_dir)
                        to_dir=os.path.join(Download_dir,"temp", temp_dir)
                        #print(to_dir)

                        fu_folder=str(to_dir).replace(str(temp_dir),"")
                        #print(fu_folder)
                        #print(Torrents_content_dir,to_dir)
                        creat_link(Torrents_content_dir,to_dir)
                        rename_file(to_dir,int(Torrents_tag))

                        upload_dir=to_dir.replace(str(fu_folder),"")
                        #print(fu_folder,upload_dir)
                        remote_dir=start_upload_move(to_dir,upload_dir)

                        save_log(row)
                        os.system(f"rm -rf '{to_dir}'") #删除硬链接
                        endtime = datetime.datetime.now()

                        sql=f"UPDATE Info SET Upload_status = 'Finished' WHERE Torrents_hash = '{Torrents_hash}' "
                        c.execute(sql)
                        conn.commit()
                        if delete=="true":
                            del_torrent(Torrents_hash)

                        send_telegram(remote_dir,str((endtime - starttime).seconds),row)

                        return
                    else:
                        #print("emby,文件夹")
                        temp_dir=str(Torrents_content_dir).replace(str(Download_dir),"")
                        #print(temp_dir)
                        to_dir=os.path.join(Download_dir,"temp", temp_dir)
                        #print(to_dir)

                        fu_folder=str(to_dir).replace(str(Torrents_name),"")
                        #print(fu_folder)

                        creat_link(Torrents_content_dir,fu_folder)

                        start_rename(fu_folder,int(Torrents_tag))

                        upload_dir=temp_dir.replace(str(Torrents_name),"")
                        #print(fu_folder,upload_dir)
                        remote_dir=start_upload_move(fu_folder,upload_dir)
                        os.system(f"rm -rf '{fu_folder}'") #删除硬链接
                        save_log(row)
                        endtime = datetime.datetime.now()

                        sql=f"UPDATE Info SET Upload_status = 'Finished' WHERE Torrents_hash = '{Torrents_hash}' "
                        c.execute(sql)
                        conn.commit()
                        if delete=="true":
                            del_torrent(Torrents_hash)

                        send_telegram(remote_dir,str((endtime - starttime).seconds),row)
                        return


    conn.close()

if __name__ == '__main__':
    zhu()