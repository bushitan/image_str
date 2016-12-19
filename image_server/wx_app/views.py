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
log = Logger()

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


class BaseMixin(object):
    def get_context_data(self, *args, **kwargs):

        # user = self.request.user
        # if not user.is_authenticated():
        #    kwargs['user_id'] = "none"
        # else:
        #    kwargs['user_id'] = user
        context = super(BaseMixin, self).get_context_data(**kwargs)
        return context


class Index(BaseMixin, ListView):
    template_name = 'upload1.html'
    def get(self, request, *args, **kwargs):
        return super(Index, self).get(request, *args, **kwargs)
        # return HttpResponse(json.dumps({"status":"false","msg":u"这是index的请求"}),content_type="application/json")
    def get_context_data(self, **kwargs):
        return super(Index, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        try:
            _file = request.FILES['file']
            _user = request.POST['user']

            _type = str(_file.name).split(".")[-1]
            print _user , _type
            _up_path = FILE_PATH.Up(_type)
            file = open(_up_path["local_path"], "wb+")
            for chunk in _file.chunks():
                file.write(chunk)
                file.close()

            return HttpResponse(json.dumps({"status":"true","file":_user }),content_type="application/json")
        except Exception,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"上传图片错误" + e}),content_type="application/json")

class UploadWXImg(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        try:
            print "UploadWXImg"
            _file = request.FILES['file']
            session = request.POST['session']

            # 1 查询用户是否存在
            if  User.objects.filter( session = session).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )
            _user = User.objects.get( session = session)
            _type = str(_file.name).split(".")[-1]
            if _type == "ext-mp4":
                _type = "mp4"
            _up_path = FILE_PATH.Up(_type,_user.id) #按用户id命名图片

            file = open(_up_path["local_path"], "wb+")
            for chunk in _file.chunks():
                file.write(chunk)
                file.close()

            if _type == 'mp4' or _type == "MP4" or _type == "Mp4":
                size = 4
            else:
                #判断size
                im = Image.open(_up_path["local_path"])
                print im.size[0],im.size[1]
                size = 170
                if _type == 'gif' or _type == "GIF" or _type == 'Gif':
                    size = 1
                elif im.size[0] <= im.size[1] :
                    size = 2
                elif im.size[0] > im.size[1] :
                    size = 3

            #3 上传七牛云
            _qiniu = QiNiu()
            if _qiniu.put("",_up_path["file_name"],_up_path["local_path"]) is True: #上传原图
                # 4 上传成，存储数据库
                _yun_url = SETTING.QINIU_HOST + _up_path["file_name"]
                print _yun_url
                _img = Img(
                    name = _up_path["file_name"],
                    yun_url = _yun_url,
                    size = size,
                )
                _img.save()

                #上传的图片添加至该用户的默认目录
                _category = Category.objects.get( user_id = _user ,is_default = 1)
                _rel = RelCategoryImg(category = _category,img = _img )
                _rel.save()

                r_img = {
                    "img_id":_img.id,
                    "yun_url":_img.yun_url, # 七牛云自动缩略图
                    "size":_img.size ,
                    "category_name":_category.name,
                    "category_id":_category.id,
                }

                return HttpResponse(json.dumps({"status":"true","img":r_img}),content_type="application/json")
            return HttpResponse(json.dumps({"status":"false","msg":"上传七牛云失败"}),content_type="application/json")
        except Exception,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"上传图片错误" + e}),content_type="application/json")
