#!/bin/bash

nohup  /usr/bin/python2.7 /logmysql/app.py &
nohup  /usr/bin/python2.7 /logmysql/rabbit_consumer.py
