#!/bin/bash
#exec &>>/var/log/work.log

./start_buy.sh &
./service0.sh &
./service1.sh &
./service2.sh &
./start_sell.sh