# 没有用
class UploadImg(BaseMixin, ListView):
    template_name = 'upload1.html'
    def get(self, request, *args, **kwargs):
        return super(UploadImg, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        return super(UploadImg, self).get_context_data(**kwargs)
    def get_queryset(self):
        pass
    def post(self, request, *args, **kwargs):
        #Todo
        # 1\接收图片二进制数据
        # 2\本地存储
        # 3、上传七牛云
        # 4、上传成功，保存数据库
        #1
        try:
            _uid = request.POST['uid']
            _imgData = base64.b64decode(request.POST['img'])
            _type = request.POST['type']
            # _uid = request.POST['uid']
            if  User.objects.filter( id = _uid ).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )

            #2 图片保存本地
            _up_path = FILE_PATH.Up(_type)
            file = open(_up_path["local_path"], "wb+")
            file.write(_imgData)
            file.flush()
            file.close()

            #3 上传七牛云
            _qiniu = QiNiu()
            if _qiniu.put("",_up_path["file_name"],_up_path["local_path"]) is True: #上传原图
                # 4 上传成，存储数据库
                _yun_url = SETTING.QINIU_HOST + _up_path["file_name"]
                print _yun_url
                _img = Img(
                    name = _up_path["file_name"],
                    yun_url = _yun_url,
                    size = 170,
                )
                _img.save()

                #上传的图片添加至该用户的默认目录
                _category = Category.objects.get( user_id = _uid ,is_default = 1)
                _rel = RelCategoryImg(category = _category,img = _img )
                _rel.save()

                _dict = {
                    "status":"true",
                    "img_id":_img.id,
                    "name":_img.name,
                    "yun_url":_img.yun_url,
                    "size":_img.size,
                    # "create_time":_img.create_time,
                }
                return HttpResponse(
                    json.dumps(_dict),
                    content_type="application/json"
                )
            else:
                return HttpResponse(json.dumps({"status":"false"}),content_type="application/json")
        except Exception,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"上传图片错误" + e}),content_type="application/json")


# 没有用
class UploadVideo(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        try:
            print "UploadVideo"
            _file = request.FILES['file']
            session = request.POST['session']

            # 1 查询用户是否存在
            if  User.objects.filter( session = session).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )
            _user = User.objects.get( session = session)
            _type = str(_file.name).split(".")[-1]
            _up_path = FILE_PATH.Up(_type,_user.id) #按用户id命名图片

            file = open(_up_path["local_path"], "wb+")
            for chunk in _file.chunks():
                file.write(chunk)
                file.close()


            return HttpResponse(
                json.dumps("OK"),
                content_type="application/json"
            )
        except Exception,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"上传图片错误" + e}),content_type="application/json")

KEY_USER_HASH = {} #内存，key-session对应表
class UploadToken(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        session = request.GET['session']
        _type = request.GET['type']

        #小程序独有过滤
        if _type == "ext-mp4":
                _type = "mp4"

        # 1 查询用户是否存在
        if  User.objects.filter( session = session).exists() is False:
            return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )
        _user = User.objects.get( session = session)

        #设置上传路径
        _up_path = FILE_PATH.Up(_type,_user.id)

        _qiniu = QiNiu()
        token,key = _qiniu.getToken("",_up_path["file_name"],_up_path["local_path"])

        #保存图片用户数据
        KEY_USER_HASH[key] = {
            "uid":_user,
            "type":_type
        }
        return HttpResponse(json.dumps({"status":"true","token":token,"key":key}),content_type="application/json")
    def post(self, request, *args, **kwargs):
        try:
            key = request.POST['key']
            _hash = request.POST['hash']
            w = request.POST['w']
            h = request.POST['h']
            duration = request.POST['duration']

            if duration == "" :
                duration = 0.0
            else :
                duration = float(duration)
            if w == "" :
                w = 0
            else :
                w = int(w)
            if h == "" :
                h = 0
            else :
                h = int(h)

            #图片存数据库
            if KEY_USER_HASH.has_key(key):
                _user = KEY_USER_HASH[key]["uid"]
                _type = KEY_USER_HASH[key]["type"]
                if _type == 'mp4' or _type == "MP4" or _type == "Mp4":
                    size = 4
                else:
                    size = 170
                    if _type == 'gif' or _type == "GIF" or _type == 'Gif':
                        size = 1
                    elif w <= h :
                        size = 2
                    elif w > h :
                        size = 3
                _img = Img(
                    name = key,
                    yun_url = SETTING.QINIU_HOST + key,
                    size = size,
                    width = w,
                    height = h,
                    duration = duration
                )
                _img.save()

                #上传的图片添加至该用户的默认目录
                _category = Category.objects.get( user_id = _user ,is_default = 1)
                _rel = RelCategoryImg(category = _category,img = _img )
                _rel.save()

                r_img = {
                    "img_id":_img.id,
                    "yun_url":_img.yun_url, # 七牛云自动缩略图
                    "size":_img.size ,
                    "category_name":_category.name,
                    "category_id":_category.id,
                }
                KEY_USER_HASH.pop(key)
                return HttpResponse(json.dumps({"status":"true","img":r_img}),content_type="application/json")
            return HttpResponse(json.dumps({"status":"false","msg":u"网络出错，请重新上传"}),content_type="application/json")
        except Exception,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"上传图片错误" + e}),content_type="application/json")
