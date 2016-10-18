#coding:utf-8
from django.views.decorators.csrf import csrf_exempt
import httplib, urllib,urllib2
from django.http import HttpResponse, Http404
from grid.models import *

from django.views.generic import View, TemplateView, ListView, DetailView
from grid.lib.str2img import Str2Img
from grid.lib.web import Web
from grid.lib.qi_niu import QiNiu

from emoticon.lib.magick import Magick

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



class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):

        # user = self.request.user
        # if not user.is_authenticated():
        #    kwargs['user_id'] = "none"
        # else:
        #    kwargs['user_id'] = user
        context = super(BaseMixin, self).get_context_data(**kwargs)
        return context

#
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
        _img_filedir = "emoticon/static/magick/upload/"
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

        if _type == 'gif' or _type =="GIF":


            print 'save_close:',datetime.datetime.now()
            _save_filedir = "emoticon/static/magick/download/"
            _save_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
            _save_style = "." + _type
            _save_filename = _save_name+_save_style
            _save_localpath = _save_filedir + _save_filename


            m = Magick(_save_localpath)
            m.Resize(_img_localpath)

            print 'resize:',datetime.datetime.now()
            return HttpResponse( "/static/magick/download/" + _save_filename)
        else :
            return HttpResponse( "/static/magick/upload/" + _img_filename)
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

