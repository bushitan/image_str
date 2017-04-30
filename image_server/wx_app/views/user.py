#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import httplib, urllib,urllib2
from django.http import HttpResponse, Http404
from wx_app.models import *

from django.views.generic import View, TemplateView, ListView, DetailView
# from grid.lib.str2img import Str2Img
# from grid.lib.web import Web
from wx_app.lib.qi_niu import QiNiu
from wx_app.lib.magick import Magick
from wx_app.lib.filepath import FilePath
from wx_app.lib.logger import Logger
LoggerObj = Logger()

import datetime
import time
import json
import logging
import os
import base64
from PIL import Image,ImageDraw,ImageFont
import sys
import image_server.settings as SETTING
from PIL import Image

from grid.lib.painter import Painter
# logger
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = FilePath(BASE_DIR)
from moviepy.editor import *
import subprocess
from django.db import transaction #事务
from wx_app.lib.logger import Logger
Logger = Logger()
import  image_server.settings as SETTINGS

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):

        # user = self.request.user
        # if not user.is_authenticated():
        #    kwargs['user_id'] = "none"
        # else:
        #    kwargs['user_id'] = user
        context = super(BaseMixin, self).get_context_data(**kwargs)
        return context

class GetUserInfo(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            session = request.GET['session']
            # _uid =
             #user 不存在
            if  User.objects.filter( session = session).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )

            _uid = User.objects.get( session = session)
            # 1 用户名下的所有目录
            # 目录下包含的图片
            _default_category = Category.objects.get( user_id = _uid, is_default = 1)

            _user_info = {
                "default_category_id":_default_category.id
            }
            return HttpResponse(json.dumps({"status":"true","user_info":_user_info}),content_type="application/json")
            # print _list
            # _category_list = []
            # for c in _list:
            #     _category_list.append({
            #         "category_id":c.id,
            #         "name":c.name,
            #         "is_default":c.is_default,
            #         "hasImg":RelCategoryImg.objects.filter( category = c ).exists(),
            #     })

            # return HttpResponse(json.dumps({"status":"true","category_list":_category_list}),content_type="application/json")
        except Exception ,e:
            print e
            logger.error(e)
            LoggerObj.error(str(e),'',self.__class__.__name__)
            return HttpResponse(json.dumps({"status":"false","msg":u"查询用户信息出错" + str(e)}),content_type="application/json")


class AddUserBack(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        session = request.GET['session']
        _back = request.GET['back']


        if  User.objects.filter( session = session).exists() is False:
            _uid = None
        else:
            _uid = User.objects.get( session = session)
        _user_back = UserBack(
            user = _uid,
            back = _back
        )
        _user_back.save()
        return HttpResponse(json.dumps({"status":"true","msg":"感谢您提供的宝贵意见"}),content_type="application/json")