#!/bin/sh
# author: hy0kle@gmail.com
# use shilt + 5, ^_*
# parse data, find really new song by shell.

#set -x

Usage="$0 <runtype:start|stop|parse>"
if [ $# -lt 1 ];then
    echo "$Usage"
    exit 1
fi
runtype=$1

if [ "$runtype" != "start" ] && [ "$runtype" != "stop" ] && [ "parse" != "$runtype" ];
then
    echo "$Usage"
    exit 1
fi

# init global var, need, necessarily!!!
###{
DEBUG_FLAG=1
SEND_MAIL=1
mail_list="hy0kle@gmail.com" # need, necessarily!!!
host_name=$(hostname)
start_time=$(date +"%Y-%m-%d:%H:%M:%S")

# modules
modules="qq-music qq-index list-baidu kuwo-billboard sogou-newtop 9sky-top 1ting-song"

# change evn for your system
py=python

# check env diretory
evn_dir="log data  work"
###}

for dir in $evn_dir
do
    if [ -d $dir ]
    then
        echo "'$dir' diretory is exists."
        # delete old file for space, befor 30 days.
        find "$dir" -type f -mtime +30 -exec rm {} \;
    else
        echo "'$dir' is NOT exists, create it ..."
        mkdir -p $dir 
    fi  
done

# global functions {
work_pids=""
function get_work_pids()
{
    work_pids=$(ps aux | grep spider.py | grep -v grep | awk '{print $2}' | xargs)
}

function debug()
{
    if ((! DEBUG_FLAG))
    then
        return 0
    fi

    argc=$#
    if ((0 == argc))
    then
        return 0
    fi

    msg="$1"
    echo "$msg"

    if ((argc > 1))
    then
        exit 0
    fi
}
# } end functions

if ((DEBUG_FLAG))
then
#{

# start process
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

# stop process
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
new_song_back="data/new-song.${today_str}.txt"
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
> $today
for module in $modules
do
    spider_file="data/${module}.${today_str}.txt"
    if [ -f $spider_file ]; then
        cat $spider_file >> $today
    else
        echo "$spider_file is NOT exists"
    fi
done

today_num=$(wc -l $today | awk '{print $1}')
if ((! (today_num > 0)))
then
    mail_title="[Warning][$host_name][spider.py] get data error, at $today_str"
    # need send mail to give notice.
    echo "$today is empty, no spider data, please check it out." | mail -s "${mail_title}" "${mail_list}"
    debug "send mail: Warning"

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
cp "$new_song" "$new_song_back"

end_time=$(date +"%Y-%m-%d:%H:%M:%S")

# send mail logic.
if ((SEND_MAIL))
then
    mail_info="log/mail.info"
    > "$mail_info"
    new_song_num=$(wc -l "$new_song" | awk '{print $1}')
    mail_tile="[Statistics][$host_name]Spider for new song $today_str"

    echo "Process start at $start_time,  Completed at $end_time." >> "$mail_info"
    echo "Find $new_song_num new song tilte." >> "$mail_info"
    if ((new_song_num))
    then
        echo "-----New song title-----" >> "$mail_info"
        cat "$new_song" >> "$mail_info"
        echo "-----END-----" >> "$mail_info"
    else
        echo "May be something is wrong, pleash check it out..." >> "$mail_info"
    fi
    echo "---" >> "$mail_info"
    echo "By hy0kle@gmail.com" >> "$mail_info"

    cat "$mail_info" | mail -s "${mail_title}" "${mail_list}"
    debug "send mail: Statistics"
fi

echo "Completed."

exit 0
