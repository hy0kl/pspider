#!/bin/env python
# -*- coding: utf-8 -*-

import time

time_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))

settings = {
    # qq new song list
    'qq-music': {
        'url': 'http://music.soso.com/portal/hit/sosoRank/new/hit_sosoRank_1.html',
        'iconv': 1,
        'log': './log/qq-music.%s.log' % time_str,
        'data_path': './data/qq-music.%s.txt' % time_str,
        'save': './work/qq-music.%s.html' % time_str,
        'retry': 5,

        # parser mark
        'block_start': '<div class="toplist_zone">',
        'block_end': '<div class="page">',
        'end_mark': '</span>',
        'song_mark': '<span class="song">',
        'singer_mark': '<span class="singer">',

        'head_flag': 0,
        'headers': {
            #'Host': 'music.soso.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://music.soso.com/',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    # the new song at qq music index
    'qq-index': {
        'url': 'http://music.soso.com/index.html',
        'iconv': 1,
        'log': './log/qq-index.%s.log' % time_str,
        'data_path': './data/qq-index.%s.txt' % time_str,
        'save': './work/qq-index.%s.html' % time_str,
        'retry': 5,

        # parser mark
        'block_start': '<div class="song_box toplist_new"',
        'block_end': '</button></a>',
        'end_mark': '</td>',
        'song_mark': '<td class="song">',
        'singer_mark': '<td class="singer">',

        'head_flag': 0,
        'headers': {
            #'Host': 'music.soso.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://music.soso.com/',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    # list baidu, new song top 100
    'list-baidu': {
        'url': 'http://list.mp3.baidu.com/top/top100.html',
        'iconv': 1,
        'log': './log/list-baidu.%s.log' % time_str,
        'data_path': './data/list-baidu.%s.txt' % time_str,
        'save': './work/list-baidu.%s.html' % time_str,
        'retry': 5,
        'callback': 'baidu_top',

        # parser mark
        'block_start': '<div class="rank-info">',
        'block_end': '<div class="module module-other',
        'end_mark': '</div>',
        'song_mark': '<div class="music-name">',
        'singer_mark': '<div class="singer">',

        'head_flag': 0,
        'headers': {
            #'Host': 'mp3.baidu.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://mp3.baidu.com/',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    # kuwo billboard
    'kuwo-billboard': {
        'url': 'http://yinyue.kuwo.cn/yy/billboard_index.htm',
        'iconv': 0, # html is utf-8
        'log': './log/kuwo-billboard.%s.log' % time_str,
        'data_path': './data/kuwo-billboard.%s.txt' % time_str,
        'save': './work/kuwo-billboard.%s.html' % time_str,
        'retry': 5,

        # parser mark
        'block_start': '<ul class="itemUl">',
        'block_end': '<input type="hidden" id="cat"',
        'end_mark': '</li>',
        'song_mark': '<li class="songName">',
        'singer_mark': '<li class="songer">',

        'head_flag': 0,
        'headers': {
            #'Host': 'yinyue.kuwo.cn',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.kuwo.cn/',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    # sogou
    'sogou-newtop': {
        'url': 'http://music.sogou.com/song/newtop_1.html',
        'iconv': 1, # html is gbk
        'log': './log/sogou-newtop.%s.log' % time_str,
        'data_path': './data/sogou-newtop.%s.txt' % time_str,
        'save': './work/sogou-newtop.%s.html' % time_str,
        'retry': 5,
        'callback': 'sogou_newtop',

        # parser mark
        'block_start': '<div id="mainwrap">',
        'block_end': '<div id="song_pagebar"',
        'end_mark': '</td>',
        'song_mark': '<td class="songname"',
        'singer_mark': '<td class="singger"',

        'head_flag': 0,
        'headers': {
            #'Host': 'music.sogou.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://music.sogou.com/',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    # 9sky-top
    '9sky-top': {
        'url': 'http://www.9sky.com/top/373.htm',
        'iconv': 1, # html is gbk
        'log': './log/9sky-top.%s.log' % time_str,
        'data_path': './data/9sky-top.%s.txt' % time_str,
        'save': './work/9sky-top.%s.html' % time_str,
        'retry': 5,
        #'callback': '9sky_top',

        # parser mark
        'block_start': '<div id="middle">',
        'block_end': 'var bottom_right_ad=false',
        'end_mark': '</div>',
        'song_mark': '<div class="middle_b3">',
        'singer_mark': '<div class="middle_b4">',

        'head_flag': 0,
        'headers': {
            #'Host': '9sky.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.9sky.com/',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    '1ting-song': {
        'url': 'http://www.1ting.com/song_n.html',
        'iconv': 0, # html is utf-8
        'log': './log/1ting-song.%s.log' % time_str,
        'data_path': './data/1ting-song.%s.txt' % time_str,
        'save': './work/1ting-song.%s.html' % time_str,
        'retry': 5,
        'callback': 'yting_top',

        # parser mark
        'block_start': '<ul id="list-0">',
        'block_end': '<p class="footlink">',
        'end_mark': ' -',
        'song_mark': 'title="',
        'singer_mark': ' ',

        'head_flag': 1,
        'headers': {
            #'Host': '1ting.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.1ting.com/',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'zh-CN,zh;q=0.8',
            #'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    #
    'kugou': {
        'url': 'http://www.kugou.com/yueku/html/musicrank/27/%s.html',
        'iconv': 0, # html is utf-8
        'log': './log/kugou.%s.log' % time_str,
        'data_path': './data/kugou.%s.txt' % time_str,
        'save': './work/kugou.%s.html' % time_str,
        'retry': 5,
        'callback': 'kugou',
        'pagination' : {'start': 1, 'end': 10, 'step': 1},

        # parser mark
        'simple_parse': 1,
        'block_start': '<ul id="ul">',
        'block_end': '<div id="public-footer">',
        'end_mark': '</li>',
        'song_mark': '<li>',
        'singer_mark': 'None',

        'head_flag': 1,
        'headers': {
            #'Host': 'kugou.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.kugou.com/',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'zh-CN,zh;q=0.8',
            #'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    # google music
    'google-music': {
        'url': 'http://www.google.cn/music/chartlisting?q=chinese_new_songs_cn&cat=song&start=%s&grouping=new-release_music&expanded_groupings=new-release_music',
        'iconv': 0, # html is utf-8
        'log': './log/google-music.%s.log' % time_str,
        'data_path': './data/google-music.%s.txt' % time_str,
        'save': './work/google-music.%s.html' % time_str,
        'retry': 5,
        #'callback': 'google',
        'pagination' : {'start': 0, 'end': 25, 'step': 25},

        # parser mark
        #'simple_parse': 0,
        'block_start': '<table id="song_list"',
        'block_end': '<div class="div-footer">',
        'end_mark': '</td>',
        'song_mark': '<td class="Title BottomBorder">',
        'singer_mark': '<td class="Artist BottomBorder">',

        'head_flag': 1,
        'headers': {
            #'Host': 'google.cn',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.google.cn/',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'zh-CN,zh;q=0.8',
            #'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },
}

special = {
    # xiami
    'xiami': {
        'first_layer': {
            'url': 'http://www.xiami.com/music/newalbum/type/all/ord/default/page/%s',
            'pagination' : {'start': 1, 'end': 4, 'step': 1},
            'start_mark': '<a id="showBlock"',
            'end_mark': 'div class="albumThread_list"',
            'callback': 'xiami_parse_url',
            #'callback': '',
        },
        'second_layer': {
            'start_mark': '<div id="album_rank"',
            'end_mark': '<div id="wall"',
            'callback': 'xiami_parse_detail',
        },
        'iconv': 0, # html is utf-8
        'log': './log/xiami.%s.log' % time_str,
        'data_path': './data/xiami.%s.txt' % time_str,  # dp_fp
        'save': './work/xiami.%s.html' % time_str,
        'title_link': './work/xiami.title-link.%s.txt' % time_str,
        'detail_data': './work/xiami.detail-data.%s.txt' % time_str,     # dd_fp
        'retry': 5,

        'head_flag': 0,
        'headers': {
            #'Host': 'xiami.com',
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.xiami.com/',
            #'Accept-Encoding': 'gzip,deflate,sdch',
            #'Accept-Language': 'zh-CN,zh;q=0.8',
            #'Accept-Charset': 'UTF-8,*;q=0.5',
            'Cookie': 'player_opencount=0; xiami_playlist_for_hao123=392059%2C1770764641%2C1770614593%2C1770714735%2C1770698677%2C1770829459%2C1770799928%2C1770828203%2C1770817009%2C1770519359%2C1769333110%2C1769275766%2C1770775994%2C176980%2C1770764730%2C1770821007%2C1770803528%2C1770700059%2C1770515731%2C1770817013%2C1770776664%2C8672%2C380307%2C1770714908%2C1770764711%2C1770783426%2C1770745554%2C1770786828%2C1770768310%2C1770770489%2C1770653173%2C1770825087%2C1770709745%2C1770665107%2C1770719126%2C1770757252%2C1770617135%2C1770707253%2C8674%2C1769802194%2C1770737583%2C1770779928%2C1770754047%2C1770714734%2C1770545005%2C1770138901%2C575%2C1770817010%2C; __gads=ID=d8f12e52ac16ed72:T=1332225422:S=ALNI_MYe91dHD_uw75mDZkj2Yj2iYMgvlQ; __XIAMI_SESSID=028f8ec54b325e6c12e965fa491e05dc; base_domain_8521f0afe9404fafbd73d063dd258df0=xiami.com; xnsetting_8521f0afe9404fafbd73d063dd258df0=%7B%22connectState%22%3A2%2C%22oneLineStorySetting%22%3A3%2C%22shortStorySetting%22%3A3%2C%22shareAuth%22%3Anull%7D; member_auth=uRDRyFTEX2WYd6a6lK6ZqBLMcQ4jWC0V2Ue5hEdZHV52Q%2B5akk0UuW%2BXpeXZyomnLZhYLFTO; t_sign_auth=0; index_logined_hotmusic_tab=1; music_tab=%2Fmusic%2Fnewalbum; __utma=251084815.1776831639.1331539086.1332313925.1332319368.4; __utmb=251084815.4.10.1332319368; __utmc=251084815; __utmz=251084815.1331539086.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); cnzz_a921634=12; sin921634=; rtime=2; ltime=1332319442322; cnzz_eid=76385987-1331535406-http%3A//www.google.com/url%3Fsa%3Dt%26rct%3Dj%26q%3D%26esrc%3Ds%26source%3Dweb%26cd%3D1%26c',
        },
    },
}

if '__main__' == __name__ :
    print settings
