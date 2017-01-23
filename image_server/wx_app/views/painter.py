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
            _img_url = request.GET['img_url']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)


            with transaction.atomic(): # 事务，同时创建 theme,step,rel_theme_user
                #创建主题
                _theme = Theme( name = _theme_name ,user_id = _user)
                _theme.save()
                #绑定主题与用户关系
                _rel = RelThemeUser( theme = _theme ,user = _user)
                _rel.save()
                # 创建主题第1步step，状态为可以抢
                print _theme,_theme.id
                _step = Step(theme_id = _theme,user_id = _user,img_url = _img_url)
                _step.save()
            return Result.Success(
                is_success = "true",
                theme_name = _step.theme_id.name,
                step_id = _step.id,
                img_url = _step.img_url,
            )
        except Exception ,e:
            print Exception,e
            logger.error(e)
            LoggerObj.error(str(e),self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 2 创建step 继续玩
class Continue(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            _img_url = request.GET['img_url']
            _step_id = request.GET['step_id']
            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)


            with transaction.atomic(): # 事务，继续游戏，加入,step,rel_theme_user
                #目测没用，不懂为什么
                # if Step.objects.filter(id=_step_id ) is False:
                #     return Result.Problem(msg=u"网络验证失败，已完成作品保存至收藏夹，请重新发起活动")

                # 1 删除
                if Step.objects.filter(id=_step_id ).exists() is False:
                     return Result.Success(is_success="false",title=u"主题已被删除",content=u"主题已被创意者删除。您完成作品已经保存在收藏夹，能继续发起新活动")
                # 用户获取“继续画”的对象
                _current_step = Step.objects.get(id=_step_id )

                # 2 为避免创立者收回权限，查是否能加入当前步骤
                if _current_step.next_user != int(_user.id):
                    return Result.Success(is_success="false",title=u"创意者已收回权限",content=u"因长时间未完成，该活动创立者已经收回权限。已完成作品保存至收藏夹，请重新发起活动")

                # 3 下一步创建成功，步骤增加1，设置下一步的用户为空，可抢
                _theme = _current_step.theme_id
                _new_number = _current_step.number + 1
                next_step = Step(theme_id = _theme ,user_id = _user,img_url = _img_url,number = _new_number)
                next_step.save()
            return Result.Success(
                is_success = "true",
                theme_name = next_step.theme_id.name,
                step_id = next_step.id,
                img_url = next_step.img_url,
            )
        except Exception ,e:
            print Exception,e
            logger.error(e)
            LoggerObj.error(str(e),'',self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 3 抢step
class Snatch(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            _theme_id = request.GET['theme_id']
            _step_id = request.GET['step_id']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)

            #用户从未登录
            if  Step.objects.filter(next_user= int(_user.id) ).exists() is False:
                pass
            else:
                #判断能不能抢
                _step_latest = Step.objects.filter( next_user= int(_user.id) ).latest()
                _theme = _step_latest.theme_id
                _number = _step_latest.number
                # 2.1 当前step的number等于，主题theme的步骤总数
                if _number == Step.objects.filter( theme_id = _theme ).count():
                    return Result.Success(
                        is_success="no_snatch",
                        title=u"不能抢啦",
                        content=u"请先完成原来的画，有始有终哦",
                        join_status = PAINTER_STEP_BUSY,
                        theme_id = _step_latest.theme_id.id,
                        theme_name = _step_latest.theme_id.name,
                        step_id = _step_latest.id,
                        img_url = _step_latest.img_url,
                        user_id = _user.id,
                    )

            #能抢
            with transaction.atomic(): # 事务，继续游戏，加入,step,rel_theme_user
                # 1.1 player 只传递theme_id
                if _theme_id != "" :
                    print _theme_id
                    _current_step = Step.objects.filter(theme_id= _theme_id ).latest()
                    _content = u"抢画成功，记得分享"
                # 1.2 painter 只传递step_id
                else:
                    _current_step = Step.objects.get(id=_step_id )
                    _content = u'画完点"找人画两笔",继续分享画哦',

                # 2 抢不成功
                if _current_step.next_user is not None:
                    # Log.log(u"",_user,self.__class__.__name__)
                    return Result.Success(is_success="false",title=u"没抢到",content=u"来晚了，画布已经被抢了")

                # 3 抢成功
                _current_step.next_user = int(_user.id)
                _current_step.save()
                _theme = _current_step.theme_id
                 # 3 主题用户关系不存在，加入关系表
                if RelThemeUser.objects.filter(theme= _theme ).exists() is False:
                    print 'Snatch add Rel_theme_user False'
                    _rel = RelThemeUser( theme = _theme ,user = _user)
                    _rel.save()
            return Result.Success(
                is_success="true",
                title=u"抢画成功",
                content=_content,
                step_id=_current_step.id,
                img_url=_current_step.img_url,
                theme_name= _theme.name
            )
        except Exception ,e:
            print Exception,e
            logger.error(e)
            # Log.error(str(e),'',self.__class__.__name__)
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

            _rel_obj_list = RelThemeUser.objects.filter(user=_user )
            print _rel_obj_list
            _theme_list = []
            for r in _rel_obj_list:
                print 'R:', r,r.theme.id
                if r.theme.lift != 2: # 该 theme没有被删除
                    print r.theme.name,r.theme.id,r.theme.lift
                    _theme_list.append({
                        "theme_name":r.theme.name,
                        "theme_id":r.theme.id,
                        "theme_lift":r.theme.lift,
                    })
            # Log.log(u"查询用户主题成功",_user,self.__class__.__name__)
            print _theme_list
            return Result.Success(theme_list= _theme_list)
            # return HttpResponse(json.dumps({"status":"true","theme_list":_theme_list}),content_type="application/json")
        except Exception ,e:
            print Exception,e
            logger.error(e)
            LoggerObj.error(str(e),'',self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 5 用户查询指定主题下，所有的step步骤，用player播放
class StepQuery(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            _session = request.GET['session']
            _theme_id = request.GET['theme_id']
            print _session,_theme_id
            # if  Login.SessionExists(_session) is False:
            #     return Result.Fail(msg=u"用户不存在,请重新登录")
            # _user = Login.GetUser(_session)
            # 查step_list ，不是用户也可以登录
            _theme = Theme.objects.get(id=_theme_id )
            _step_obj_list = Step.objects.filter(theme_id=_theme )
            _step_list = []
            for s in _step_obj_list:
                _step_list.append({
                    "step_id":s.id,
                    "img_url":s.img_url,
                    "step_number":s.number,
                    "user_id":s.user_id.id,
                    "next_user_id":s.next_user,
                })
            # Log.log(u"获取主题内容成功",'',self.__class__.__name__)
            return Result.Success(theme_name=_theme.name,step_list=_step_list)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            LoggerObj.error(str(e),'',self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 6 查询用户是否正在参与活动，
# 正在参加，nextuser.number == count
# join_status 用户参加活动的状态
# 1 未参加活动
# 2 正在参加
# 3 待分享
PAINTER_STEP_FREE = 1
PAINTER_STEP_BUSY = 2
PAINTER_STEP_SHARE = 3
class JoinLatest(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)
            # 1 用户从未参加
            if  Step.objects.filter(next_user= int(_user.id) ).exists() is False:
                return Result.Success(join_status = PAINTER_STEP_FREE,user_id = _user.id,)
            # 2 用户已经参加过
            else:
                _step_latest = Step.objects.filter( next_user= int(_user.id) ).latest()
                _theme = _step_latest.theme_id
                _number = _step_latest.number
                # 2.1 当前step的number等于，主题theme的步骤总数
                if _number == Step.objects.filter( theme_id = _theme ).count():
                    return Result.Success(
                        join_status = PAINTER_STEP_BUSY,
                        theme_id = _step_latest.theme_id.id,
                        theme_name = _step_latest.theme_id.name,
                        step_id = _step_latest.id,
                        img_url = _step_latest.img_url,
                        user_id = _user.id,
                    )
                # 2.2 已经分享了的，number不等于theme的总数
                else:
                     return Result.Success(join_status = PAINTER_STEP_FREE,user_id = _user.id,)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            LoggerObj.error(str(e),'',self.__class__.__name__)
            return Result.Fail(msg= str(e))


class Color(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        # _colors =  ['#6326b6','#000032', '#FF0bb0', '#FcA5b0', '#FFFF00', '#208010', '#0b40FF', '#fff55f',]
        _colors = ['#666666','#000000', '#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#ffffff',]
        # paint_color = '#fff55f'
        _paint_color = '#666666'
        return Result.Success(colors = _colors,paint_color = _paint_color )
