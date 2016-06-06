# -*- coding: utf-8 -*-
__author__ = 'wangjingyao'
from django.conf.urls import patterns, include, url
from wechat.views import *

auth_partterns = patterns('',
  url(r'^$', WeChat),
  url(r'^create_menu/', create_menu),
  url(r'^add_MT/', add_MT),
  url(r'^get_MT/', get_MT),
  url(r'^addper_MT/', addper_MT),
  url(r'^getper_MT/', getper_MT),
  url(r'^get_totalMT/', get_totalMT),
  url(r'^get_listMT/', get_listMT),
)
