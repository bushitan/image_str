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
    "user_info":{"uid":"1","user_name":"11","password":"11"},
    "is_login":False,
    "uuid":"",
    "auto_reply":{"1":"123","2":"wqe"},
    "talk_data":"",
}]

#通过uuid获取用户信息
def GetUser(uid = None , uuid = None):
    for user in USER_INFO:
        if str(user["user_info"]["uid"]) == str(uid) :
            return user
        if  user["uuid"] == uuid: #启动时候添加回复
            return user
    return False


class BotIndex(ListView):
    template_name = 'bot_index.html'
    qr_url = ""
    # init_file_name = 5
    def get(self, request, *args, **kwargs):

        _uid = request.GET.get("uid", "")
        print _uid
        user = GetUser(uid = _uid)
        print user

        if user : #已登录
            uuid = get_QRuuid()
            self.uuid = uuid
            user["uuid"] = uuid #用户同步uuid
            self.auto_reply = user["auto_reply"] #准备将回复模板传到前端
            self.qr_url = '%s/qrcode/%s' % (BASE_URL, uuid) #二维码链接
            _filePath = SETTING.BASE_DIR + '\wx_app\lib/robote/new_itchat.py '
            _cmd = u'python '+ _filePath + uuid
            subprocess.Popen(_cmd, shell=True) #启动项目
        else:#未登录情况
            mydict = {"msg":u"用户未登录"}
            return HttpResponse(
                json.dumps(mydict),
                content_type="application/json"
            )
            # self.uuid = 123
            # self.auto_reply = None
            # pass
        return super(BotIndex, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context =super(BotIndex, self).get_context_data(**kwargs)
        context['qr_url'] = self.qr_url
        context['uuid'] = self.uuid
        context['auto_reply'] = self.auto_reply
        return context
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        _uuid = request.POST.get("uuid", "")
        user = GetUser( uuid = _uuid)
        _reply = request.POST.get("reply", "")
        # print _reply
        _reply_dict = json.loads(_reply)
        # print _reply_dict
        # print user
        user["auto_reply"] = _reply_dict  #直接更改user_reply 的key
        mydict = {"msg":u"回复模板设置成功"}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

# USER_ACCOUNT = [
#     {"account":"1",
#     "secret":"1",
#      "reply":{"1":"231","2":"432"}}
# ]
import math

class UserLogin(ListView):
    template_name = 'bot_login_user.html'
    def get(self, request, *args, **kwargs):
        # uuid = request.GET.get("uuid", "")
        # is_login =  request.GET.get("is_login", "")
        # user_name =  request.GET.get("user_name", "")
        # print 123,uuid,is_login,user_name
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
        _register = request.POST.get("register", "")
        _user_name = request.POST.get("user_name", "")
        _password = request.POST.get("password", "")
        _uid = "2"
        #用户注册
        if _register:
            user = {
                "user_info":{"uid":_uid,"user_name":_user_name,"password":_password},
                "is_login":False,
                "uuid":"",
                "auto_reply":{"a":"mnm","b":"pop"},
                "talk_data":"",
            }
            USER_INFO.append(user)
            mydict = {'is_login':'false', 'msg':u'注册成功'}
        else:
            mydict = {'is_login':'false','msg':u'登陆失败'}
            for u in USER_INFO:
                if u["user_info"]["user_name"] == _user_name and u["user_info"]["password"] == _password:
                    mydict = {'is_login':'true','msg':u'登陆成功',"uid":u["user_info"]["uid"]}
                    break
        print mydict,USER_INFO
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )
import time
#查询二维码是否扫描，若已经扫描，则登陆成功
class QRStatus(ListView):
    def post(self, request, *args, **kwargs):
        _uuid = request.POST.get("uuid", "")
        user = GetUser( uuid = _uuid)
        # print user
        # print user["is_login"]

        #长连接轮训二维码扫描情况
        step = 0
        while step<20:
            # print "step:",step
            if user["is_login"] == "True" or user["is_login"] == True:
                mydict = {'qr_status':'true', 'msg':u'已扫描，登陆成功'}
                return HttpResponse(
                    json.dumps(mydict),
                    content_type="application/json"
                )
            step = step + 1
            time.sleep(0.1)

        mydict = {'qr_status':'false', 'msg':u'二维码未扫描'}
        print mydict
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

        # if user["is_login"] == "True" or user["is_login"] == True:
        #     mydict = {'qr_status':'true', 'msg':u'已扫描，登陆成功'}
        # else:
        #     mydict = {'qr_status':'false', 'msg':u'二维码未扫描'}
        # print mydict
        # return HttpResponse(
        #     json.dumps(mydict),
        #     content_type="application/json"
        # )
class LoginCallback(ListView):
    def get(self, request, *args, **kwargs):
        _uuid = request.GET.get("uuid", "")
        _is_login =  request.GET.get("is_login", "")
        _user_name =  request.GET.get("user_name", "")

        user = GetUser( uuid = _uuid)
        user["is_login"] = _is_login
        # print 123,uuid,is_login,user_name
        mydict = {"msg":"login ok"}
        return HttpResponse(
            json.dumps(mydict),
            content_type="application/json"
        )

class ReceiveCallback(ListView):
    def get(self, request, *args, **kwargs):
        uuid = request.GET.get("uuid", "")
        # is_login =  request.GET.get("is_login", "")
        # user_name =  request.GET.get("user_name", "")

        # print uuid
        #Todo uuid查询用户
        user = USER_INFO[0]

        # print "ReceiveCallback:", user["auto_reply"]
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



















