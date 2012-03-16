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

import settings as gconfig
import tools

module = 'qq-music'

# init logger
logger = tools.create_logger(module)
logger.info('Beginning for %s' % module)

parser = HTMLParser.HTMLParser()
conf = gconfig.settings[module]

try:
    f  = open(conf['data_path'], 'w', 0)
except IOError:
    logger.warn('Can NOT open file: %s' % conf['data_path'])
    exit(-1)

# create request
req = urllib2.Request(conf['url'])
headers = conf['headers']
for key in headers :
    req.add_header(key, headers[key])
#tools.debug(req, 1)

retry = 0
while retry < conf['retry'] :
    try:
        if 'head_flag' in conf and conf['head_flag'] :
            content = urllib2.urlopen(req).read()
        else:
            content = urllib2.urlopen(conf['url']).read()
        break
    except:
        retry += 1
        logger.info('Open [%s] is wrong, try it again times: %d' % (conf['url'], retry))
logger.info('Download page success for: %s, url: %s' % (module, conf['url']))

#exit(0)
if ('iconv' in conf) and conf['iconv'] :
    content = content.decode('gbk', 'ignore').encode('utf-8') 
    logger.info('convert code success.')

# backup
if 'save' in conf :
    try:
        back_f = open(conf['save'], 'w', 0)
        back_f.write(content)
        logger.info('backup success.')
    except:
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
while song_mark in sub_content :
#{
    #print sub_content
    start_index = sub_content.index(song_mark)
    sub_content = sub_content[start_index + len(song_mark): ]
    end_index   = sub_content.index(end_mark)
    song_data = sub_content[0: end_index]
    #print song_data
    song = re.sub(r'</?\w+[^>]*>', '', song_data)
    #song = parser.unescape(song)
    #song = decode_html(song)
    #song = unescape(song)

    sub_content = sub_content[end_index + len(end_mark): ]
    start_index = sub_content.index(singer_mark)
    end_index   = sub_content.index(end_mark)
    singer_data = sub_content[start_index + len(singer_mark): end_index]
    #print singer_data
    singer = re.sub(r'</?\w+[^>]*>', '', singer_data)
    #singer = parser.unescape(singer)
    #singer = decode_html(singer)
    #singer = unescape(singer)

    sub_content = sub_content[end_index + len(end_mark): ]

    try:
        song = parser.unescape(song)
        singer = parser.unescape(singer)
        
        out_str = song + "\t" + singer + "\n"
        try:
            f.write(out_str)
        except UnicodeEncodeError:
            pass
    except UnicodeDecodeError: 
        pass
#}

f.close()

logger.info('The [%s] process is completed.' % module)

