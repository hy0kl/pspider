#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
tools for spider
'''

import re
import time
import logging

def debug(msg, exit_flag = 0) :
    print msg
    if exit_flag :
        exit(0)

def decode_html(string):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent))
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp)
            else:
                return match.group()

    return entity_re.subn(substitute_entity, string)[0]

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def create_logger(module):
    from settings import settings as gconfig
    if not (module in gconfig) :
        print 'wrong configuration.'
        exit(-1)

    config = gconfig[module]

    logger = logging.getLogger(module)
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(config['log'])
    fh.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(fh)

    logger.info('Init logger for %s' % module)

    return logger

#---function---
def str_replace(html):
#{
    special_str = {
        '&#45;': '-',
        '&#32;': ' ',
        '\n': '',
        '\r': '',
    }

    for sp_str in special_str :
        html = html.replace(sp_str, special_str[sp_str])

    return html
#}

# the html use ellipsis, so shule use callback
def baidu_top(html):
#{
    if '...' in html :
        find = 'title='
        if find in html :
            f_index  = html.find(find)
            f_char   = html[f_index + len(find)]
            sub_html = html[f_index + len(find) + 1: ]
            f_index  = sub_html.find(f_char)
            sub_html = sub_html[0: f_index]

            html = sub_html
    else :
        html =  re.sub(r'</?\w+[^>]*>', '', html)

    return html
#}

def callback(obj, callback_fun):
#{
    callback = {
        'baidu_top': 'baidu_top'
    }

    if 'baidu_top' in callback :
        return callback[callback_fun](obj)
    else :
        return obj
#}

def get_html(module, conf, logger):
#{
    contents = []

    index = 0
    start = 0
    end   = 0
    url   = conf['url']
    pagination_flag = 0

    if 'pagination' in conf :
        pagination_flag = 1
        pager = conf['pagination']
        start = pager['start']
        end   = pager['end']

    while start <= end :
    #{
        retry = 0

        if pagination_flag :
            url = url % start

        # create request
        req = urllib2.Request(url)
        headers = conf['headers']
        for key, value in headers :
            req.add_header(key, value)

        while retry < conf['retry'] :
            try:
                if 'head_flag' in conf and conf['head_flag'] :
                    contents[index] = urllib2.urlopen(req).read()
                else:
                    contents[index] = urllib2.urlopen(url).read()
                break

            except:
                retry += 1
                logger.info('Open [%s] is wrong, try it again times: %d' % (conf['url'], retry))
                time.sleep(retry)

        logger.info('Download page success for: %s, url: %s' % (module, conf['url']))

        index += 1
        start += 1
    #}

    return contents
#}

if '__main__' == __name__ :
    print baidu_top('test....<a title="abc">a</a>')
