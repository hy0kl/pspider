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
import re
import logging
import time

import settings as gconfig
import tools
import proxy

if '__main__' == __name__ :
    # diff module

    # import module
    import fetch_qq_music 
