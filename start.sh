#!/bin/bash


# 检查config配置文件，并创建
if [ ! -e "/config/qBittorrent/config/qBittorrent.conf" ] ;  then 
mkdir -p /config/qBittorrent/config/
cp /usr/local/qbittorrent/defaults/qBittorrent.conf  /config/qBittorrent/config/qBittorrent.conf
fi

# permissions
chown 0777 -R /config \
    /downloads

git clone https://github.com/666wcy/qbittorrent_python_rclone
mkdir /upload/
mv /qbittorrent_heroku/upload/* /upload/
chmod 0777 /upload/ -R
rm -rf /qbittorrent_heroku


nohup yes "" | qbittorrent-nox --webui-port=$PORT  --profile=/config  &
python3 /upload/config.py
python3 /upload/dingshi.py