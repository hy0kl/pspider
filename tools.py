#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
tools for spider
'''

import re
import time
import logging
import urllib2
import HTMLParser
import htmlentitydefs

def debug(msg, exit_flag = 0) :
    try:
        print msg
    except (UnicodeEncodeError), e:
        print e

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
    def convert(matchobj):
        text = matchobj.group(0)
        if text[:2] == "&#":
            # Numeric Character Reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # Character entities references
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # Return Unicode characters
    return re.sub("&#?\w+;", convert, text)

def create_logger(module):
    import settings as gconfs

    if (module in gconfs.settings) :
        gconfig = gconfs.settings
    elif (module in gconfs.special) :
        gconfig = gconfs.special
    else :
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
        '\t': '',
    }

    for sp_str in special_str :
        html = html.replace(sp_str, special_str[sp_str])

    return html
#}

def strip_html_tag(html):
#{
    '''
    strip html tag by re.
    '''

    html = re.sub(r'</?\w+[^>]*>', '', html)
    html = html.strip()
    space_html = html.split()
    html = ' '.join(space_html)
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

            html = sub_html.strip()
    else :
        html =  strip_html_tag(html)

    return html
#}

def sogou_newtop(html):
#{
    find = '>'
    if find in html:
        f_index= html.find(find)
        html = html[f_index + len(find): ]
        html = strip_html_tag(html)

    return html
#}

def yting_top(html):
#{
    find = '" t'
    if find in html:
        f_index = html.find(find)
        html = html[0: f_index]

    return html
#}

def kugou_parse(html):
#{
    res = {'song': '', 'singer': ''}

    html = strip_html_tag(html)
    html = re.sub(r'^\d*', '', html)
    res_tmp  = html.split(' - ')

    if 2 == len(res_tmp) :
        res['song']   = res_tmp[1]
        res['singer'] = res_tmp[0]

    return res
#}

def top_cn(html):
    pass

def google_music(html):
    pass

def get_html(module, conf, logger):
#{
    contents = []

    start = 0
    end   = 0
    step  = 1
    original_url   = conf['url']
    pagination_flag = 0

    if 'pagination' in conf :
        pagination_flag = 1
        pager = conf['pagination']
        start = pager['start']
        end   = pager['end']
        step  = pager['step']

    while start <= end :
    #{
        retry = 0

        if pagination_flag :
            url = original_url % start
        else :
            url = original_url

        # create request
        req = urllib2.Request(url)
        headers = conf['headers']
        for key in headers :
            req.add_header(key, headers[key])

        html = ''
        while retry < conf['retry'] :
            try:
                if 'head_flag' in conf and conf['head_flag'] :
                    html = urllib2.urlopen(req).read()
                else:
                    html = urllib2.urlopen(url).read()
                break

            except Exception, e:
                retry += 1
                logger.info('Open [%s] is wrong, try it again times: %d. [Exception]: %s' %
                    (url, retry, e))
                time.sleep(retry)

        contents.append(html)
        html_len = len(html)
        if html_len :
            logger.info('Download page success for: %s, url: %s' % (module, url))
        else :
            logger.info('The HTML source is empty, url: %s' % url)

        start += step
    #}

    return contents
#}

if '__main__' == __name__ :
    print baidu_top('test....<a title="abc">a</a>')
