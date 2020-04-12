#!/bin/bash


while true
do

SERVICE0='heikin_ashi.py'

ps -ef | grep $SERVICE0 | grep -v grep
[ $?  -eq "0" ] && echo "$SERVICE0 process is running" || echo "$SERVICE0 process is not running, starting"; python /usr/local/bin/heikin_ashi.py

done
