"""
WSGI config for fengzhengBlog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wechat_huoyun.settings")

#from django.core.wsgi import get_wsgi_application
#application = get_wsgi_application()
#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
