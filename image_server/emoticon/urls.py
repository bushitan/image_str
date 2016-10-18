# -*- coding: utf-8 -*-

from django.conf.urls import url
from emoticon.views import *
urlpatterns = [
   url(r'resize/$', Resize.as_view()),
   # url(r'^api/img_str/$', API_ImgToStr_Temp.as_view()),
   # url(r'^api/img_str_data/$', API_ImgToStr_Data.as_view()),



]