#55
class PictureMy(BaseMixin, ListView):
   pass

class PictureHot(BaseMixin, ListView):
    pass
#66
class PictureQuery(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        # 1 查用户名下所有图片 （管理者权限的图片加限制）
        # 2 查目录下所有图片
        # 3 查用户指定目录下图片
        try:
            # _uid = request.POST['uid']
            session = request.GET['session']
            _category_id = request.GET['category_id']

            # print "name",_category_name
            _uid = User.objects.get( session = session)
            # print "_category_id",_category_id
            #1
            if _category_id == "null" and _uid != "null":
                # _user = User.objects.filter( id = _uid )
                _category_list = Category.objects.filter( user_id = _uid)
                _rel = []
                _img_list = []
                #1个用户有多个目录，将多个目录的img读取，
                for _category in _category_list:
                    for _r in RelCategoryImg.objects.filter(category=_category):
                        # print "_r.img.yun_url",type(_r.img),_r.img.name , _r.img.size , _r.img.yun_url , _r.img.create_time
                        _size = str(_r.img.size) + "x" + str(_r.img.size) #size
                        _img_list.append({
                            "img_id":_r.img.id,
                            # "yun_url":_r.img.yun_url + "?imageMogr2/thumbnail/" + _size, # 七牛云自动缩略图
                            "yun_url":_r.img.yun_url, # 七牛云自动缩略图
                            "size":_r.img.size ,
                            "category_name":_category.name,
                            "category_id":_category.id,
                        })

                return HttpResponse(json.dumps({"status":"true","img_list":_img_list}),content_type="application/json")
            #2

            _category_name = request.GET['category_name']
            print _category_name
            if _uid == "null" and _category_name != "null" :
                _category = Category.objects.get( name = _category_name)
                _rel = RelCategoryImg.objects.filter(category=_category)
                return HttpResponse(json.dumps({"status":"true","img_list":_rel}),content_type="application/json")
            #3
            if _uid != "null" and _category_name != "null" :
                _category = Category.objects.get( user_id = _uid, name = _category_name)

                _img_list = []
                for _r in RelCategoryImg.objects.filter(category=_category):
                    _img_list.append({
                        "img_id":_r.img.id,
                        "yun_url":_r.img.yun_url, # 七牛云自动缩略图
                        "size":_r.img.size ,
                        "category_name":_category.name,
                        "category_id":_category.id,
                    })
                # _rel = RelCategoryImg.objects.filter(category=_category)
                return HttpResponse(json.dumps({"status":"true","img_list":_img_list}),content_type="application/json")
            # if  _category_name == "null" :

            # return HttpResponse(json.dumps({"status":"true","img_list":"OK"}),content_type="application/json")
        except Exception ,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"系统查询图片除错" + e}),content_type="application/json")

