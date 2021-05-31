#!/bin/bash
DIRECTORY="/upload/"	

if [ "`ls -A $DIRECTORY`" = "" ]; then
	git clone https://github.com/666wcy/qbittorrent_python_rclone
	mv  /qbittorrent_python_rclone/*   /upload
	rm -rf /qbittorrent_python_rclone/
	sudo chmod 777 /upload/ -R
	tail -f /dev/null
else
  echo "$DIRECTORY is not empty"
  tail -f /dev/null
fi		
