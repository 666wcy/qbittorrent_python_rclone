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




if __name__ == '__main__':
    scheduler = BlockingScheduler()
    
    scheduler.add_job(new_clock, "interval", seconds=60)
    print("开启监控")
    sys.stdout.flush()
    scheduler.start()