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
            'Host': 'music.soso.com',
            'Connection': 'keep-alive',
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
            'Host': 'music.soso.com',
            'Connection': 'keep-alive',
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
            'Host': 'mp3.baidu.com',
            'Connection': 'keep-alive',
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
        #'callback': 'baidu_top',

        # parser mark
        'block_start': '<ul class="itemUl">',
        'block_end': '<input type="hidden" id="cat"',
        'end_mark': '</li>',
        'song_mark': '<li class="songName">',
        'singer_mark': '<li class="songer">',

        'head_flag': 0,
        'headers': {
            'Host': 'yinyue.kuwo.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer': 'http://www.kuwo.cn/',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            #'Cookie: '
        }
    },

    # pagination : {'start': 1, 'end': 10}
}

if '__main__' == __name__ :
    print settings
