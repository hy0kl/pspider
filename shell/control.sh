#!/bin/env bash

#set -x

Usage="$0 <runtype:start|stop>"
if [ $# -lt 1 ];then
    echo "$Usage"
    exit 1
fi
runtype=$1

if [ "$runtype" != "start" ] && [ "$runtype" != "stop" ]; then
    echo "$Usage"
    exit 1
fi

# modules
modules="qq-music qq-index list-baidu kuwo-billboard sogou-newtop 9sky-top 1ting-song"

py=python

# check env diretory
evn_dir="log data  work"
for dir in $evn_dir
do
    if [ -d $dir ]
    then
        echo "'$dir' diretory is exists."
    else
        echo "'$dir' is NOT exists, create it ..."
        mkdir -p $dir 
    fi  
done

if [ "start" == $runtype ]; then
    work_pids=$(ps aux | grep spider.py | grep -v grep | awk '{print $2}' | xargs)
    if [ "$work_pids" == "" ]; then
        echo "It is no process working, so let it start to work."
    else
        echo "It has process working now, please stop it before start it."
        exit -1
    fi

    for module in $modules
    do
        $py spider.py $module &
        echo "Start spider process for $module ..."
    done
fi

if [ "stop" == $runtype ]; then
   echo "Stop process, please wait a moment. :)" 

   kill_pids=`ps aux | grep spider.py | grep -v grep | awk '{print $2}' | xargs`

   #no process need to quit
   if [ "$kill_pids" == "" ]; then
       echo "No process need to quit..."
       exit 0
   fi

   kill -s SIGKILL $kill_pids
   echo "kill SIGKILL: $kill_pids"
   exit 0
fi

exit 0
