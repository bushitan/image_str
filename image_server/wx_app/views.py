#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import httplib, urllib,urllib2
from django.http import HttpResponse, Http404
from grid.models import *

from django.views.generic import View, TemplateView, ListView, DetailView
from grid.lib.str2img import Str2Img
from grid.lib.web import Web
from emoticon.lib.qi_niu import QiNiu
from emoticon.lib.magick import Magick
from emoticon.lib.filepath import FilePath

import datetime
import time
import json
import logging
import os
import base64
from PIL import Image,ImageDraw,ImageFont
import sys
import image_server.settings as SETTING
from grid.lib.painter import Painter
# logger
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = FilePath(BASE_DIR)
class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):

        # user = self.request.user
        # if not user.is_authenticated():
        #    kwargs['user_id'] = "none"
        # else:
        #    kwargs['user_id'] = user
        context = super(BaseMixin, self).get_context_data(**kwargs)
        return context


# 11
class UploadImg(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _imgData = request.POST['imgData']
        _type = request.POST['imgType']
        # _imgDecode = base64.b64decode(_imgData)
        _dict = {
            "imgData":_imgData,
            "imgType":_type,
            "imgUrl":"http://127.0.0.1:8000/static/magick/download/3.gif"
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#22
class UploadVideo(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _videoData = request.POST['videoData']
        _dict = {
            "videoData":_videoData,
            "imgUrl":"http://127.0.0.1:8000/static/magick/download/5.gif"
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#33
class EditorWatermark(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _watermarkData = request.POST['watermarkData']
        # _imgDecode = base64.b64decode(_imgData)
        _dict = {
            "watermarkData":_watermarkData,
            "imgUrl":"http://127.0.0.1:8000/static/magick/download/watermark.gif"
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )
#44
class EditorJoin(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _imgFirstUrl = request.POST['imgFirstUrl']
        _imgSecondeUrl = request.POST['imgSecondeUrl']
        _dict = {
            "imgFirstUrl":_imgFirstUrl,
            "imgSecondeUrl":_imgSecondeUrl,
            "imgUrl":"http://127.0.0.1:8000/static/magick/download/5.gif"
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#55
class PictureMy(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _uId = request.POST['uId']
        _imgParentId = request.POST['imgParentId']
        _imgId = request.POST['imgId']
        _dict = {
            "uId":_uId,
            "imgParentId":_imgParentId,
            "imgId":_imgId,
            "imgUrlList":[
                "http://127.0.0.1:8000/static/magick/download/join.gif",
                "http://127.0.0.1:8000/static/magick/download/5gif",
            ]
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#66
class PictureHot(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _uId = request.POST['uId']
        _imgParentId = request.POST['imgParentId']
        _imgId = request.POST['imgId']
        _dict = {
            "uId":_uId,
            "imgParentId":_imgParentId,
            "imgId":_imgId,
            "imgUrlList":[
                "http://127.0.0.1:8000/static/magick/download/join.gif",
                "http://127.0.0.1:8000/static/magick/download/5gif",
            ]
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#77
class CategoryAdd(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _uId = request.POST['uId']
        _categoryId = request.POST['categoryId']
        _categoryParentId = request.POST['categoryParentId']
        _name = request.POST['name']
        _isPublic = request.POST['isPublic']
        _dict = {
            "uId":_uId,
            "categoryId":_categoryId,
            "categoryParentId":_categoryParentId,
            "name":_name,
            "isPublic":_isPublic,
            "isSuccess":"true",
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#88
class CategoryReset(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _uId = request.POST['uId']
        _categoryId = request.POST['categoryId']
        _categoryParentId = request.POST['categoryParentId']
        _name = request.POST['name']
        _isPublic = request.POST['isPublic']
        _dict = {
            "uId":_uId,
            "categoryId":_categoryId,
            "categoryParentId":_categoryParentId,
            "name":_name,
            "isPublic":_isPublic,
            "isSuccess":"true",
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#99
class CategoryDelete(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _uId = request.POST['uId']
        _categoryId = request.POST['categoryId']
        _dict = {
            "uId":_uId,
            "categoryId":_categoryId,
            "isSuccess":"true",
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )

#10
class CategoryQuery(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _uId = request.POST['uId']
        _categoryId = request.POST['categoryId']
        _dict = {
            "uId":_uId,
            "categoryId":_categoryId,
            "isSuccess":"true",
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )
#11
class UserAdd(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        _uuId = request.POST['uuId']
        _role = request.POST['role']
        _icon = request.POST['icon']
        _name = request.POST['name']
        _isManage = request.POST['isManage']
        _dict = {
            "uuId":_uuId,
            "role":_role,
            "icon":_icon,
            "name":_name,
            "isManage":_isManage,
            "isSuccess":"true",
        }
        return HttpResponse(
            json.dumps(_dict),
            content_type="application/json"
        )