#77  移动图片
class PictureMove(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            # 移动图片，到新分类
            _img_id = request.GET['img_id']
            _old_category_id = request.GET['old_category_id']
            _new_category_id = request.GET['new_category_id']

            print _img_id,_old_category_id

            if  Category.objects.filter( id = _old_category_id ).exists()is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"目录不存在"}),content_type="application/json" )
            if  Img.objects.filter( id = _img_id ).exists()is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"图片不存在"}),content_type="application/json" )

            _img =Img.objects.get(id = _img_id)
            _old_category = Category.objects.get(id = _old_category_id)
            _new_category = Category.objects.get(id = _new_category_id)
            print
            if RelCategoryImg.objects.filter(category=_new_category,img=_img).exists() :
                return HttpResponse( json.dumps({"status":"false","msg":u"图片已在当前目录"}),content_type="application/json" )

            rel = RelCategoryImg.objects.get(category=_old_category,img=_img)
            rel.category = _new_category
            rel.save()
            # _rel = RelCategoryImg(
            #     category = _category,
            #     img = _img
            # )
            # _rel.save()
            return HttpResponse(json.dumps({"status":"true","img_id":_img_id,"category_id":_new_category_id}),content_type="application/json")
        except Exception ,e:
                print e
                return HttpResponse(json.dumps({"status":"false","msg":u"系统移动图片分组出错"+ e}),content_type="application/json")


#88  图片删除  删除图片、图片目录关系
class PictureDelete(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:

            _img_id = request.GET['img_id']
            _category_id = request.GET['category_id']
            if  Img.objects.filter(id=_img_id).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"图片不存在"}),content_type="application/json" )
            if  Category.objects.filter(id= _category_id).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"目录不存在"}),content_type="application/json" )

            _img = Img.objects.get(id=_img_id)
            _category = Category.objects.get(id=_category_id)
            _rel = RelCategoryImg.objects.filter(img=_img , category_id = _category)
            _img.delete()
            _rel.delete()

            #Todo 删除七牛云数据
            _dict = {
                "status":"true",
                "img_id":_img_id,
                "category_id":_category_id,
            }
            return HttpResponse(
                json.dumps(_dict),
                content_type="application/json"
            )
        except Exception ,e:
                print e
                return HttpResponse(json.dumps({"status":"false","msg":u"删除图片出错"+ e}),content_type="application/json")

class PictureAdd(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            _img_id = request.GET['img_id']
            session = request.GET['session']
            _user = User.objects.get( session = session)

            _img = Img.objects.get(id=_img_id)
            print _img
            _category = Category.objects.get( user_id = _user ,is_default = 1)
            print _category

            if RelCategoryImg.objects.filter(img=_img , category_id = _category) is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"已收藏"}),content_type="application/json" )

            _rel = RelCategoryImg(
                img=_img ,
                category = _category
            )
            _rel.save()

            r_img = {
                "img_id":_img.id,
                "yun_url":_img.yun_url, # 七牛云自动缩略图
                "size":_img.size ,
                "category_name":_category.name,
                "category_id":_category.id,
            }
            print r_img
            return HttpResponse(json.dumps({"status":"true","img":r_img}),content_type="application/json")
        except Exception ,e:
                print e
                return HttpResponse(json.dumps({"status":"false","msg":u"收藏图片出错"+ e}),content_type="application/json")


#77
class CategoryAdd(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            _category_name = request.GET['category_name']
            session = request.GET['session']
            #user 不存在
            if   User.objects.filter( session = session).exists() is False:
                return HttpResponse(
                    json.dumps({"status":"false","msg":u"用户不存在"}),
                    content_type="application/json"
                )

            _user = User.objects.get( session = session)
            print _category_name
            _category = Category(
                name = _category_name,
                user_id = _user,
            )
            _category.save()
            c_dict = {
                "category_id":_category.id,
                "name":_category.name,
                "is_default":_category.is_default,
                "hasImg":RelCategoryImg.objects.filter( category = _category ).exists(),
            }
            return HttpResponse(json.dumps({"status":"true","category":c_dict}),content_type="application/json")
        except Exception ,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"系统增加目录出错" + e}),content_type="application/json")

