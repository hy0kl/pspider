#!/bin/sh
# use shilt + 5, ^_*

#set -x

Usage="$0 <runtype:start|stop|parse>"
if [ $# -lt 1 ];then
    echo "$Usage"
    exit 1
fi
runtype=$1

if [ "$runtype" != "start" ] && [ "$runtype" != "stop" && "parse" != "$runtype" ];
then
    echo "$Usage"
    exit 1
fi

# modules
modules="qq-music qq-index list-baidu kuwo-billboard sogou-newtop 9sky-top 1ting-song"

# change evn for your system
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

work_pids=""
function get_work_pids()
{
    work_pids=$(ps aux | grep spider.py | grep -v grep | awk '{print $2}' | xargs)
}

if [ 0 == 1 ]; then
#{

work_flag=0
if [ "start" == "$runtype" ]; then
    #work_pids=$(ps aux | grep spider.py | grep -v grep | awk '{print $2}' | xargs)
    get_work_pids
    if [ "$work_pids" == "" ]; then
        echo "It is no process working, so let it start to work."
    else
        echo "It has process working now, please stop it before start it."
        exit -1
    fi

    for module in $modules
    do
        #$py spider.py $module &
        echo "Start spider process for $module ..."
    done

    work_flag=1
fi

if [ "stop" == "$runtype" ]; then
    echo "Stop process, please wait a moment. :)"

    get_work_pids
    kill_pids=$work_pids

    #no process need to quit
    if [ "$kill_pids" == "" ]; then
       echo "No process need to quit..."
       exit 0
    fi

    kill -s SIGKILL $kill_pids
    echo "kill SIGKILL: $kill_pids"
    exit 0
fi

if [ "parse" == "$runtype" ]; then
    work_flag=1
fi

if ((1 != work_flag))
then
    echo "It is NO work, pleash check out it."
    exit -1
fi
#} debug
fi

#####
# find really new song.
today_str=$(date +"%Y-%m-%d")
history="data/history"
today="work/today"
new_song="data/new-song.txt"
new_song_gbk="data/new-song.gbk.txt"
merge_data="work/merge.txt"

# sleep for spider, give time to fetch and parse
i=0
get_work_pids
pids=$(echo $work_pids | awk '{print length($0)}')
while ((pids > 0))
do
    i=$((i + 1))
    echo "sleep for $i"
    sleep $i

    if ((i > 16))
    then
        echo "Something is wrong..."
        exit -2
    fi

    get_work_pids
    pids=$(echo $work_pids | awk '{print length($0)}')
done

# merge all new data.
#> $today
for module in $modules
do
    spider_file="data/${module}.${today_str}.txt"
    if [ -f $spider_file ]; then
        cat $spider_file >> $today
    else
        echo "$spider_file is NOT exists"
    fi
done

if [ ! -f $today ]; then
    echo "$today is NOT exists, no spider data, please check it out."
    exit -3
fi

if [ ! -f $history ]; then
    cat "$today" | sort -uf > "$history"
fi

cat "$today" "$history" | sort -uf > "$merge_data"
diff -ru "$history" "$merge_data" | awk '
    BEGIN
    {
        i = 0;
    }
    {
        if (i > 2 && length($0))
        {
            char = substr($0, 1, 1);
            if ("+" == char)
            {
                line = substr($0, 2, length($0));
                print line;
            }
        }
        i++
    }' > "$new_song"

# cycle for next day
cat "$new_song" "$history" | sort -uf > "$history"

# create gbk version for some system.
iconv -c -f "utf-8" -t "gbk" "$new_song" -o "$new_song_gbk"

# send mail logic.

echo "Completed."


exit 0
