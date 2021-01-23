#!/bin/bash
DIRECTORY="/upload/"	

if [ "`ls -A $DIRECTORY`" = "" ]; then
	git clone https://github.com/666wcy/qbittorrent_python_rclone
	mv  /upload/qbittorrent_python_rclone/*   /upload
	rm -rf /upload/qbittorrent_python_rclone/
	sudo chmod 777 /upload/ -R
else
  echo "$DIRECTORY is not empty"
fi		
