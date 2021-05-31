from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from check import *
import requests
import os
import json
import qbittorrentapi
import sys
os.chdir(os.path.dirname(__file__))



def new_clock():
    print("检查种子情况:%s"%datetime.datetime.now())
    sys.stdout.flush()
    zhu()


def wakeup():
    title=os.environ.get('title')
    with open('/upload/config.json', 'r', encoding='utf-8') as f:
        conf = json.loads(f.read())
        f.close()
    QB_host=conf["QB_host"]
    QB_port=conf["QB_port"]
    QB_username=conf["QB_username"]
    QB_password=conf["QB_password"]
    qbt_client = qbittorrentapi.Client(host=QB_host, port=QB_port, username=QB_username, password=QB_password)
    torrent_temp = qbt_client.torrents_info()

    if torrent_temp==[]:
        print("无种子任务，不保持唤醒")
        sys.stdout.flush()
    else:
        url=f"https://{title}.herokuapp.com/"
        print(requests.get(url=url))
        print("种子正在下载，保持唤醒")
        sys.stdout.flush()

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(wakeup, "interval", seconds=60)
    scheduler.add_job(new_clock, "interval", seconds=60)
    print("开启监控")
    sys.stdout.flush()
    scheduler.start()