# -*- coding: utf-8 -*-

from django.conf.urls import url
from wx_app.views import *
urlpatterns = [

   url(r'^$', Index.as_view()),

   url(r'^upload/img/$', UploadImg.as_view()),
   url(r'^upload/wx_img/$', UploadWXImg.as_view()),
   url(r'^upload/video/$', UploadVideo.as_view()),


   # url(r'^editor/watermark/$', EditorWatermark.as_view()),
   # url(r'^editor/join/$', EditorJoin.as_view()),


   url(r'^picture/my/$', PictureMy.as_view()),
   url(r'^picture/hot/$', PictureHot.as_view()),


   url(r'^img/add/$', PictureAdd.as_view()),
   url(r'^img/query/$', PictureQuery.as_view()),
   url(r'^img/move/$', PictureMove.as_view()),
   url(r'^img/delete/$', PictureDelete.as_view()),


   url(r'^category/add/$', CategoryAdd.as_view()),
   url(r'^category/reset/$', CategoryReset.as_view()),
   url(r'^category/delete/$', CategoryDelete.as_view()),
   url(r'^category/query/$', CategoryQuery.as_view()),


   url(r'^user/login/$', UserLogin.as_view()),
   url(r'^user/add/$', UserAdd.as_view()),
   url(r'^user/reset/$', UserAdd.as_view()),
   url(r'^user/delete/$', UserAdd.as_view()),
   url(r'^user/query/$', UserAdd.as_view()),
   url(r'^user/identify/$', UserAdd.as_view()),

]