#88
class CategoryReset(BaseMixin, ListView):
    def post(self, request, *args, **kwargs):
        pass

#99
class CategoryDelete(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:

            session = request.GET['session']
            _category_id = request.GET['category_id']
            print session,_category_id
            #user 不存在
            if  User.objects.filter( session = session ).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )

            if  Category.objects.filter( id = _category_id ).exists()is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"目录不存在"}),content_type="application/json" )

            _user = User.objects.get( session = session )
            # 1 目录只能给本uid 删除
            if  Category.objects.filter( id = _category_id ,user_id = _user).exists()is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户没有删除该目录权限"}),content_type="application/json" )

            # 2 有子目录不能删除
            if  Category.objects.filter( parent_id = _category_id ).exists():
                return HttpResponse( json.dumps({"status":"false","msg":u"存在子目录，请先移除子目录"}),content_type="application/json" )

            # 3 relcatimig 中，目录下有图片不能删除
            _category =  Category.objects.get( id = _category_id )
            if  RelCategoryImg.objects.filter( category = _category ).exists():
                return HttpResponse( json.dumps({"status":"false","msg":u"目录下存在图片，请先移除图片"}),content_type="application/json" )

            #删除目录
            _category.delete()
            # return HttpResponse(json.dumps({"status":"true","category_id":_category.id}),content_type="application/json")
            #查询用户名下所有目录
            _list = Category.objects.filter( user_id = _user)
            _category_list = []
            for c in _list:
                _category_list.append({
                    "category_id":c.id,
                    "name":c.name,
                    "is_default":c.is_default,
                    "hasImg":RelCategoryImg.objects.filter( category = c ).exists(),
                })

            return HttpResponse(json.dumps({"status":"true","category_list":_category_list}),content_type="application/json")
        except Exception ,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"系统删除目录除错" + e}),content_type="application/json")


#10
class CategoryQuery(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:

            session = request.GET['session']
            # _uid =
             #user 不存在
            if  User.objects.filter( session = session).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在"}),content_type="application/json" )

            _uid = User.objects.get( session = session)
            # 1 用户名下的所有目录
            # 目录下包含的图片
            _list = Category.objects.filter( user_id = _uid)
            print _list
            _category_list = []
            for c in _list:
                _category_list.append({
                    "category_id":c.id,
                    "name":c.name,
                    "is_default":c.is_default,
                    "hasImg":RelCategoryImg.objects.filter( category = c ).exists(),
                })

            return HttpResponse(json.dumps({"status":"true","category_list":_category_list}),content_type="application/json")
        except Exception ,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"系统查询目录除错" + e}),content_type="application/json")

#11

app_id = "wx00098b11d40e8910"
app_secret = "34362b7f79645d0659c5950e21e892cd"
# app_secret = "34362b7f79645d0659c5950e21e892"

