# -*- coding: utf-8 -*-

from django.conf.urls import url
from grid.views import *
urlpatterns = [

   url(r'^img_str/$', ImgToStrView.as_view()),
   url(r'^wx_img_str/$', WXImgToStr.as_view()),

   url(r'^api/img_str/$', API_ImgToStr.as_view()),

]