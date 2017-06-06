# -*- coding: utf-8 -*-

from django.conf.urls import url
from wx_app.views.views import *
from wx_app.views.user import *
from wx_app.views.magick import *
from wx_app.views.painter import *
from wx_app.views.blog import *
from wx_app.views.gather import *
from wx_app.views.v_qiniu import *

urlpatterns = [

   url(r'^$', Index.as_view()),

   url(r'^upload/img/$', UploadImg.as_view()),
   url(r'^upload/wx_img/$', UploadWXImg.as_view()),
   url(r'^upload/video/$', UploadVideo.as_view()),
   url(r'^upload/token/$', UploadToken.as_view()),

   # url(r'^editor/watermark/$', EditorWatermark.as_view()),
   # url(r'^editor/join/$', EditorJoin.as_view()),


   url(r'^picture/my/$', PictureMy.as_view()),
   url(r'^picture/hot/$', PictureHot.as_view()),



   url(r'^img/add/$', PictureAdd.as_view()),
   url(r'^img/query/$', PictureQuery.as_view()),
   url(r'^img/move/$', PictureMove.as_view()),
   url(r'^img/delete/$', PictureDelete.as_view()),
   url(r'^user/session/$', UserGetSession.as_view()),  #用户登录 ，这两个应该合在一起
   # url(r'^img/video2gif/$', Video2Gif.as_view()),
   # url(r'^img/video2gif/$', Video2Gif_NoUpload.as_view()),
   # url(r'^img/join/$', Join_NoUpload.as_view()),


   url(r'^img/movie/$', Movie.as_view()),


   url(r'^category/add/$', CategoryAdd.as_view()),
   url(r'^category/reset/$', CategoryReset.as_view()),
   url(r'^category/delete/$', CategoryDelete.as_view()),
   url(r'^category/query/$', CategoryQuery.as_view()),



   url(r'^tag/add/$', TagAdd.as_view()),
   url(r'^tag/query/$', TagQuery.as_view()),
   url(r'^tag/img_add/$', TagImgAdd.as_view()),
   url(r'^tag/img_query/$', TagImgQuery.as_view()),
   url(r'^tag/cache_clear/$', CacheClear.as_view()),
   url(r'^tag/random/$',  TagImgRandom.as_view()), #将后边的图片随机置顶

   url(r'^user/info/$', GetUserInfo.as_view()), #获取用户信息
   url(r'^user/login/$', UserLogin.as_view()),  #用户登录 ，这两个应该合在一起
   url(r'^user/back/$', AddUserBack.as_view()), #收集用户反馈信息


   url(r'^ad/title/$', AdTitle.as_view()),

   url(r'^img/video2gif/$', Video2Gif_NoUpload.as_view()),
   url(r'^img/join/$', Join_NoUpload.as_view()),


   url(r'^painter/start/$', Start.as_view()),
   url(r'^painter/continue/$', Continue.as_view()),
   url(r'^painter/snatch/$', Snatch.as_view()),
   url(r'^painter/theme_query/$', ThemeQuery.as_view()),
   url(r'^painter/step_query/$', StepQuery.as_view()),
   url(r'^painter/join_latest/$', JoinLatest.as_view()),
   url(r'^painter/color/$', Color.as_view()),


   url(r'^blog/article/list/$', EmojiArticleList.as_view()),
   url(r'^blog/article/$', EmojiBlog.as_view()),
   url(r'^blog/taobao/$', Taobao.as_view()),

   #七牛上传

   url(r'^qiniu/upload/$', QiNiuUpload.as_view()),

   #gather英雄帖
   url(r'^gather/get_user_info/$', GetUserInfo.as_view()),
   url(r'^gather/set_user_info/$', SetUserInfo.as_view()),

   url(r'^gather/get_master_info/$', GetMasterInfo.as_view()),#获取发帖人信息
   url(r'^gather/help_master/$', HelpMaster.as_view()),#获取发帖人信息

   url(r'^gather/create_master_qr/$', CreateMasterQR.as_view()),#生成小程序二维码


]