class UserLogin(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):

        _expires = 1000000000 #session存活秒数
        _js_code = request.GET['js_code']
        _session = request.GET['session']

        _session_url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code "  %(app_id,app_secret,_js_code )

        # if  _session == "false":  #像weixin查询openid,secret_key
        def WX_GetSession(_session_url):
            req = urllib2.Request(_session_url)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(req)
            _json =  json.loads(response.read())
            return _json

        try:
            # raise NameError("There is a name error","in test.py")

            if  User.objects.filter( session = _session ).exists() is False: #查session不存在,更新整个用户

                _json = WX_GetSession(_session_url)
                print _json
                if _json.has_key('errcode') : #登陆信息错误，结束
                    return HttpResponse(json.dumps({"status":"false","msg":_json["errmsg"] }),content_type="application/json")

                #查open_id存在user表中
                _expires_in =  time.time() + _json["expires_in"]  #存在时间
                _new_session = _js_code + str(time.time())
                _new_expires = time.time() + _expires

                if  User.objects.filter( wx_open_id =  _json["openid"] ).exists():
                    _user = User.objects.get( wx_open_id =  _json["openid"] ) #用户存在，增加session
                    _user.wx_session_key =  _json["session_key"]
                    _user.wx_expires_in = _expires_in
                    _user.session = _new_session
                    _user.expires = _new_expires #当前时间+存活秒数
                    _user.save()
                    #登陆成功 ，返回session
                    return HttpResponse(json.dumps({"status":"true","session":_new_session }),content_type="application/json")
                else:
                    #不存在，新增用户
                    _user = User(
                        wx_open_id = _json["openid"],
                        wx_session_key =  _json["session_key"],
                        wx_expires_in = _expires_in,
                        session = _new_session,
                        expires = _new_expires,
                    )
                    _user.save()
                    #新增默认目录
                    _category = Category(
                        name = u"默认目录",
                        user_id = _user,
                        is_default = 1,
                    )
                    _category.save()
                    #登陆成功 ，返回session
                    return HttpResponse(json.dumps({"status":"true","session":_new_session }),content_type="application/json")
            else : #session 存在，
                _user = User.objects.get( session = _session )

                if time.time() > _user.wx_expires_in : #wx_session 过期
                    _json = WX_GetSession(_session_url)
                    if _json["errcode"] : #登陆信息错误，结束
                        return HttpResponse(json.dumps({"status":"false","msg":_json["errmsg"] }),content_type="application/json")

                    if _user.wx_open_id == _json["openid"]: #用户存在，跟新wx_session信息
                        _user.wx_session_key = _json["session_key"]
                        _user.wx_expires_in = time.time() + _json["expires_in"]
                        _user.save()
                    else:
                        return HttpResponse(json.dumps({"status":"false","msg":"微信错误。未回复open_id" }),content_type="application/json")

                if time.time() >_user.expires: # python 的session过期
                    _new_session = _js_code + str(time.time())  #新的后台session
                    _new_expires = time.time() + _expires #新的后台过期时间
                    _user.session = _new_session
                    _user.expires = _new_expires
                    _user.save()
                    return HttpResponse(json.dumps({"status":"true","session":_new_session }),content_type="application/json")

                print _session
                #session未过期，回复继续使用
                return HttpResponse(json.dumps({"status":"true","session":_session }),content_type="application/json")
        except Exception ,e:
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"用户登录错误" + e}),content_type="application/json")

