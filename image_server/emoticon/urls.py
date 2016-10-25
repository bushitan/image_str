# -*- coding: utf-8 -*-

from django.conf.urls import url
from emoticon.views import *
urlpatterns = [
   url(r'^upload/$', Upload.as_view()),
   url(r'^identify/$', Identify.as_view()),
   url(r'^join/$', Join.as_view()),
   url(r'^resize/$', Resize.as_view()),
   url(r'^watermark/$', Watermark.as_view()),
]