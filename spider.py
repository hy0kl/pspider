#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
fetch title for new song, from qq music, kuwo, baidu, 9sky,
kugou, top100, sogou, 1ting and so on.

@author: hy0kle@gmail.com
@date: 2012.03
'''
import os
import sys
import urllib2
import re
import HTMLParser
import time

import settings as gconfig
import tools

argc = len(sys.argv)
if not (argc > 1) :
    print 'Need more arguments.'
    exit(0)

argv = sys.argv[1]
if not (argv in gconfig.settings) :
    print 'Wrong configuration for:[%s].' % argv
    exit(0)

module = argv

# init logger
logger = tools.create_logger(module)
logger.info('Beginning for %s' % module)

parser = HTMLParser.HTMLParser()
conf = gconfig.settings[module]

try:
    f = open(conf['data_path'], 'w', 0)
except IOError, e :
    logger.warn('Can NOT open file: %s. [Except]: %s' %
        (conf['data_path'], e))
    exit(-1)

contents = tools.get_html(module, conf, logger)

for content in contents :
#{
    #content = contains[i]

    if ('iconv' in conf) and conf['iconv'] :
        content = content.decode('gbk', 'ignore').encode('utf-8')
        logger.info('convert code success.')

    # backup
    if 'save' in conf :
        try:
            back_f = open(conf['save'], 'w+', 0)
            back_f.write(content)
            logger.info('backup success.')
        except e :
            logger.info('Can NOT save html page. [Except]: %s' % e)
            pass

    special_str = conf['block_start']
    end_str     = conf['block_end']
    sub_content = ''
    if special_str in content :
        start_index = content.index(special_str)
        sub_content = content[start_index + len(special_str): ]
        end_index   = sub_content.index(end_str)
        sub_content = sub_content[0: end_index]
        #sub_content = re.sub(r'</?\w+[^>]*>',' ', sub_content)

    ###
    end_mark    = conf['end_mark']
    song_mark   = conf['song_mark']
    singer_mark = conf['singer_mark']
    find_index  = 0

    sub_content = tools.str_replace(sub_content)
    i = 0
    while song_mark in sub_content :
    #{
        #print sub_content
        start_index = sub_content.index(song_mark)
        sub_content = sub_content[start_index + len(song_mark): ]
        end_index   = sub_content.index(end_mark)
        song_data   = sub_content[0: end_index]
        #song = parser.unescape(song)
        #song = decode_html(song)
        #song = unescape(song)

        sub_content = sub_content[end_index + len(end_mark): ]
        start_index = sub_content.index(singer_mark)
        end_index   = sub_content.index(end_mark)
        singer_data = sub_content[start_index + len(singer_mark): end_index]
        #print singer_data
        if 'callback' in conf :
            song   = tools.callback(song_data, conf['callback'])
            singer = tools.callback(singer_data, conf['callback'])
            #tools.debug(song)
            #tools.debug(singer, 1)
        else :
            song   = re.sub(r'</?\w+[^>]*>', '', song_data)
            singer = re.sub(r'</?\w+[^>]*>', '', singer_data)
        #singer = parser.unescape(singer)
        #singer = decode_html(singer)
        #singer = unescape(singer)

        sub_content = sub_content[end_index + len(end_mark): ]

        try:
            song   = parser.unescape(song)
            singer = parser.unescape(singer)

            out_str = song + "\t" + singer + "\n"
            f.write(out_str)
        except (UnicodeDecodeError, UnicodeEncodeError, e) :
            logger.info('Parse data error. Iterate times:%d. [Except]: %s' % (i, e))
            pass
        i += 1
    #} end while
#} end for

f.close()

logger.info('The [%s] process is completed.' % module)

