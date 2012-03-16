#!/bin/env python

settings = {
    'qq-music': {
        'url': 'http://music.soso.com/portal/hit/sosoRank/new/hit_sosoRank_1.html',
        'iconv': 1,
        'data_path': './data/qq-music.txt',
        'headers': {
            'Host: music.soso.com',
            'Connection: keep-alive',
            'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.79 Safari/535.11',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Referer: http://music.soso.com/',
            'Accept-Encoding: gzip,deflate,sdch',
            'Accept-Language: zh-CN,zh;q=0.8',
            'Accept-Charset: UTF-8,*;q=0.5',
            #'Cookie: '
        }
    }
}

if '__main__' == __name__ :
    print settings