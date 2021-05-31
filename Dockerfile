FROM ubuntu


COPY root /
RUN apt-get update
RUN apt-get install sudo

RUN sudo apt-get update
RUN apt-get install wget -y
RUN apt-get install git -y

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN sudo apt-get install python3-distutils -y
RUN python3 get-pip.py
RUN pip3 install pyTelegramBotAPI
RUN pip3 install qbittorrent-api
RUN pip3 install apscheduler

RUN sudo chmod 777 /qbittorrent-nox
RUN mv /qbittorrent-nox /usr/bin/

RUN sudo chmod 777 /rclone
RUN mv /rclone /usr/bin/


CMD wget https://raw.githubusercontent.com/666wcy/qbittorrent_python_rclone/main/start.sh  && chmod 0777 start.sh && bash start.sh

