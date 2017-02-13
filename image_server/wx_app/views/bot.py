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
USER_INFO = [{
    "user_info":{"id":"1", "user_name":""},
    "is_login":False,
    "uuid":"",
    "auto_reply":{"1":"123","2":"wqe"},
    "talk_data":"",
}]
def GetUser(uid):
    for user in USER_INFO:
        if user["user_info"]["id"] == uid: #启动时候添加回复
            return user
    return False

class BotIndex(ListView):
    template_name = 'bot_index.html'
    qr_url = ""
    # init_file_name = 5
    def get(self, request, *args, **kwargs):

        _uid = request.GET.get("uid", "")
        user = GetUser(_uid)
        if user : #已登录
            self.uid = _uid
            uuid = get_QRuuid()
            self.uuid = uuid
            user["uuid"] = uuid #用户同步uuid
            self.auto_reply = user["auto_reply"] #准备将回复模板传到前端
            self.qr_url = '%s/qrcode/%s' % (BASE_URL, uuid) #二维码链接
            _filePath = SETTING.BASE_DIR + '\wx_app\lib/robote/new_itchat.py '
            _cmd = u'python '+ _filePath + uuid
            subprocess.Popen(_cmd, shell=True) #启动项目
        else:#未登录情况
            self.uuid = 123
            self.auto_reply = None
            pass
        return super(BotIndex, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context =super(BotIndex, self).get_context_data(**kwargs)
        context['qr_url'] = self.qr_url
        context['uid'] = self.uid
        context['uuid'] = self.uuid
        context['auto_reply'] = self.auto_reply
        return context
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        print "OK",requests
        _uid = request.POST.get("uid", "")
        user = GetUser(_uid)
        _reply = request.POST.get("reply", "")
        print _reply
        _reply_dict = json.loads(_reply)
        print _reply_dict
        print user
        user["auto_reply"] = _reply_dict  #直接更改user_reply 的key
        mydict = {"msg":u"回复模板设置成功"}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

USER_ACCOUNT = [
    {"account":'1',
    "secret":'1',
     'reply':{"1":"231","2":"432"}}
]
class UserLogin(ListView):
    template_name = 'bot_login_user.html'
    def get(self, request, *args, **kwargs):
        uuid = request.GET.get("uuid", "")
        is_login =  request.GET.get("is_login", "")
        user_name =  request.GET.get("user_name", "")
        print 123,uuid,is_login,user_name
        return super(UserLogin, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context =super(UserLogin, self).get_context_data(**kwargs)
        # context['qr_url'] = self.qr_url
        # context['uuid'] = self.uuid
        return context
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        print "OK",requests
        _register = self.request.POST.get("register", "")
        _account = self.request.POST.get("account", "")
        _secret = self.request.POST.get("secret", "")

        #用户注册
        if _register:
            user = {
                "account":_account,
                "secret":_secret
            }
            USER_ACCOUNT.append(user)
            mydict = {'is_login':'false', 'msg':u'注册成功'}
        else:
            mydict = {'is_login':'false','msg':u'登陆失败'}
            print USER_ACCOUNT
            for u in USER_ACCOUNT:
                if u["account"] == _account and u["secret"] == _secret:
                    mydict = {'is_login':'true','msg':u'登陆成功',"account":_account}
                    break
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

class ReceiveCallback(ListView):
    def get(self, request, *args, **kwargs):
        uuid = request.GET.get("uuid", "")
        # is_login =  request.GET.get("is_login", "")
        # user_name =  request.GET.get("user_name", "")

        print uuid
        #Todo uuid查询用户
        user = USER_INFO[0]

        print "ReceiveCallback:", user["auto_reply"]
        mydict = {
            "auto_reply":user["auto_reply"]
        }
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )


class UpdateReply(ListView):
    def get(self, request, *args, **kwargs):
        pass
        # _uuid = request.GET.get("uuid", "")
        # return HttpResponse(
        #     json.dumps(USER_REPLY[_uuid]),
        #     content_type="application/json"
        # )



















