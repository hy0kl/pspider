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
    # pagination : {'start': 1, 'end': 10, 'step': 1}
}

if '__main__' == __name__ :
    print settings
