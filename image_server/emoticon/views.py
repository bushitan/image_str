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


class Upload(BaseMixin, ListView):
    template_name = 'upload.html'

    def get(self, request, *args, **kwargs):
        return super(Upload, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(Upload, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):

        _imgData = base64.b64decode(request.POST['img'])
        _type = request.POST['type']
        _up_path = FILE_PATH.Up(_type)
        print _up_path["local_path"]
        #图片保存本地
        file = open(_up_path["local_path"], "wb+")
        file.write(_imgData)
        file.flush()
        file.close()

        #上传七牛云
        _qiniu = QiNiu()

        if _qiniu.put("",_up_path["file_name"],_up_path["local_path"]) is True: #上传原图
        # if True:
             img_dict = {
                 "status": 1,
                 "img":SETTING.QINIU_HOST + _up_path["file_name"] + "?imageMogr2/thumbnail/170x170",#默认返回170x170的缩略图
             }
        else:
            img_dict = {
                 "status": -1 ,
                 "img":-1,
             }

        return HttpResponse(
            json.dumps(img_dict),
            content_type="application/json"
        )

class Identify(BaseMixin, ListView):
    def get_context_data(self, **kwargs):
        return super(Identify, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):

        _img_url = request.POST['img_url']
        req = urllib2.Request(_img_url)

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        response = opener.open(req)
        data = response.read()

        _save_filedir = BASE_DIR + "/emoticon/static/magick/download/"
        _save_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        # _save_style = "." + _type
        # _save_filename = _save_name+_save_style
        _save_localpath = _save_filedir + _save_name

        file = open(_save_localpath, "wb+")
        file.write(data)
        file.flush()
        file.close()

        _magick = Magick()
        img_dict = _magick.Identity(_img_url)

        return HttpResponse(
            json.dumps(img_dict),
            content_type="application/json"
        )


import datetime
class Resize(BaseMixin, ListView):
    template_name = 'resize.html'

    def get(self, request, *args, **kwargs):
        return super(Resize, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(Resize, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        print "post API_PC"

        print 'begin:',datetime.datetime.now()
        _tx = request.POST['img']
        _type = request.POST['type']
        _imgData = base64.b64decode(_tx)
        print 'post over:',datetime.datetime.now()


        #图片全部写入，只转gif
        _img_filedir = BASE_DIR + "/emoticon/static/magick/upload/"
        _img_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _img_style = "." + _type
        _img_filename = _img_name+_img_style
        _img_localpath = _img_filedir + _img_filename
        print 'save:',datetime.datetime.now()

        # print "_img_localpath:" + _img_localpath
        #写入图片
        file = open(_img_localpath, "wb+")
        file.write(_imgData)
        file.flush()
        file.close()

        #存储图片
        print 'save_close:',datetime.datetime.now()
        _save_filedir = BASE_DIR + "/emoticon/static/magick/download/"
        _save_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _save_style = "." + _type
        _save_filename = _save_name+_save_style
        _save_localpath = _save_filedir + _save_filename

        _magick = Magick(_save_localpath)

        if _type == 'gif' or _type =="GIF":
            print "in gif"
            _magick.Resize(_img_localpath)
            print 'resize:',datetime.datetime.now()
            # return HttpResponse( "/static/magick/download/" + _save_filename)
        #其他图片，只复制
        else :
            _magick.Copy(_img_localpath)

        # _magick.AddWatermark(_save_localpath)


        img_dict = _magick.Identity(_save_localpath)
        img_dict["yun_url"] = "/static/magick/download/" + _save_filename
        return HttpResponse(
            json.dumps(img_dict),
            content_type="application/json"
        )
            # return HttpResponse( "/static/magick/upload/" + _img_filename)
        # IMAGE_SERVER_HOST = 'http://120.27.97.33:91/'
        # url = IMAGE_SERVER_HOST + 'grid/api/img_str/'
        # data  = {  "img_url":IMAGE_SERVER_HOST + "static/art/img/"+_img_filename}

        # print url,data
        #
        # req = urllib2.Request(url)
        # data = urllib.urlencode(data)
        # #enable cookie
        # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
        # response = opener.open(req,data)
        # res = response.read()
        # print 'res:',res


import datetime
class Join(BaseMixin, ListView):
    template_name = 'join.html'

    def get(self, request, *args, **kwargs):
        return super(Join, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(Join, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):

        _img1_post = request.POST['img_first']
        _img2_post = request.POST['img_second']
        _type1 = request.POST['type_first']
        _type2 = request.POST['type_second']

        _imgData1 = base64.b64decode(_img1_post)
        _imgData2 = base64.b64decode(_img2_post)


        #图片全部写入，只转gif
        _img_filedir = BASE_DIR + "/emoticon/static/magick/upload/"

        _img1_name = "{}1".format(time.strftime('%Y%m%d%H%M%S'))
        _img1_style = "." + _type1
        _img1_filename = _img1_name+_img1_style
        _img1_localpath = _img_filedir + _img1_filename
        _img2_name = "{}2".format(time.strftime('%Y%m%d%H%M%S'))
        _img2_style = "." + _type2
        _img2_filename = _img2_name+_img2_style
        _img2_localpath = _img_filedir + _img2_filename

        _img_bg = BASE_DIR + "/emoticon/static/magick/resouces/black.jpg"
        #写入两张图片
        file = open(_img1_localpath, "wb+")
        file.write(_imgData1)
        file.flush()
        file.close()

        file = open(_img2_localpath, "wb+")
        file.write(_imgData2)
        file.flush()
        file.close()

        #拼接的图片为gif格式
        print 'save_close:',datetime.datetime.now()
        _save_filedir = BASE_DIR + "/emoticon/static/magick/download/"
        _save_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _save_style = ".gif"
        _save_filename = _save_name+_save_style
        _save_localpath = _save_filedir + _save_filename

        _magick = Magick(_save_localpath)
        _magick.Join([_img1_localpath,_img_bg,_img2_localpath])

        # _magick.AddWatermark(_save_localpath)

        img_dict = _magick.Identity(_save_localpath)
        img_dict["yun_url"] = "/static/magick/download/" + _save_filename
        return HttpResponse(
            json.dumps(img_dict),
            content_type="application/json"
        )


class Watermark(BaseMixin, ListView):
    template_name = 'watermark.html'

    def get(self, request, *args, **kwargs):
        return super(Watermark, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(Watermark, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        _tx = request.POST['img']
        _type = request.POST['type']
        _imgData = base64.b64decode(_tx)
        print 'post over:',datetime.datetime.now()

        #图片全部写入，只转gif
        _img_filedir = BASE_DIR + "/emoticon/static/magick/upload/"
        _img_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _img_style = "." + _type
        _img_filename = _img_name+_img_style
        _img_localpath = _img_filedir + _img_filename
        print 'save:',datetime.datetime.now()
        # print "_img_localpath:" + _img_localpath
        #写入图片
        file = open(_img_localpath, "wb+")
        file.write(_imgData)
        file.flush()
        file.close()

        #存储图片
        print 'save_close:',datetime.datetime.now()
        _save_filedir = BASE_DIR + "/emoticon/static/magick/download/"
        _save_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
        _save_style = "." + _type
        _save_filename = _save_name+_save_style
        _save_localpath = _save_filedir + _save_filename

        _magick = Magick(_save_localpath)
        _magick.AddWatermark(_img_localpath)

        img_dict = _magick.Identity(_save_localpath)
        img_dict["yun_url"] = "/static/magick/download/" + _save_filename
        return HttpResponse(
            json.dumps(img_dict),
            content_type="application/json"
        )

