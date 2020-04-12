#!/bin/bash

PID0=`ps aux | awk '/auth.py/ && !/awk/ { print $2 }'`
echo "$PID0"
if [ "$PID0" ]
then
        echo "Process exists, lets kill it"
        kill $PID0
else
        echo "Process absent, moving to other process"
fi


PID1=`ps aux | awk '/app.py/ && !/awk/ { print $2 }'`
echo "$PID1"
if [ "$PID1" ]
then
        echo "Process exists, lets kill it"
        kill $PID1
else
        echo "Process absent, moving to other process"
fi

