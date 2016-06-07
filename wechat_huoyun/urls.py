"""wechat_huoyun URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from wechat.Urls.auth_urls import auth_partterns
from wechat.views import *
from wechat_huoyun import settings
import os

urlpatterns = [
    url(r'^static/wechat/js/(?P<path>.*)$', 'django.views.static.serve'),
    url(r'^static/wechat/css/(?P<path>.*)$', 'django.views.static.serve'),
    url(r'^static/wechat/images/(?P<path>.*)$', 'django.views.static.serve'),
    url(r'^static/wechat/upload/(?P<path>.*)$', 'django.views.static.serve'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wechat/', include(auth_partterns)),
    url(r'^login.html/', index),
]
    # if settings.DEBUG:
    #     url( r'^css/(?P<path>.*)$', 'django.views.static.serve',
    #             { 'document_root': ROOT+'/css' }
    #     ),
    #     url( r'^js/(?P<path>.*)$', 'django.views.static.serve',
    #             { 'document_root': ROOT+'/js' }
    #     ),
    #     url( r'^images/(?P<path>.*)$', 'django.views.static.serve',
    #             { 'document_root': ROOT+'/images' }
    #     ),
    #     url( r'^ueEditor/(?P<path>.*)$', 'django.views.static.serve',
    #             { 'document_root': ROOT+'/ueEditor' }
    #     ),
# if settings.DEBUG:
#     urlpatterns += [
#     url(r'^static/wechat/js/(?P<path>.*)$', 'django.views.static.serve'),
#     url(r'^static/wechat/css/(?P<path>.*)$', 'django.views.static.serve'),
#     url(r'^static/wechat/images/(?P<path>.*)$', 'django.views.static.serve)',
#     url(r'^static/wechat/upload/(?P<path>.*)$', 'django.views.static.serve)',
    # ({'document_root': os.path.join(settings.SITE_ROOT,'media')},name="media"),
    # ]