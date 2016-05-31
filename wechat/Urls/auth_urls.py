# -*- coding: utf-8 -*-
__author__ = 'wangjingyao'
from django.conf.urls import patterns, include, url
from wechat.views import *

auth_partterns = patterns('',
  url(r'^$', WeChat),
  url(r'^init_conf/', init_conf),
)
