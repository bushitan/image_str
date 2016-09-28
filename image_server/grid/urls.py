# -*- coding: utf-8 -*-

from django.conf.urls import url
from grid.views import *
urlpatterns = [

   # url(r'^img_str/$', ImgToStrView.as_view()),
   # url(r'^wx_img_str/$', WXImgToStr.as_view()),

   # url(r'^api/img_str/$', API_ImgToStr.as_view()),
   url(r'^api/pc/$', API_PC.as_view()),
   url(r'^api/img_str/$', API_ImgToStr_Temp.as_view()),
   url(r'^api/img_str_data/$', API_ImgToStr_Data.as_view()),


   url(r'^api/game/$', API_Game_ActiveCircle.as_view()),

   url(r'^api/gif/mix/$', API_GIF_Mix.as_view()),


   # url(r'^api/img_str_temp/$', API_ImgToStr_Temp.as_view()),

]