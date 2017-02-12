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
Log = Logger()


from wx_app.lib.login import Login
Login = Login()

from wx_app.lib.result import Result
Result = Result()

from wx_app.lib.web import DownFile

from wx_app.lib.filepath import CreateFileName  #创建文件名称
import  image_server.settings as SETTINGS
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
import random
import re
import json
from django.db import transaction #事务


import requests
BASE_URL = 'https://login.weixin.qq.com'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'

def get_QRuuid():
    url = '%s/jslogin' % BASE_URL
    params = {
        'appid' : 'wx782c26e4c19acffb',
        'fun'   : 'new', }
    headers = { 'User-Agent' : USER_AGENT }
    s = requests.Session()
    r = s.get(url, params=params, headers=headers)
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)";'
    data = re.search(regx, r.text)
    if data and data.group(1) == '200':
        uuid = data.group(2)
        return uuid
USER = {}


# class BaseMixin(object):
#     def get_context_data(self, *args, **kwargs):
#         kwargs['user_id'] = 1
#         print kwargs
#         context = super(BaseMixin, self).get_context_data(**kwargs)
#         return context


# class BotIndex(BaseMixin, ListView):
SUB_LIST = []
USER_REPLY = {}
class BotIndex(ListView):
    template_name = 'bot_index.html'
    qr_url = ""
    # init_file_name = 5

    def get(self, request, *args, **kwargs):

        #图片转像素，返回像素矩阵

        # _cmd = u"magick convert -colors 100 %s %s" % (img['color'],self.save_url,self.save_url)
        # _cmd = u'python H:\Code\Python\Git\image_str\image_server\wx_app\lib/robote/r_itchat.py '
        # _cmd = u'python H:\Code\Python\Git\image_str\image_server\wx_app\static/r_itchat.py '
        uuid = get_QRuuid()
        self.uuid = uuid
        self.qr_url = '%s/qrcode/%s' % (BASE_URL, uuid)
        # print "get"
        print 1234,request.GET.get("uuid", "")

        # _cmd = u'python H:\Code\Python\Git\wx_robot\wxBot-master\\test.py '
        # subprocess.check_output(_cmd, shell=True)

        _cmd = u'python H:\Code\Python\Git\image_str\image_server\wx_app\lib/robote/new_itchat.py  ' + uuid
        # _cmd = u'python H:\Code\Python\Git\image_str\image_server\wx_app\static/r_itchat.py '
        subprocess.Popen(_cmd, shell=True)
        # subproc = subprocess.Popen(_cmd,  stdin=subprocess.PIPE,shell=True)
        # SUB_LIST.append(subproc)

        return super(BotIndex, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context =super(BotIndex, self).get_context_data(**kwargs)
        context['qr_url'] = self.qr_url
        context['uuid'] = self.uuid
        return context
    def get_queryset(self):
        pass


    def post(self, request, *args, **kwargs):
        print "OK",requests
        _uuid = self.request.POST.get("uuid", "")
        print _uuid
        _reply = self.request.POST.get("reply", "")
        print _reply
        _reply_dict = json.loads(_reply)
        # print _reply_dict["1"]

        USER_REPLY[_uuid] = _reply_dict  #直接更改user_reply 的key
        # _key = request.POST['key']
        # print request.POST
        # _value = self.request.POST.get("value", "")
        key = request.POST['uuid']
        # is_login = request.POST['is_login']
        print key

        # _reply = {
        #     "key":_key,
        #     "value":_value
        # }
        # path = r"H:\Code\Python\Git\image_str\image_server\wx_app\static\storage.txt"
        # with open(path, "wb") as code:
        #     code.write(str(_reply))


        mydict = {}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )


class LoginCallback(ListView):
    def get(self, request, *args, **kwargs):
        uuid = request.GET.get("uuid", "")
        is_login =  request.GET.get("is_login", "")
        user_name =  request.GET.get("user_name", "")
        print 123,uuid,is_login,user_name
        mydict = {}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

class UpdateReply(ListView):
    def get(self, request, *args, **kwargs):
        _uuid = request.GET.get("uuid", "")
        return HttpResponse(
            json.dumps(USER_REPLY[_uuid]),
            content_type="application/json"
        )



















