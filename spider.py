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
import time
import re
import HTMLParser
import urllib2

import settings as gconfig
import tools
import SpecialSpider

def callback(obj, fun):
#{
    '''
    factory method.
    '''
    callback = {
        'baidu_top': 'baidu_top',
        'kugou':     'kugou_parse',
        'top_cn':    'top_cn',
        'google':    'google_music',
        'sogou_newtop' : 'sogou_newtop',
        'yting_top': 'yting_top'
    }

    if fun in callback :
        call_fun = callback[fun]
        handle = getattr(tools, call_fun)

        # debug
        #tools.debug(handle, 1)
        return handle(obj)
    else :
        return obj
#}

if '__main__' != __name__ :
    exit(0)

# set encode is utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

argc = len(sys.argv)
if not (argc > 1) :
    print 'Need more arguments.'
    exit(0)

argv = sys.argv[1]
module = argv
parser = HTMLParser.HTMLParser()

if not ((argv in gconfig.settings) or (argv in gconfig.special)) :
    print 'Wrong configuration for:[%s].' % argv
    exit(0)
# init logger
logger = tools.create_logger(module)
logger.info('Beginning for %s' % module)

### special site logic {
if argv in gconfig.special :
    sp = SpecialSpider.SpecialSpider()
    sp.spider(module, gconfig.special, logger, parser)

    logger.info('The [%s] process is completed.' % module)
    exit(0)
### end }

conf = gconfig.settings[module]

try:
    f = open(conf['data_path'], 'w', 0)
except (IOError), e :
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
            back_f = open(conf['save'], 'a', 0)
            back_f.write(content)
            logger.info('backup success.')

            back_f.close()
        except Exception, e :
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
        song   = ''
        singer = ''
        if 'simple_parse' in conf and conf['simple_parse'] :
            start_index = sub_content.index(song_mark)
            sub_content = sub_content[start_index + len(song_mark): ]
            end_index   = sub_content.index(end_mark)
            html        = sub_content[0: end_index]

            song_singer = callback(html, conf['callback'])
            #tools.debug(song_singer, 1)

            song   = song_singer['song']
            singer = song_singer['singer']

            sub_content = sub_content[end_index + len(end_mark): ]
        else :
            #print sub_content
            #{
            start_index = sub_content.index(song_mark)
            sub_content = sub_content[start_index + len(song_mark): ]
            end_index   = sub_content.index(end_mark)
            song_data   = sub_content[0: end_index]
            #song = parser.unescape(song)
            #song = decode_html(song)
            #song = unescape(song)

            sub_content = sub_content[end_index + len(end_mark): ]

            start_index = sub_content.index(singer_mark)
            sub_content = sub_content[start_index + len(singer_mark): ]
            end_index   = sub_content.index(end_mark)
            singer_data = sub_content[0: end_index]

            #tools.debug(song_data)
            #tools.debug(singer_data, 1)
            if 'callback' in conf :
                #tools.debug(conf['callback'], 1)
                song   = callback(song_data, conf['callback'])
                singer = callback(singer_data, conf['callback'])
                #tools.debug(song)
                #tools.debug(singer, 1)
            else :
                song   = tools.strip_html_tag(song_data)
                singer = tools.strip_html_tag(singer_data)

            #singer = parser.unescape(singer)
            #singer = decode_html(singer)
            #singer = unescape(singer)

            sub_content = sub_content[end_index + len(end_mark): ]
            #}

        #tools.debug(song)
        #tools.debug(singer, 1)
        try:
            song   = parser.unescape(song)
            singer = parser.unescape(singer)

        except (UnicodeDecodeError, UnicodeEncodeError), e :
            logger.info('Parse data error. Iterate times:%d. [Exception]: %s' % (i, e))
            pass

        #print sys.getdefaultencoding()
        if len(song) and len(singer) :
            out_str = song + "\t" + singer + "\t" + module + "\n"
            f.write(out_str)
        else :
            logger.warn('It has empty data. song[%s], singer[%s]' % (song, singer))

        #tools.debug(song)
        #tools.debug(singer, 1)

        i += 1

    #} end while
#} end for

f.close()

logger.info('The [%s] process is completed.' % module)

