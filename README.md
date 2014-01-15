Name
====
python spider

Version
------
    0.3

Description
----------
    NOTICE: vi ~/.bashrc
    +export LANG=en_US.UTF-8
    . ~/.bashrc

    Fetch title for new song, from qq music, kuwo, baidu, 9sky, kugou, top100, sogou  and so on.

    Python 2.7.1+

Usage
-----
    #cd "root-path"
    ./shell/control.sh start

    crontab -e
    30 10 * * * cd /opt/fetch && ./shell/control.sh start >> log/crontab.log."$(date +\%Y-\%m-\%d.\%H.\%M)" 2>&1

History
------
    1. verison: 0.1 release, at 2012.03.20, please enjoy it.
    2. verison: 0.2 release, at 2012.03.23, add function to fetch new song from xiami.com.
    3. verison: 0.3 release, at 2012.06.19, sogou change html page, so change settings for it.
    4. It is stop, I am sorry, just study example.
