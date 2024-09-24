#!/bin/bash
#service cron start;uvicorn main:app --host 0.0.0.0 --port 8080 --reload

#echo DB_IP=172.17.0.1 >> /etc/environment;
#echo LINE_TOKEN=$LINE_NOTI_PATH >> /etc/environment;
env >> /etc/environment;
service cron start;
uvicorn main:app --host 0.0.0.0 --port 8080 --reload;
