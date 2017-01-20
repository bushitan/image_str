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
            _img_url = request.GET['img_url']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)


            with transaction.atomic(): # 事务，同时创建 theme,step,rel_theme_user
                print "OK1"
                _theme = Theme( name = _theme_name ,user_id = _user)
                _theme.save()
                print "OK2" , _theme , _user
                _rel = RelThemeUser( theme = _theme ,user = _user)
                _rel.save()
                print "OK3"
                # 创建第1步，该步可以抢
                print _theme,_theme.id
                _step = Step(theme_id = _theme,user_id = _user,img_url = _img_url)
                _step.save()
                print "OK4"

            # _share = {
            #     "theme_id":_theme.id,
            #     "step_id":_step.id,
            #     "step_number":_step.number,
            # }
            Log.log(u"创建绘画主题成功",_user,self.__class__.__name__)
            # return Result.Success(
            #     theme_id= _theme.id,
            #     step_id = _step.id,
            #     step_number = _step.number,
            # )
            return Result.Success(
                is_success = "true",
                theme_name = _step.theme_id.name,
                step_id = _step.id,
                img_url = _step.img_url,
            )
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),self.__class__.__name__)
            return Result.Fail(msg= str(e))

# 2 创建step 继续玩
class Continue(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            _session = request.GET['session']
            # _theme_id = request.GET['theme_id']
            _img_url = request.GET['img_url']
            _step_id = request.GET['step_id']
            # _step_number = request.GET['step_number']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)


            with transaction.atomic(): # 事务，继续游戏，加入,step,rel_theme_user
                #目测没用，不懂为什么
                # if Step.objects.filter(id=_step_id ) is False:
                #     return Result.Problem(msg=u"网络验证失败，已完成作品保存至收藏夹，请重新发起活动")
                print _step_id
                _current_step = Step.objects.get(id=_step_id )
                print _current_step.next_user,_user.id
                #应该不用 为避免创立者收回权限，查是否能加入当前步骤
                if _current_step.next_user != int(_user.id):
                    Log.log(u"创建绘画主题成功",_user,self.__class__.__name__)
                    return Result.Success(is_success="false",title=u"创意者已收回权限",content=u"因长时间未完成，该活动创立者已经收回权限。已完成作品保存至收藏夹，请重新发起活动")

                print 1
                _theme = _current_step.theme_id
                print 2,_theme
                #主题用户关系不存在，加入关系表
                if RelThemeUser.objects.filter(theme=_theme ).exists() is False:
                    print 'False'
                    _rel = RelThemeUser( theme = _theme ,user = _user)
                    _rel.save()
                print 'ok'
                _new_number = _current_step.number + 1

                #  设置 下一步的用户为空，可抢
                next_step = Step(theme_id = _theme ,user_id = _user,img_url = _img_url,number = _new_number)
                next_step.save()

            # _share = {
            #     "theme_id":_theme.id,
            #     "step_id":_step.id,
            # }
            Log.log(u"创建绘画主题成功",_user,self.__class__.__name__)
            # return Result.Success(share= _share)
            # return Result.Success(
            #     is_success = "true",
            #     theme_id = _theme.id,
            #     step_id = _step.id,
            #     step_number = _step.number,
            # )
            return Result.Success(
                is_success = "true",
                theme_name = next_step.theme_id.name,
                step_id = next_step.id,
                img_url = next_step.img_url,
            )


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
            # _theme_id = request.GET['theme_id']
            # _img_id = request.GET['img_id']
            _step_id = request.GET['step_id']

            if  Login.SessionExists(_session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(_session)

            with transaction.atomic(): # 事务，继续游戏，加入,step,rel_theme_user
                print 1
                _current_step = Step.objects.get(id=_step_id )
                print _current_step.next_user , _current_step.id
                if _current_step.next_user is not None:
                    # Log.log(u"",_user,self.__class__.__name__)
                    return Result.Success(is_success="false",title=u"没抢到",content=u"来晚了，画布已经被抢了")

                #能抢，上一步is_free = 1 ，别的就不能抢了
                _current_step.next_user = int(_user.id)
                _current_step.save()

                print  _current_step.theme_id.id
                # _theme = Theme.objects.get(id = _current_step.theme_id)
                _theme = _current_step.theme_id
                print _theme
            # _step={
            #     "step_id":_current_step.id,
            #     "img_url":_current_step.img_url,
            #     "theme_name":_theme.name,
            # }
            Log.log(u"抢画成功",_user,self.__class__.__name__)
            return Result.Success(
                is_success="true",
                title=u"抢画成功",
                content=u'画完点"找人画两笔",继续分享画哦',
                step_id=_current_step.id,
                img_url=_current_step.img_url,
                theme_name= _theme.name
            )
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),'',self.__class__.__name__)
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
            Log.log(u"查询用户主题成功",_user,self.__class__.__name__)
            print _theme_list
            return Result.Success(theme_list= _theme_list)
            # return HttpResponse(json.dumps({"status":"true","theme_list":_theme_list}),content_type="application/json")
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
            _step_obj_list = Step.objects.filter(theme_id=_theme )
            _step_list = []
            for s in _step_obj_list:
                _step_list.append({
                    "img_url":s.img_url,
                    "step_number":s.number,
                })
            # _theme_dict = {
            #     "theme_name":_theme.name,
            #     "step_list":_step_list,
            # }
            Log.log(u"获取主题内容成功",_user,self.__class__.__name__)
            return Result.Success(theme_name=_theme.name,step_list=_step_list)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
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

            #用户从未参加
            if  Step.objects.filter(next_user= int(_user.id) ).exists() is False:
                print False
                return Result.Success(join_status = PAINTER_STEP_FREE)

            #用户最近参加记录,查user ，参与者
            # _step_latest = Step.objects.filter(next_user= int(_user.id) ).latest()
            _step_latest = Step.objects.filter(user_id= _user ).latest()

            # 该步骤 next_user 为空，未分享
            print "share:",_step_latest,_step_latest.next_user
            # if _step_latest.next_user is None:
            #     return Result.Success(
            #         join_status = PAINTER_STEP_SHARE,
            #         theme_id = _step_latest.theme_id.id,
            #         theme_name = _step_latest.theme_id.name,
            #         step_id = _step_latest.id,
            #         img_url = _step_latest.img_url,
            #     )
            # else:
            if _step_latest.next_user == int(_user.id):
                return Result.Success(
                    join_status = PAINTER_STEP_BUSY,
                    theme_id = _step_latest.theme_id.id,
                    theme_name = _step_latest.theme_id.name,
                    step_id = _step_latest.id,
                    img_url = _step_latest.img_url,
                )
            else:
                return Result.Success(join_status = PAINTER_STEP_FREE)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
            return Result.Fail(msg= str(e))
        #  next_user 存在，判断是否为用户

            #最近参加主题的step总数
            # _count = Step.objects.filter(theme_id=_step_latest.theme_id ).count()
            # print "OK1"
            # # 主题下step总数，等于next_user对应的number，用户正在参与活动
            # if _count == _step_latest.number:
            #     print "ing"
            #     Log.log(u"用户正在参与互动",_user,self.__class__.__name__)
            #     return Result.Success(
            #         join_status = PAINTER_STEP_BUSY,
            #         theme_id = _step_latest.theme_id.id,
            #         theme_name = _step_latest.theme_id.name,
            #         step_id = _step_latest.id,
            #         img_url = _step_latest.img_url,
            #     )
            # else:
            #     print  _count, _step_latest.number
            #     return Result.Success(join_status = PAINTER_STEP_FREE)