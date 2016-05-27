#! /bin/bash
nginx -s reload
killall -9 uwsgi
uwsgi --ini django_socker.ini
