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


#视频转GIF，不用上传，直接返回前台
class Video2Gif_NoUpload(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        _user = ""
        try:
            session = request.GET['session']
            video_url = request.GET['video_url']
            start_time = int( request.GET['start_time'] )
            duration_time = int(request.GET['duration_time'])
            width = int(request.GET['width'])
            height = int(request.GET['height'])
            print width,height
            print datetime.datetime.now()
            if  User.objects.filter( session = session).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在,请重新登录"}),content_type="application/json" )

            _user = User.objects.get( session = session)

            print datetime.datetime.now()
             #下载文件
            name = str(video_url).split("/")[-1]
            img_down_path = FILE_PATH.Down(name)["local_path"]


            if os.path.exists(img_down_path) is False : #文件不存在，下载
                f = urllib2.urlopen(video_url)
                data = f.read()
                with open(img_down_path, "wb") as code:
                    code.write(data)
                #GIf路径
            print datetime.datetime.now()
            img_type = "gif"
            _up_path = FILE_PATH.Up(img_type,_user.id) #按用户id命名图片
            _local_url =  "http://"+ request.get_host() +"/static/magick/upload/" + _up_path["file_name"]  #"http://127.0.0.1:8000

            #视频转换
            # magick = Magick(_up_path["local_path"])
            # magick.Video2Gif(img_down_path, _up_path["local_path"],start_time,start_time+duration_time)
            end_time = start_time+duration_time  #结束时间

            #裁剪大小
            new_size = 480
            if(width >= height):
                resize = float(new_size)/float(width)
            else:
                resize = float(new_size)/float(height)

            print resize
            _cmd = u"python %s  %s %s %s %s %s" % ( FILE_PATH.GetMagickPy(),img_down_path, _up_path["local_path"],start_time,end_time,resize)
            subprocess.check_output(_cmd, shell=True)

            print datetime.datetime.now()
            return HttpResponse(json.dumps({"status":"true","local_url": _local_url}),content_type="application/json")
        except Exception ,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":str(e)}),content_type="application/json")
import inspect
#视频转GIF 返回前台 不上传，
class Join_NoUpload(BaseMixin, ListView):

    def get(self, request, *args, **kwargs):

        _user = ""
        try:
            session = request.GET['session']
            first_url = request.GET['first']  #原图地址
            seconde_url = request.GET['seconde']

            if  Login.SessionExists(session) is False:
                return Result.Fail(msg=u"用户不存在,请重新登录")
            _user = Login.GetUser(session)
            #压缩后地址 ,
            _re_size = 180
            _re_url = "?imageMogr2/thumbnail/%sx%s" % (_re_size,_re_size)
            first_url_resize = first_url + _re_url
            seconde_url_resize = seconde_url + _re_url

             #为2幅图重命名
            first_file_name = str(_re_size) + "_" + str(first_url).split("/")[-1]  #  文件名字   含后缀  180_56123.gif
            first_name = first_file_name.split(".")[0]  # 图片名字   不含后缀   180_56123
            first_type = first_file_name.split(".")[1]
            seconde_file_name = str(_re_size) + "_" + str(seconde_url).split("/")[-1]
            seconde_name = seconde_file_name.split(".")[0]  # 图片名字   不含后缀   180_56123
            seconde_type = seconde_file_name.split(".")[1]

            print first_file_name,seconde_file_name
            #GIf路径
            # _up_path = CreateFileName("gif",_user.id) #按用户id命名图片
            _join_name = first_name + "join" + seconde_name + ".gif"
            _join_path = SETTINGS.MAGICK_FILE + _join_name


            _first_path = SETTINGS.MAGICK_FILE + first_file_name   # 下载、处理用，两张图片的本地完整路径
            _seconde_path = SETTINGS.MAGICK_FILE + seconde_file_name

             #join文件存在，直接返回
            if os.path.exists(_join_path) is True :
                _local_url =  "http://"+ request.get_host() +"/static/magick/upload/" + _join_name #"http://127.0.0.1:8000
                Log.log(u"join成功",_user,self.__class__.__name__)
                return Result.Success(local_url= _local_url)

            print datetime.datetime.now()
            if os.path.exists(_first_path) is False :
                print 111
                DownFile(first_url_resize,_first_path)
            if os.path.exists(_seconde_path) is False :
                print 111
                DownFile(seconde_url_resize,_seconde_path)
            print datetime.datetime.now()

            #GIF拼接
            magick = Magick()
            magick.Join_HasReize(_first_path,first_type,_seconde_path,seconde_type,_join_path,_re_size)

            #返回拼接好的路径
            _local_url =  "http://"+ request.get_host() +"/static/magick/upload/" + _join_name #"http://127.0.0.1:8000
            Log.log(u"join成功",_user,self.__class__.__name__)
            return Result.Success(local_url= _local_url)
        except Exception ,e:
            print Exception,e
            logger.error(e)
            Log.error(str(e),_user,self.__class__.__name__)
            return Result.Fail(msg= str(e))