#视频转GIF
class Video2Gif(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:

            session = request.GET['session']
            video_url = request.GET['video_url']

            if  User.objects.filter( session = session).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在,请重新登录"}),content_type="application/json" )

            _user = User.objects.get( session = session)


             #下载文件
            name = str(video_url).split("/")[-1]
            img_down_path = FILE_PATH.Down(name)["local_path"]
            f = urllib2.urlopen(video_url)
            data = f.read()
            with open(img_down_path, "wb") as code:
                code.write(data)

            #GIf路径
            img_type = "gif"
            _up_path = FILE_PATH.Up(img_type,_user.id) #按用户id命名图片

            #视频转换
            # magick = Magick(_up_path["local_path"])
            # magick.Video2Gif(0,6,img_down_path)
            _cmd = u"python %s  %s %s %s %s" % ( FILE_PATH.GetMagickPy(),img_down_path, _up_path["local_path"],0,6)
            subprocess.check_output(_cmd, shell=True)

            size = 1
            _qiniu = QiNiu()
            if _qiniu.put("",_up_path["file_name"],_up_path["local_path"]) is True: #上传原图
                # 4 上传成，存储数据库
                _yun_url = SETTING.QINIU_HOST + _up_path["file_name"]
                print _yun_url
                _img = Img(
                    name = _up_path["file_name"],
                    yun_url = _yun_url,
                    size = size,
                )
                _img.save()

                #上传的图片添加至该用户的默认目录
                _category = Category.objects.get( user_id = _user ,is_default = 1)
                _rel = RelCategoryImg(category = _category,img = _img )
                _rel.save()

                r_img = {
                    "img_id":_img.id,
                    "yun_url":_img.yun_url, # 七牛云自动缩略图
                    "size":_img.size ,
                    "category_name":_category.name,
                    "category_id":_category.id,
                }
                return HttpResponse(json.dumps({"status":"true","img":r_img}),content_type="application/json")
            return HttpResponse(json.dumps({"status":"false","msg":"上传七牛云失败"}),content_type="application/json")
        except Exception ,e:
            logger.error( e)
            print e
            return HttpResponse(json.dumps({"status":"false","msg":str(e)}),content_type="application/json")


#视频转GIF
class Join(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            session = request.GET['session']
            first_url = request.GET['first']
            seconde_url = request.GET['seconde']

            # return  HttpResponse( json.dumps({"status":"false","1":first_url,"2":seconde_url}),content_type="application/json" )
            if  User.objects.filter( session = session).exists() is False:
                return HttpResponse( json.dumps({"status":"false","msg":u"用户不存在,请重新登录"}),content_type="application/json" )
            _user = User.objects.get( session = session)

            def DownImg(img_url):
             #下载文件
                name = str(img_url).split("/")[-1]
                img_down_path = FILE_PATH.Down(name)["local_path"]
                print img_down_path
                f = urllib2.urlopen(img_url)
                data = f.read()
                with open(img_down_path, "wb") as code:
                    code.write(data)
                return img_down_path

            #GIf路径
            _up_path = FILE_PATH.Up("gif",_user.id) #按用户id命名图片

            _first_path = DownImg(first_url)
            _seconde_path = DownImg(seconde_url)

            #GIF拼接
            magick = Magick()
            magick.Join([_first_path,_seconde_path],_up_path["local_path"])


            size = 1
            _qiniu = QiNiu()
            if _qiniu.put("",_up_path["file_name"],_up_path["local_path"]) is True: #上传原图
                # 4 上传成，存储数据库
                _yun_url = SETTING.QINIU_HOST + _up_path["file_name"]
                print _yun_url
                _img = Img(
                    name = _up_path["file_name"],
                    yun_url = _yun_url,
                    size = size,
                )
                _img.save()

                #上传的图片添加至该用户的默认目录
                _category = Category.objects.get( user_id = _user ,is_default = 1)
                _rel = RelCategoryImg(category = _category,img = _img )
                _rel.save()

                r_img = {
                    "img_id":_img.id,
                    "yun_url":_img.yun_url, # 七牛云自动缩略图
                    "size":_img.size ,
                    "category_name":_category.name,
                    "category_id":_category.id,
                }
                return HttpResponse(json.dumps({"status":"true","img":r_img}),content_type="application/json")
            return HttpResponse(json.dumps({"status":"false","msg":"上传七牛云失败"}),content_type="application/json")
        except Exception ,e:
            logger.error( e)
            print e
            return HttpResponse(json.dumps({"status":"false","msg":str(e)}),content_type="application/json")


class Movie(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        _startTime = request.GET['startTime']
        _endTime =  request.GET['endTime']
        _save_path =  request.GET['save_path']
        _path =  request.GET['path']
        _speed = 1.5
        _resize = float(180.00/320.00) #把320*40的视频转192*144
        _fps = 10
        # print VideoFileClip(url)
        clip = (VideoFileClip(_path)
                .subclip((0,_startTime),(0,_endTime))
                .speedx(_speed)
                .resize(_resize)
                # .fx(vfx.freeze_region, outside_region=(170, 230, 380, 320))
                )
        clip.write_gif(_save_path, fps=_fps)
        return HttpResponse(True)



#12 标签 -增加
class TagAdd(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            _session = request.GET['session']
            _category_name = request.GET['tag_name']
            _category_parent_id = request.GET['tag_parent_id']
            print _category_name,_category_parent_id
            if Category.objects.filter(name = _category_name,user_id=None).exists() is False: #不允许重名
                if _category_parent_id == "":
                    _category = Category(
                        name = _category_name,
                    )
                else:
                    _parent = Category.objects.get( id = _category_parent_id)
                    # Category.objects.create(
                    #     name = _category_name,
                    #     parent_id = _parent
                    # )
                    _category = Category(
                        name = _category_name,
                        parent_id = _parent
                    )
                    print _parent,_category.parent_id,_category.parent_id.id
                _category.save()
                c_dict = {
                    "category_id":_category.id,
                    "name":_category.name,
                    # "is_default":_category.is_default,
                }
                return HttpResponse(json.dumps({"status":"true","category":c_dict}),content_type="application/json")
            return HttpResponse(json.dumps({"status":"false","msg":u"标签已存在"}),content_type="application/json")
        except Exception ,e:
            log.error(e,None,"TagAdd")
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"增加标签出错"}),content_type="application/json")

#13 标签 - 查询
class TagQuery(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            self._session = request.GET['session']
            #1 全部标签查询
            _list = Category.objects.filter( user_id = None)
            print _list
            _category_list = []
            for c in _list:
                if c.parent_id is None:
                    _parent_id = None
                else:
                    _parent_id = c.parent_id.id
                _category_list.append({
                    "category_id":c.id,
                    "name":c.name,
                    "parent_id": _parent_id,
                })
            return HttpResponse(json.dumps({"status":"true","category_list":_category_list}),content_type="application/json")

            #2 Todo 模糊查询

        except Exception ,e:
            log.error(e,None,"TagQuery")
            return HttpResponse(json.dumps({"status":"false","msg":u"查询标签出错" }),content_type="application/json")

#13 标签 - 贴标签
class TagImgAdd(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            self._session = request.GET['session']
            _category_id_list = [43]
            # _category_id_list = list(request.GET['tag_id_list'] ) #Todo 小程序get请求还会出错
            _img_id = request.GET['img_id']
            print _category_id_list,type(_category_id_list)

            _img = Img.objects.get( id = _img_id )
            for c in _category_id_list:
                # print Category.objects.filter(id = c , parent_id = None).exists()
                if Category.objects.filter(id = c , parent_id = None).exists() is False: # 是否为父类 ， 子类绑定图片，父类不行
                    _category = Category.objects.get( id = c )
                    print _category
                    if RelCategoryImg.objects.filter(img=_img , category = _category).exists() is False: #
                        _rel = RelCategoryImg(
                            img=_img ,
                            category = _category,
                        )
                        _rel.save()
                        print _rel
            return HttpResponse(json.dumps({"status":"true","msg":u"标签添加成功"}),content_type="application/json")
        except Exception ,e:
            log.error(e,None,"TagImgAdd")
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"查询标签出错" }),content_type="application/json")

#点击标签，查询图片
class TagImgQuery(BaseMixin, ListView):
    def get(self, request, *args, **kwargs):
        try:
            self._session = request.GET['session']
            _category_name = request.GET['tag_name']
            #1 精确查询
            _category = Category.objects.get( name = _category_name,user_id=None)  #,parent_id=None
            _img_list = []
            for _r in RelCategoryImg.objects.filter(category=_category):
                _img_list.append({
                    "img_id":_r.img.id,
                    "yun_url":_r.img.yun_url, # 七牛云自动缩略图
                    "size":_r.img.size
                })
            return HttpResponse(json.dumps({"status":"true","img_list":_img_list}),content_type="application/json")
            #2 Todo 模糊查询

        except Exception ,e:
            log.error(e,None,"TagImgQuery")
            print e
            return HttpResponse(json.dumps({"status":"false","msg":u"查询标签出错" }),content_type="application/json")