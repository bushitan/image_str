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

from django.db import transaction #事务

class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):

        # user = self.request.user
        # if not user.is_authenticated():
        #    kwargs['user_id'] = "none"
        # else:
        #    kwargs['user_id'] = user
        print "get_context_data"
        context = super(BaseMixin, self).get_context_data(**kwargs)

        print "get_context_data"
        return context

# 1 创建主题
class Start(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            _theme_name = request.GET['theme_name']
            _img_id = request.GET['img_id']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)


            with transaction.atomic(): # 事务，同时创建 theme,step,rel_theme_user
                _theme = Theme( name = _theme_name ,user_id = _user)
                _theme.save()

                _rel = RelThemeUser( theme_id = _theme ,user_id = _user)
                _rel.save()

                # 创建第1步，该步可以抢
                _step = Step(theme_id = _theme ,user_id = _user,img_id = _img_id,number = 1,is_free=0)
                _step.save()

            _share = {
                "theme_id":_theme.id,
                "step_id":_step.id,
                "step_number":_step.number,
            }
            Log.log(u"创建绘画主题成功",_user,self.__class__.__name__)
            return Result.Success(share= _share)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 2 创建step 继续玩
class Continue(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            _theme_id = request.GET['theme_id']
            _img_id = request.GET['img_id']
            _step_id = request.GET['step_id']
            _step_number = request.GET['step_number']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)


            with transaction.atomic(): # 事务，继续游戏，加入,step,rel_theme_user
                #目测没用，不懂为什么
                # if Step.objects.filter(id=_step_id ) is False:
                #     return Result.Problem(msg=u"网络验证失败，已完成作品保存至收藏夹，请重新发起活动")

                _current_step = Step.objects.get(id=_step_id )
                #为避免创立者收回权限，查是否能加入当前步骤
                if _current_step.is_free == 1: # 当前步骤不可插入，返回
                    Log.log(u"创建绘画主题成功",_user,self.__class__.__name__)
                    return Result.Problem(msg=u"该绘画主题已经结束，已完成作品保存至收藏夹，请重新发起活动")


                #主题用户关系不存在，加入关系表
                if RelThemeUser.objects.filter(theme_id=_theme_id ) is False:
                    _rel = RelThemeUser( theme_id = _theme_id ,user_id = _user)
                    _rel.save()

                _new_number = _current_step.number + 1
                # 创建第1步，该步可以抢  Todo _theme_id 直接查询可能会出错
                # 下一步的用户为空
                _step = Step(theme_id = _theme_id ,user_id = _user,img_id = _img_id,number = _new_number)
                _step.save()

            _share = {
                "theme_id":_theme.id,
                "step_id":_step.id,
            }
            Log.log(u"创建绘画主题成功",_user,self.__class__.__name__)
            return Result.Success(share= _share)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 3 抢step
class Snatch(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            _theme_id = request.GET['theme_id']
            # _img_id = request.GET['img_id']
            _step_id = request.GET['step_id']
            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)

            with transaction.atomic(): # 事务，继续游戏，加入,step,rel_theme_user
                _current_step = Step.objects.get(id=_step_id )
                if _current_step.next_user is not None:
                    # Log.log(u"",_user,self.__class__.__name__)
                    return Result.Problem(msg=u"来晚了，画布已经被抢了")

                #能抢，上一步is_free = 1 ，别的就不能抢了
                _current_step.next_user = _user.id
                _current_step.save()

                _img = Img.objects.get(id = _current_step.img_id )
                _theme = Theme.objects.get(id = _current_step._theme_id )

            _step={
                "step_id":_current_step,
                "img_id":_img.id,
                "img_yun_url":_img.yun_url,
                "theme_name":_theme.name,
            }
            Log.log(u"抢画成功",_user,self.__class__.__name__)
            return Result.Success(step= _step)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 4 用户查询参加的所有Theme主题
class ThemeQuery(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)

            _rel_obj_list = RelThemeUser.objects.filter(user_id=_user )
            _theme_list = []
            for r in _rel_obj_list:
                _theme_list.append({
                    "theme_name",r.name,
                    "them_id",r.id,
                })
            Log.log(u"查询用户主题成功",_user,self.__class__.__name__)
            return Result.Success(theme_list= _theme_list)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 5 用户查询指定主题下，所有的step步骤，用player播放
class StepQuery(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            _theme_id = request.GET['theme_id']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)


            _theme = Theme.objects.get(id=_theme_id )
            _step_obj_list = Step.objects.filter(user_id=_theme )
            _step_list = []
            for s in _step_obj_list:
                _img = Img.objects.get(id=s.img_id )
                _step_list.append({
                    "theme_name":_theme.name,
                    "img_yun_url":_img.yun_url,
                    "step_number":_step.number,
                })

            Log.log(u"查询所有步骤成功",_user,self.__class__.__name__)
            return Result.Success(step_list= _step_list)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
            return Result.Fail(msg= str(e))
