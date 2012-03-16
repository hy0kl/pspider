#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import urllib2
import re
import HTMLParser
import re
import settings as gconfig
import tools

def str_replace(html):
#{
    special_str = {
        '&#45;': '-',
        '&#32;': ' ',
    }

    for sp_str in special_str :
        html = html.replace(sp_str, special_str[sp_str])

    return html
#}

module = 'qq-music'

# init logger
logger = tools.create_logger(module)
logger.info('Beginning for %s' % module)

parser = HTMLParser.HTMLParser()
qq = gconfig.settings[module]
f  = open(qq['data_path'], 'w', 0)
#debug(qq, 0)

content = urllib2.urlopen(qq['url']).read()
if ('iconv' in qq) and qq['iconv'] :
    content = content.decode('gbk', 'ignore').encode('utf-8') 

special_str = '<div class="toplist_zone">'
end_str     = '<div class="page">'
sub_content = ''
if special_str in content :
    start_index = content.index(special_str)
    sub_content = content[start_index + len(special_str): ]
    end_index   = sub_content.index(end_str)
    sub_content = sub_content[0: end_index]
    #sub_content = re.sub(r'</?\w+[^>]*>',' ', sub_content)

###
end_mark    = '</span>'
song_mark   = '<span class="song">'
singer_mark = '<span class="singer">'
find_index  = 0

sub_content = str_replace(sub_content)
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
