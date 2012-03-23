#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
fetch title for new song, from xiami.
It is special site, so...

@author: hy0kle@gmail.com
@date: 2012.03
'''
import os
import sys
import time
import re
import HTMLParser
import urllib2

import tools

class SpecialSpider :
    def spider(self, module, conf, logger, parser):
        self._module = module
        self._conf   = conf
        self._logger = logger
        self._parser = parser

        self.extract_url(module)
        self.parse_detail(module)
        return 0

    def extract_url(self, module):
    #{
        conf   = self._conf[module]
        module = self._module
        logger = self._logger

        layer_conf   = conf['first_layer']

        title_link = conf['title_link']
        try:
            fp = open(title_link, 'w', 0)
        except (IOError), e :
            logger.warn('Can NOT open file: %s. [Except]: %s' %
                (title_link, e))
            exit(-1)

        contents = self.get_html(module, conf, layer_conf, logger)
        start_mark = layer_conf['start_mark']
        end_mark   = layer_conf['end_mark']

        for content in contents:
        #{
            html_section = content
            if start_mark in content :
                start_index = content.find(start_mark)
                end_index   = content.find(end_mark)
                html_section= content[start_index + len(start_mark): end_index]

            handle = getattr(SpecialSpider(), layer_conf['callback'])
            handle(html_section, module, conf, fp, logger)
        #}

        fp.close()

        time.sleep(1)
        return 0
    #}

    def get_html(self, module, conf, layer_conf, logger):
    #{
        contents = []
        start = 0
        end   = 0
        step  = 1
        pagination_flag = 0
        original_url = layer_conf['url']

        if 'pagination' in layer_conf :
            pagination_flag = 1
            pager = layer_conf['pagination']
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
            #{
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
            #} end retry while

            if ('iconv' in conf) and conf['iconv'] :
                html = html.decode('gbk', 'ignore').encode('utf-8', 'ignore')
                logger.info('Need and Convert code success.')

            # backup
            if 'save' in conf :
                back_html = '<<<%s>>>\n%s\n' % (url, html)
                try:
                    back_f = open(conf['save'], 'a', 0)
                    back_f.write(back_html)
                    logger.info('Backup success.')
                    back_f.close()
                except Exception, e :
                    logger.info('Can NOT save html page. [Except]: %s' % e)
                    pass

            html_len = len(html)
            if html_len :
                contents.append(html)
                logger.info('Download page success for: %s, url: %s' % (module, url))
            else :
                logger.info('The HTML source is empty, url: %s' % url)


            start += step
        #}
        return contents
    #}

    def parse_detail(self, module):
    #{
        conf   = self._conf[module]
        module = self._module
        logger = self._logger

        logger.info('Start to parse detail info for %s.' % module)

        layer_conf   = conf['second_layer']

        title_link = conf['title_link']
        detail_data= conf['detail_data']
        data_path  = conf['data_path']
        try:
            tl_fp = open(title_link, 'r', 0)
            dd_fp = open(detail_data, 'w', 0)
            dp_fp = open(data_path, 'w', 0)
        except (IOError), e :
            logger.warn('Can NOT open file: %s. [Except]: %s' %
                (title_link, e))

        for line in tl_fp :
        #{
            line = line.replace('\n', '')
            info = line.split('\t')
            info_obj  = {
                'album': info[0],
                'singer': info[1],
                'url': info[2],
            }
            layer_conf['url'] = info_obj['url']
            #tools.debug(layer_conf, 1)

            contents = self.get_html(module, conf, layer_conf, logger)
            start_mark = layer_conf['start_mark']
            end_mark   = layer_conf['end_mark']

            for content in contents:
            #{
                html_section = content
                if start_mark in content :
                    start_index = content.find(start_mark)
                    end_index   = content.find(end_mark)
                    html_section= content[start_index + len(start_mark): end_index]

                handle = getattr(SpecialSpider(), layer_conf['callback'])
                fp_obj = {
                    'dd_fp': dd_fp,
                    'dp_fp': dp_fp,
                }
                handle(html_section, module, conf, info_obj, fp_obj, logger)
            #}


        #} end for read file

        logger.info('It is completed for %s.' % module)

        tl_fp.close()
        dd_fp.close()
        dp_fp.close()

        return 0
    #}

    def xiami_parse_url(self, html, module, conf, fp, logger):
    #{
        logger.info('Start parse url for %s' % module)

        start_tag = '<li>'
        end_tag   = '</li>'
        deep_url  = 'http://www.xiami.com%s'

        html = tools.str_replace(html)
        while start_tag in html:
        #{
            start_index = html.find(start_tag)
            end_index   = html.find(end_tag)

            sub_html = html[start_index + len(start_tag): end_index]
            #tools.debug(sub_html, 1)

            parse_info = {
                'album': '',
                'artist': '',
                'url': '',
                'year': ''
            }

            # parse deep page url
            url = '#'
            u_start = 'href="'
            u_end   = '"'
            if u_start in sub_html :
                u_s_index = sub_html.find(u_start)
                sub_html  = sub_html[u_s_index + len(u_start): ]
                u_e_index = sub_html.find(u_end)
                url       = sub_html[0: u_e_index]
                sub_html = sub_html[u_e_index + len(u_end): ]
            if '/' == url[0] :
                url = deep_url % url
            else :
                url = '/%s' % url
                url = deep_url % url
            parse_info['url'] = url

            # parse album name, singer and year
            parse = [
                {
                    'name': 'album',
                    'start': '<a class="song"',
                    'end': '</a>',
                },
                {
                    'name': 'singer',
                    'start': '<a class="singer"',
                    'end': '</a>',
                },
                {
                    'name': 'year',
                    'start': '<p class="year"',
                    'end': '</p>',
                },
            ]

            for obj in parse :
            #{
                name  = obj['name']
                start = obj['start']
                end   = obj['end']
                data   = ''

                start_len = len(start)
                end_len   = len(end)

                if start in sub_html :
                    s_index = sub_html.find(start)
                    sub_html  = sub_html[s_index: ]
                    e_index = sub_html.find(end)
                    tmp_html= sub_html[0: e_index + end_len]
                    data = tools.strip_html_tag(tmp_html)
                    sub_html = sub_html[e_index + end_len: ]
                parse_info[name] = data
            #}

            # album singer url year
            w_str = '%s\t%s\t%s\t%s\n' % (parse_info['album'],
                parse_info['singer'], parse_info['url'], parse_info['year'])
            #tools.debug(w_str, 1)
            try :
                fp.write(w_str)
            except :
                logger.warn('Write data fail for %s.' % module)

            html = html[end_index + len(end_tag): ]
        #} end while
        logger.info('parse url is completed for %s.' % module)

        return 0
    #} end function

    def xiami_parse_detail(self, html, module, conf, info_obj, fp_obj, logger):
    #{
        #tools.debug(html_section)
        #tools.debug(info_obj)
        #tools.debug(fp_obj, 1)
        parser = HTMLParser.HTMLParser()
        dp_fp  = fp_obj['dp_fp']
        dd_fp  = fp_obj['dd_fp']

        url = info_obj['url']
        logger.info('Start parse url for %s, url: %s' % (module, url))
        #tools.debug(url)

        html = tools.str_replace(html)
        detail_data = {
            'url': url,
            'album': info_obj['album'],
            'artist': '',
            'language': '',
            'company': '',
            'publish_time': '',
            'album_type': '',
            'album_intro': '',
        }
        start = '<td valign="top"'
        end   = '</td>'
        start_len = len(start)
        end_len   = len(end)

        parse = ['artist', 'language', 'company', 'publish_time', 'album_type']
        for tag in parse :
        #{
            if start not in html:
                break

            s_index = html.find(start)
            html    = html[s_index: ]
            e_index = html.find(end)
            sub_html= html[0: e_index + end_len]
            data    = tools.strip_html_tag(sub_html)
            #tools.debug(data)
            detail_data[tag] = data

            html = html[e_index + end_len: ]
        #} end for tag
        #tools.debug(detail_data, 1)

        # album intro
        start = '<div id="album_intro"'
        end   = '<div class="album_intro_toggle'
        start_len = len(start)
        end_len   = len(end)
        if start in html :
            s_index = html.find(start)
            e_index = html.find(end)
            sub_html= html[s_index: e_index]
            data    = tools.strip_html_tag(sub_html)
            #{
            try:
                data = parser.unescape(data)
            except (UnicodeDecodeError, UnicodeEncodeError), e :
                logger.info('Parse data error. [Exception]: %s' % (e))
            #}
            detail_data['album_intro'] = data

        # write album detail data
        a_str_lable = '[album]'
        # url album artist language company publish_time album_type album_intro
        a_str = '%s\n%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n[song]\n' % (a_str_lable,
            detail_data['url'], detail_data['album'], detail_data['artist'], detail_data['language'],
            detail_data['company'], detail_data['publish_time'], detail_data['album_type'], detail_data['album_intro'])

        try :
            dd_fp.write(a_str)
        except :
            logger.warn('Write detail info wrong for: %s' % url)
            pass

        # new song
        start = '<td class="song_name">'
        end   = '</td>'
        start_len = len(start)
        end_len   = len(end)
        while start in html:
        #{
            s_index = html.find(start)
            html = html[s_index: ]
            e_index = html.find(end)
            sub_html= html[0: e_index + end_len]
            song = tools.strip_html_tag(sub_html)
            #tools.debug(song)

            # song artist album
            a_str = '%s\t%s\t%s\n' % (song, detail_data['artist'], detail_data['album'])
            # song artist
            s_str = '%s\t%s\n' % (song, detail_data['artist'])
            if len(song) > 0 :
                try :
                    dd_fp.write(a_str)
                    dp_fp.write(s_str)
                except :
                    logger.warn('Can NOT wrong song data for: %s' % url)
            else :
                #tools.debug(url)
                #tools.debug(html)
                logger.warn('Parse song wrong for: %s' % url)

            html = html[e_index + end_len: ]
        #}

        #tools.debug(detail_data, 1)
        logger.info('Parse detail is completed for %s.' % url)

        time.sleep(1)
        return 0
    #}
