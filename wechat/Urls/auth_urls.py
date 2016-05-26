# -*- coding: utf-8 -*-
__author__ = 'wangjingyao'
from django.conf.urls import patterns, include, url
from wechat.views import WeChat

auth_partterns = patterns('',
  url(r'^$', WeChat),
)